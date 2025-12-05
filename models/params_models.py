from models.base_models import ParamsBase
from schematics import types
from models.value_models import *

def value_claim_function(field_instance, data):
    value_type = data.get('value_type')
    if value_type == 'valueint':
        return 'models.value_models.ValueInt'
    if value_type == 'valuefloat':
        return 'models.value_models.ValueFloat'
    if value_type == 'valueexpression':
        return 'models.value_models.ValueExpression'
    return None

ArgsPolyList = types.ListType(
    types.PolyModelType(
        model_spec=[
            'models.value_models.ValueInt',
            'models.value_models.ValueFloat',
            'models.value_models.ValueExpression'
        ],
        claim_function=value_claim_function
    ),
    required=True,
    min_size=1
)

class AddParams(ParamsBase):
    params_type = types.StringType(default='addparams', required=True)
    args = ArgsPolyList

    def calculate(self):
        return sum(arg.calculate() for arg in self.args)


class SubtractParams(ParamsBase):
    params_type = types.StringType(default='subtractparams', required=True)
    args = ArgsPolyList

    def calculate(self):
        if not self.args:
            return 0.0
        result = self.args[0].calculate()
        for arg in self.args[1:]:
            result -= arg.calculate()
        return result


class MultiplyParams(ParamsBase):
    params_type = types.StringType(default='multiplyparams', required=True)
    args = ArgsPolyList

    def calculate(self):
        result = 1.0
        for arg in self.args:
            result *= arg.calculate()
        return result


class DivideParams(ParamsBase):
    params_type = types.StringType(default='divideparams', required=True)
    args = ArgsPolyList

    def calculate(self):
        if not self.args:
            return 0.0
        result = self.args[0].calculate()
        for arg in self.args[1:]:
            val = arg.calculate()
            if val == 0:
                raise ValueError("Деление на ноль")
            result /= val
        return result


class PowerParams(ParamsBase):
    params_type = types.StringType(default='powerparams', required=True)

    def calculate(self):
        if not self.args:
            return 0.0
        result = self.args[0].calculate()
        for arg in self.args[1:]:
            result **= arg.calculate()
        return result