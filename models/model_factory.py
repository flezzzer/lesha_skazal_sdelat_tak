from .models import (
    IntValue, FloatValue, Variable, Expression,
    Add, Subtract, Multiply, Divide, Power,
    AddParams, SubtractParams, MultiplyParams, DivideParams, PowerParams
)


class ModelFactory:

    @staticmethod
    def create_int(value):
        return IntValue({'value': float(value), 'type': 'IntValue'})

    @staticmethod
    def create_float(value):
        return FloatValue({'value': value, 'type': 'FloatValue'})

    @staticmethod
    def create_variable(name):
        return Variable({'type': 'Variable', 'name': name})

    @staticmethod
    def create_expression(operation):
        if isinstance(operation, Expression):
            return operation
        return Expression({'expression': operation, 'type': 'Expression'})

    @staticmethod
    def _wrap_args(args):
        wrapped_args = []
        for a in args:
            if isinstance(a, (IntValue, FloatValue, Variable, Expression)):
                wrapped_args.append(a)
            elif isinstance(a, (Add, Subtract, Multiply, Divide, Power)):
                wrapped_args.append(ModelFactory.create_expression(a))
            elif isinstance(a, (int, float)):
                if isinstance(a, int) or (isinstance(a, float) and a.is_integer()):
                    wrapped_args.append(ModelFactory.create_int(a))
                else:
                    wrapped_args.append(ModelFactory.create_float(a))
            elif isinstance(a, str):
                wrapped_args.append(ModelFactory.create_variable(a))
            else:
                raise TypeError(f"Unsupported arg type {type(a)}")
        return wrapped_args

    @staticmethod
    def create_operation(operation_name, args):
        operation_map = {
            'add': ModelFactory.create_add_operation,
            'subtract': ModelFactory.create_subtract_operation,
            'multiply': ModelFactory.create_multiply_operation,
            'divide': ModelFactory.create_divide_operation,
            'power': ModelFactory.create_power_operation,
        }

        if operation_name not in operation_map:
            raise ValueError(f"Unknown operation: {operation_name}")

        return operation_map[operation_name](args)

    @staticmethod
    def create_add_operation(args):
        wrapped_args = ModelFactory._wrap_args(args)
        params = AddParams({
            'type': 'AddParams',
            'args': wrapped_args
        })
        return Add({
            'type': 'Add',
            'params': params
        })

    @staticmethod
    def create_subtract_operation(args):
        wrapped_args = ModelFactory._wrap_args(args)
        params = SubtractParams({
            'type': 'SubtractParams',
            'args': wrapped_args
        })
        return Subtract({
            'type': 'Subtract',
            'params': params
        })

    @staticmethod
    def create_multiply_operation(args):
        wrapped_args = ModelFactory._wrap_args(args)
        params = MultiplyParams({
            'type': 'MultiplyParams',
            'args': wrapped_args
        })
        return Multiply({
            'type': 'Multiply',
            'params': params
        })

    @staticmethod
    def create_divide_operation(args):
        wrapped_args = ModelFactory._wrap_args(args)
        params = DivideParams({
            'type': 'DivideParams',
            'args': wrapped_args
        })
        return Divide({
            'type': 'Divide',
            'params': params
        })

    @staticmethod
    def create_power_operation(args):
        wrapped_args = ModelFactory._wrap_args(args)
        params = PowerParams({
            'type': 'PowerParams',
            'args': wrapped_args
        })
        return Power({
            'type': 'Power',
            'params': params
        })

    @staticmethod
    def calculate(operation_name, args, context=None):
        operation = ModelFactory.create_operation(operation_name, args)
        expr = ModelFactory.create_expression(operation)
        return expr.calculate(context)