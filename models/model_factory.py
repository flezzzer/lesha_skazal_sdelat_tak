from .models import (
    IntValue, FloatValue, Expression,
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
    def create_expression(operation):
        if isinstance(operation, Expression):
            return operation
        return Expression({'expression': operation, 'type': 'Expression'})

    @staticmethod
    def _wrap_args(args):
        wrapped_args = []
        for a in args:
            if isinstance(a, (IntValue, FloatValue, Expression)):
                wrapped_args.append(a)
            elif isinstance(a, (Add, Subtract, Multiply, Divide, Power)):
                wrapped_args.append(ModelFactory.create_expression(a))
            else:
                raise TypeError(f"Unsupported arg type {type(a)}")
        return wrapped_args

    @staticmethod
    def _create_params(params_class, wrapped_args, params_type):
        return params_class({
            'type': params_type,
            'args': wrapped_args
        })

    @staticmethod
    def create_add_operation(args):
        wrapped_args = ModelFactory._wrap_args(args)
        params = ModelFactory._create_params(AddParams, wrapped_args, 'AddParams')
        return Add({
            'type': 'Add',
            'params': params
        })

    @staticmethod
    def create_subtract_operation(args):
        wrapped_args = ModelFactory._wrap_args(args)
        params = ModelFactory._create_params(SubtractParams, wrapped_args, 'SubtractParams')
        return Subtract({
            'type': 'Subtract',
            'params': params
        })

    @staticmethod
    def create_multiply_operation(args):
        wrapped_args = ModelFactory._wrap_args(args)
        params = ModelFactory._create_params(MultiplyParams, wrapped_args, 'MultiplyParams')
        return Multiply({
            'type': 'Multiply',
            'params': params
        })

    @staticmethod
    def create_divide_operation(args):
        wrapped_args = ModelFactory._wrap_args(args)
        params = ModelFactory._create_params(DivideParams, wrapped_args, 'DivideParams')
        return Divide({
            'type': 'Divide',
            'params': params
        })

    @staticmethod
    def create_power_operation(args):
        wrapped_args = ModelFactory._wrap_args(args)
        params = ModelFactory._create_params(PowerParams, wrapped_args, 'PowerParams')
        return Power({
            'type': 'Power',
            'params': params
        })