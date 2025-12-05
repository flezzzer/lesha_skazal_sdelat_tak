from schematics import Model, types

class ValueBase(Model):
    def calculate(self):
        raise NotImplementedError()

class OperationBase(Model):
    operation_type = types.StringType(required=True)
    def calculate(self):
        raise NotImplementedError()

class ParamsBase(Model):
    params_type = types.StringType(required=True)

    def calculate(self):
        raise NotImplementedError()


class ValueInt(ValueBase):
    value_type = types.StringType(default='valueint', required=True)
    value = types.FloatType(required=True)

    def validate_value(self, data, val):
        from schematics.exceptions import ValidationError
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
        claim_function='operation_claim_function',
        required=True
    )

    def calculate(self):
        return self.expression.calculate()


class AddOperation(OperationBase):
    operation_type = types.StringType(default='addoperation', required=True)
    params= types.ListType(
        types.ModelType('AddParams'),
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
        types.ModelType('SubtractParams'),
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
        types.ModelType('MultiplyParams'),
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
        types.ModelType('DivideParams'),
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
        types.ModelType('PowerParams'),
        required=True,
        min_size=1
    )

    def calculate(self):
        if not self.params:
            return 0.0
        return self.params[0].calculate()




class AddParams(ParamsBase):
    params_type = types.StringType(default='addparams', required=True)
    args = 'ArgsPolyList'

    def calculate(self):
        return sum(arg.calculate() for arg in self.args)


class SubtractParams(ParamsBase):
    params_type = types.StringType(default='subtractparams', required=True)
    args = 'ArgsPolyList'

    def calculate(self):
        if not self.args:
            return 0.0
        result = self.args[0].calculate()
        for arg in self.args[1:]:
            result -= arg.calculate()
        return result


class MultiplyParams(ParamsBase):
    params_type = types.StringType(default='multiplyparams', required=True)
    args = 'ArgsPolyList'

    def calculate(self):
        result = 1.0
        for arg in self.args:
            result *= arg.calculate()
        return result


class DivideParams(ParamsBase):
    params_type = types.StringType(default='divideparams', required=True)
    args = 'ArgsPolyList'

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
    args = 'ArgsPolyList'
    def calculate(self):
        if not self.args:
            return 0.0
        result = self.args[0].calculate()
        for arg in self.args[1:]:
            result **= arg.calculate()
        return result

def value_claim_function(field_instance, data):
    value_type = data.get('value_type')
    if value_type == 'valueint':
        return ValueInt
    if value_type == 'valuefloat':
        return ValueFloat
    if value_type == 'valueexpression':
        return ValueExpression
    return None

all_operations = ['AddOperation', 'SubtractOperation', 'MultiplyOperation', 'DivideOperation', 'PowerOperation']


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


ArgsPolyList = types.ListType(
    types.PolyModelType(
        model_spec=[
            ValueInt,
            ValueFloat,
            ValueExpression
        ],
        claim_function=value_claim_function
    ),
    required=True,
    min_size=1
)


AddParams.args= ArgsPolyList
SubtractParams.args= ArgsPolyList
MultiplyParams.args= ArgsPolyList
DivideParams.args= ArgsPolyList
PowerParams.args= ArgsPolyList
