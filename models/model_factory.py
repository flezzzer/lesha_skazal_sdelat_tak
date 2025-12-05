from .models import (
    ValueInt, ValueFloat, ValueExpression,
    AddOperation, SubtractOperation, MultiplyOperation, DivideOperation, PowerOperation
)


class ModelFactory:

    @staticmethod
    def create_int(value):
        return ValueInt({'value': float(value), 'value_type': 'valueint'})

    @staticmethod
    def create_float(value):
        return ValueFloat({'value': value, 'value_type': 'valuefloat'})

    @staticmethod
    def create_expression(operation):
        if isinstance(operation, ValueExpression):
            return operation
        return ValueExpression({'expression': operation, 'value_type': 'valueexpression'})

    @staticmethod
    def _wrap_args(args):
        wrapped_args = []
        for a in args:
            if isinstance(a, (ValueInt, ValueFloat, ValueExpression)):
                wrapped_args.append(a)
            elif isinstance(a, (AddOperation, SubtractOperation, MultiplyOperation, DivideOperation, PowerOperation)):
                wrapped_args.append({'expression': a, 'value_type': 'valueexpression'})
            else:
                raise TypeError(f"Unsupported arg type {type(a)}")
        return wrapped_args

    @staticmethod
    def create_add_operation(args):
        wrapped_args = ModelFactory._wrap_args(args)
        return AddOperation({
            'operation_type': 'addoperation',
            'params': [{
                'params_type': 'addparams',
                'args': wrapped_args
            }]
        })

    @staticmethod
    def create_subtract_operation(args):
        wrapped_args = ModelFactory._wrap_args(args)
        return SubtractOperation({
            'operation_type': 'subtractoperation',
            'params': [{
                'params_type': 'subtractparams',
                'args': wrapped_args
            }]
        })

    @staticmethod
    def create_multiply_operation(args):
        wrapped_args = ModelFactory._wrap_args(args)
        return MultiplyOperation({
            'operation_type': 'multiplyoperation',
            'params': [{
                'params_type': 'multiplyparams',
                'args': wrapped_args
            }]
        })

    @staticmethod
    def create_divide_operation(args):
        wrapped_args = ModelFactory._wrap_args(args)
        return DivideOperation({
            'operation_type': 'divideoperation',
            'params': [{
                'params_type': 'divideparams',
                'args': wrapped_args
            }]
        })

    @staticmethod
    def create_power_operation(args):
        wrapped_args = ModelFactory._wrap_args(args)
        return PowerOperation({
            'operation_type': 'poweroperation',
            'params': [{
                'params_type': 'powerparams',
                'args': wrapped_args
            }]
        })
