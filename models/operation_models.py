from models.base_models import OperationBase
from models.params_models import *
from schematics import types



class AddOperation(OperationBase):
    operation_type = types.StringType(default='addoperation', required=True),
    params= types.ListType(
        types.ModelType('models.params_models.AddParams'),
        required=True,
        min_size=1
    )

    def calculate(self):
        if not self.params:
            return 0.0
        return self.params[0].calculate()

class SubtractOperation(OperationBase):
    operation_type = types.StringType(default='subtractoperation', required=True)
    params= types.ListType(
        types.ModelType('models.params_models.SubtractParams'),
        required=True,
        min_size=1
    )

    def calculate(self):
        if not self.params:
            return 0.0
        return self.params[0].calculate()

class MultiplyOperation(OperationBase):
    operation_type = types.StringType(default='multiplyoperation', required=True)
    params= types.ListType(
        types.ModelType('models.params_models.MultiplyParams'),
        required=True,
        min_size=1
    )
    def calculate(self):
        if not self.params:
            return 0.0
        return self.params[0].calculate()

class DivideOperation(OperationBase):
    operation_type = types.StringType(default='divideoperation', required=True)
    params= types.ListType(
        types.ModelType('models.params_models.DivideParams'),
        required=True,
        min_size=1
    )

    def calculate(self):
        if not self.params:
            return 0.0
        return self.params[0].calculate()

class PowerOperation(OperationBase):
    operation_type = types.StringType(default='poweroperation', required=True)
    params= types.ListType(
        types.ModelType('models.params_models.PowerParams'),
        required=True,
        min_size=1
    )

    def calculate(self):
        if not self.params:
            return 0.0
        return self.params[0].calculate()


