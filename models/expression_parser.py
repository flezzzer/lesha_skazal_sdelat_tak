import ast
from .model_factory import ModelFactory
import collections

class ExpressionParser:
    OP_MAPPING = {
        ast.Add: ModelFactory.create_add_operation,
        ast.Sub: ModelFactory.create_subtract_operation,
        ast.Mult: ModelFactory.create_multiply_operation,
        ast.Div: ModelFactory.create_divide_operation,
        ast.Pow: ModelFactory.create_power_operation,
    }

    @staticmethod
    def _parse_leaf(node):
        if isinstance(node, ast.Num):
            if isinstance(node.n, int):
                return ModelFactory.create_int(node.n)
            elif isinstance(node.n, float):
                return ModelFactory.create_float(node.n)
        elif isinstance(node, ast.Name):
            from .models import Variable
            var_instance = Variable()
            var_instance.import_data({'type': 'Variable', 'name': node.id})
            var_instance.validate()
            return var_instance
        elif isinstance(node, ast.BinOp):
            return ExpressionParser._parse_node(node)
        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                operand = ExpressionParser._parse_leaf(node.operand)
                return ModelFactory.create_multiply_operation([
                    ModelFactory.create_int(-1),
                    operand
                ])
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                if isinstance(node.value, int):
                    return ModelFactory.create_int(node.value)
                else:
                    return ModelFactory.create_float(node.value)
        raise TypeError(f"Unsupported leaf node: {node}")

    @staticmethod
    def _collect_same_ops(node, target_op):
        if isinstance(node, ast.BinOp):
            if type(node.op) == target_op:
                left_args = ExpressionParser._collect_same_ops(node.left, target_op)
                right_args = ExpressionParser._collect_same_ops(node.right, target_op)
                return left_args + right_args
        return [ExpressionParser._parse_leaf(node)]

    @staticmethod
    def _parse_node(node):
        if isinstance(node, ast.BinOp) and type(node.op) in ExpressionParser.OP_MAPPING:
            op_type = type(node.op)
            create_func = ExpressionParser.OP_MAPPING[op_type]

            args = ExpressionParser._collect_same_ops(node, op_type)
            if len(args) >= 2:
                return create_func(args)

            left = ExpressionParser._parse_leaf(node.left)
            right = ExpressionParser._parse_leaf(node.right)
            return create_func([left, right])

        return ExpressionParser._parse_leaf(node)

    @staticmethod
    def parse(expr):
        tree = ast.parse(expr, mode='eval')
        op = ExpressionParser._parse_node(tree.body)
        return ModelFactory.create_expression(op)