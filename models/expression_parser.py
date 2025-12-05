import ast
from .model_factory import ModelFactory

class ExpressionParser:

    @staticmethod
    def _parse_node(node):
        if isinstance(node, ast.BinOp):
            left = ExpressionParser._parse_node(node.left)
            right = ExpressionParser._parse_node(node.right)

            if isinstance(node.op, ast.Add):
                op = ModelFactory.create_add_operation([left, right])
            elif isinstance(node.op, ast.Sub):
                op = ModelFactory.create_subtract_operation([left, right])
            elif isinstance(node.op, ast.Mult):
                op = ModelFactory.create_multiply_operation([left, right])
            elif isinstance(node.op, ast.Div):
                op = ModelFactory.create_divide_operation([left, right])
            elif isinstance(node.op, ast.Pow):
                op = ModelFactory.create_power_operation([left, right])
            else:
                raise TypeError(f"Unsupported operator: {node.op}")

            return op

        elif isinstance(node, ast.Num):  # Python <3.8
            if isinstance(node.n, int):
                return ModelFactory.create_int(node.n)
            elif isinstance(node.n, float):
                return ModelFactory.create_float(node.n)
        elif isinstance(node, ast.Constant):  # Python 3.8+
            if isinstance(node.value, int):
                return ModelFactory.create_int(node.value)
            elif isinstance(node.value, float):
                return ModelFactory.create_float(node.value)
        else:
            raise TypeError(f"Unsupported AST node: {node}")

    @staticmethod
    def parse(expr):
        tree = ast.parse(expr, mode='eval')
        op = ExpressionParser._parse_node(tree.body)
        return ModelFactory.create_expression(op)
