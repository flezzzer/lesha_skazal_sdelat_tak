from schematics import types
from schematics.exceptions import ValidationError
from models.base_models import ValueBase
from models.operation_models import AddOperation, SubtractOperation, MultiplyOperation, DivideOperation, PowerOperation

all_operations = [AddOperation, SubtractOperation, MultiplyOperation, DivideOperation, PowerOperation]


def operation_claim_function(field_instance, data):
    op_type = data.get('operation_type')
    if op_type == 'addoperation':
        return AddOperation
    if op_type == 'subtractoperation':
        return SubtractOperation
    if op_type == 'multiplyoperation':
        return MultiplyOperation
    if op_type == 'divideoperation':
        return DivideOperation
    if op_type == 'poweroperation':
        return PowerOperation
    return None

class ValueInt(ValueBase):
    value_type = types.StringType(default='valueint', required=True)
    value = types.FloatType(required=True)

    def validate_value(self, data, val):
        if not val.is_integer():
            raise ValidationError(f"Value {val} must be integer for ValueInt")
        return val

    def calculate(self):
        return float(self.value)


class ValueFloat(ValueBase):
    value_type = types.StringType(default='valuefloat', required=True)
    value = types.FloatType(required=True)

    def calculate(self):
        return self.value


class ValueExpression(ValueBase):
    value_type = types.StringType(default='valueexpression', required=True)

    expression = types.PolyModelType(
        model_spec=['AddOperation', 'SubtractOperation', 'MultiplyOperation',
                    'DivideOperation', 'PowerOperation'],
        claim_function=operation_claim_function,
        required=True
    )

    def calculate(self):
        return self.expression.calculate()