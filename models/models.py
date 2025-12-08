from schematics import Model, types
from schematics.exceptions import ValidationError


class ClaimRegistry:
    _value_claim_map = {}
    _operation_claim_map = {}
    _params_claim_map = {}

    @classmethod
    def register_value(cls, value_type, model_class):
        cls._value_claim_map[value_type] = model_class

    @classmethod
    def register_operation(cls, operation_type, model_class):
        cls._operation_claim_map[operation_type] = model_class

    @classmethod
    def register_params(cls, params_type, model_class):
        cls._params_claim_map[params_type] = model_class

    @classmethod
    def value_claim_function(cls, field_instance, data):
        value_type = data.get('value_type')
        return cls._value_claim_map.get(value_type)

    @classmethod
    def operation_claim_function(cls, field_instance, data):
        operation_type = data.get('operation_type')
        return cls._operation_claim_map.get(operation_type)

    @classmethod
    def params_claim_function(cls, field_instance, data):
        params_type = data.get('params_type')
        return cls._params_claim_map.get(params_type)


class ValueBase(Model):
    def calculate(self):
        raise NotImplementedError()


class ValueInt(ValueBase):
    value_type = types.StringType(default="valueint", required=True)
    value = types.FloatType(required=True)

    def validate_value(self, data, val):
        if not val.is_integer():
            raise ValidationError(f"Value {val} must be integer for ValueInt")
        return val

    def calculate(self):
        return float(self.value)


class ValueFloat(ValueBase):
    value_type = types.StringType(default="valuefloat", required=True)
    value = types.FloatType(required=True)

    def calculate(self):
        return self.value


class ParamsBase(Model):
    params_type = types.StringType(required=True)

    def calculate(self):
        raise NotImplementedError()


class AddParams(ParamsBase):
    params_type = types.StringType(default="addparams", required=True)
    args = types.ListType(
        types.PolyModelType(
            model_spec=[ValueInt, ValueFloat, lambda: ValueExpression],
            claim_function=ClaimRegistry.value_claim_function
        ),
        required=True,
        min_size=1
    )

    def calculate(self):
        return sum(a.calculate() for a in self.args)


class SubtractParams(ParamsBase):
    params_type = types.StringType(default="subtractparams", required=True)
    args = types.ListType(
        types.PolyModelType(
            model_spec=[ValueInt, ValueFloat, lambda: ValueExpression],
            claim_function=ClaimRegistry.value_claim_function
        ),
        required=True,
        min_size=1
    )

    def calculate(self):
        r = self.args[0].calculate()
        for a in self.args[1:]:
            r -= a.calculate()
        return r


class MultiplyParams(ParamsBase):
    params_type = types.StringType(default="multiplyparams", required=True)
    args = types.ListType(
        types.PolyModelType(
            model_spec=[ValueInt, ValueFloat, lambda: ValueExpression],
            claim_function=ClaimRegistry.value_claim_function
        ),
        required=True,
        min_size=1
    )

    def calculate(self):
        r = 1.0
        for a in self.args:
            r *= a.calculate()
        return r


class DivideParams(ParamsBase):
    params_type = types.StringType(default="divideparams", required=True)
    args = types.ListType(
        types.PolyModelType(
            model_spec=[ValueInt, ValueFloat, lambda: ValueExpression],
            claim_function=ClaimRegistry.value_claim_function
        ),
        required=True,
        min_size=1
    )

    def calculate(self):
        r = self.args[0].calculate()
        for a in self.args[1:]:
            v = a.calculate()
            if v == 0:
                raise ValueError("Деление на ноль")
            r /= v
        return r


class PowerParams(ParamsBase):
    params_type = types.StringType(default="powerparams", required=True)
    args = types.ListType(
        types.PolyModelType(
            model_spec=[ValueInt, ValueFloat, lambda: ValueExpression],
            claim_function=ClaimRegistry.value_claim_function
        ),
        required=True,
        min_size=1
    )

    def calculate(self):
        r = self.args[0].calculate()
        for a in self.args[1:]:
            r **= a.calculate()
        return r


class OperationBase(Model):
    operation_type = types.StringType(required=True)

    def calculate(self):
        raise NotImplementedError()


class AddOperation(OperationBase):
    operation_type = types.StringType(default="addoperation", required=True)
    params = types.ListType(types.ModelType(AddParams), required=True, min_size=1)

    def calculate(self):
        return self.params[0].calculate()


class SubtractOperation(OperationBase):
    operation_type = types.StringType(default="subtractoperation", required=True)
    params = types.ListType(types.ModelType(SubtractParams), required=True, min_size=1)

    def calculate(self):
        return self.params[0].calculate()


class MultiplyOperation(OperationBase):
    operation_type = types.StringType(default="multiplyoperation", required=True)
    params = types.ListType(types.ModelType(MultiplyParams), required=True, min_size=1)

    def calculate(self):
        return self.params[0].calculate()


class DivideOperation(OperationBase):
    operation_type = types.StringType(default="divideoperation", required=True)
    params = types.ListType(types.ModelType(DivideParams), required=True, min_size=1)

    def calculate(self):
        return self.params[0].calculate()


class PowerOperation(OperationBase):
    operation_type = types.StringType(default="poweroperation", required=True)
    params = types.ListType(types.ModelType(PowerParams), required=True, min_size=1)

    def calculate(self):
        return self.params[0].calculate()


class ValueExpression(ValueBase):
    value_type = types.StringType(default="valueexpression", required=True)
    expression = types.PolyModelType(
        model_spec=[
            AddOperation,
            SubtractOperation,
            MultiplyOperation,
            DivideOperation,
            PowerOperation,
        ],
        claim_function=ClaimRegistry.operation_claim_function,
        required=True,
    )

    def calculate(self):
        return self.expression.calculate()


ArgsPolyList = types.ListType(
    types.PolyModelType(
        model_spec=[ValueInt, ValueFloat, lambda: ValueExpression],
        claim_function=ClaimRegistry.value_claim_function,
    ),
    required=True,
    min_size=1,
)


ClaimRegistry.register_value('valueint', ValueInt)
ClaimRegistry.register_value('valuefloat', ValueFloat)
ClaimRegistry.register_value('valueexpression', ValueExpression)

ClaimRegistry.register_operation('addoperation', AddOperation)
ClaimRegistry.register_operation('subtractoperation', SubtractOperation)
ClaimRegistry.register_operation('multiplyoperation', MultiplyOperation)
ClaimRegistry.register_operation('divideoperation', DivideOperation)
ClaimRegistry.register_operation('poweroperation', PowerOperation)

ClaimRegistry.register_params('addparams', AddParams)
ClaimRegistry.register_params('subtractparams', SubtractParams)
ClaimRegistry.register_params('multiplyparams', MultiplyParams)
ClaimRegistry.register_params('divideparams', DivideParams)
ClaimRegistry.register_params('powerparams', PowerParams)