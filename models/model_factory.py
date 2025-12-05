from models.models import *


class ModelFactory:
    @staticmethod
    def create_int(value):
        return ValueInt({
            'value_type': 'valueint',
            'value': float(value)
        })

    @staticmethod
    def create_float(value):
        return ValueFloat({
            'value_type': 'valuefloat',
            'value': value
        })

    @staticmethod
    def create_expression(operation):
        return ValueExpression({
            'value_type': 'valueexpression',
            'expression': operation
        })

    @staticmethod
    def create_add_operation(args):
        params = AddParams({
            'params_type': 'addparams',
            'args': args
        })
        return AddOperation({
            'operation_type': 'addoperation',
            'params': [params]
        })

    @staticmethod
    def create_subtract_operation(args):
        params = SubtractParams({
            'params_type': 'subtractparams',
            'args': args
        })
        return SubtractOperation({
            'operation_type': 'subtractoperation',
            'params': [params]
        })

    @staticmethod
    def create_multiply_operation(args):
        params = MultiplyParams({
            'params_type': 'multiplyparams',
            'args': args
        })
        return MultiplyOperation({
            'operation_type': 'multiplyoperation',
            'params': [params]
        })

    @staticmethod
    def create_divide_operation(args):
        params = DivideParams({
            'params_type': 'divideparams',
            'args': args
        })
        return DivideOperation({
            'operation_type': 'divideoperation',
            'params': [params]
        })

    @staticmethod
    def create_power_operation(args):
        params = PowerParams({
            'params_type': 'powerparams',
            'args': args
        })
        return PowerOperation({
            'operation_type': 'poweroperation',
            'params': [params]
        })