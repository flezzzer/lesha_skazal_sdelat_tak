from schematics import Model, types
from schematics.exceptions import ValidationError

class PolymorphicBase(Model):
    _registry = {}
    _type_field = None

    @classmethod
    def register(cls, class_key, model_class):
        cls._registry[class_key] = model_class

    @classmethod
    def _claim(cls, data, ctx=None):
        if ctx and isinstance(ctx, dict):
            type_name = ctx.get(cls._type_field)
            if type_name:
                return cls._registry.get(type_name)
        return None

class ValueBase(PolymorphicBase):
    _type_field = "type"
    type = types.StringType(required=True)

    @classmethod
    def create_args_field(cls):
        return types.ListType(
            types.PolyModelType(
                model_spec=[IntValue, FloatValue, Expression],
                claim_function=cls._claim
            ),
            required=True,
            min_size=2
        )

    def calculate(self):
        raise NotImplementedError()

class IntValue(ValueBase):
    type = types.StringType(default="int", required=True)
    value = types.FloatType(required=True)

    def validate_value(self, data, val):
        if not val.is_integer():
            raise ValidationError(f"Value {val} must be integer for IntValue")
        return val

    def calculate(self):
        return float(self.value)

class FloatValue(ValueBase):
    type = types.StringType(default="float", required=True)
    value = types.FloatType(required=True)

    def calculate(self):
        return self.value

class ParamsBase(PolymorphicBase):
    _type_field = "type"
    type = types.StringType(required=True)

    @classmethod
    def create_params_field(cls, param_cls):
        return types.PolyModelType(
            model_spec=param_cls,
            claim_function=cls._claim,
            required=True
        )

    def calculate(self):
        raise NotImplementedError()

class OperationBase(PolymorphicBase):
    _type_field = "type"
    type = types.StringType(required=True)

    @classmethod
    def create_params_field(cls, param_cls):
        return types.PolyModelType(
            model_spec=param_cls,
            claim_function=ParamsBase._claim,
            required=True
        )

    def calculate(self):
        raise NotImplementedError()

class Expression(ValueBase):
    type = types.StringType(default="expression", required=True)
    expression = types.PolyModelType(
        model_spec=OperationBase,
        claim_function=OperationBase._claim,
        required=True
    )

    def calculate(self):
        return self.expression.calculate()

class AddParams(ParamsBase):
    type = types.StringType(default="add_params", required=True)
    args = ValueBase.create_args_field()

    def calculate(self):
        return sum(a.calculate() for a in self.args)

class SubtractParams(ParamsBase):
    type = types.StringType(default="subtract_params", required=True)
    args = ValueBase.create_args_field()

    def calculate(self):
        r = self.args[0].calculate()
        for a in self.args[1:]:
            r -= a.calculate()
        return r

class MultiplyParams(ParamsBase):
    type = types.StringType(default="multiply_params", required=True)
    args = ValueBase.create_args_field()

    def calculate(self):
        r = 1.0
        for a in self.args:
            r *= a.calculate()
        return r

class DivideParams(ParamsBase):
    type = types.StringType(default="divide_params", required=True)
    args = ValueBase.create_args_field()

    def calculate(self):
        r = self.args[0].calculate()
        for a in self.args[1:]:
            v = a.calculate()
            if v == 0:
                raise ValueError("Division by zero")
            r /= v
        return r

class PowerParams(ParamsBase):
    type = types.StringType(default="power_params", required=True)
    args = ValueBase.create_args_field()

    def calculate(self):
        r = self.args[0].calculate()
        for a in self.args[1:]:
            r **= a.calculate()
        return r

class Add(OperationBase):
    type = types.StringType(default="add", required=True)
    params = OperationBase.create_params_field(AddParams)

    def calculate(self):
        return self.params.calculate()

class Subtract(OperationBase):
    type = types.StringType(default="subtract", required=True)
    params = OperationBase.create_params_field(SubtractParams)

    def calculate(self):
        return self.params.calculate()

class Multiply(OperationBase):
    type = types.StringType(default="multiply", required=True)
    params = OperationBase.create_params_field(MultiplyParams)

    def calculate(self):
        return self.params.calculate()

class Divide(OperationBase):
    type = types.StringType(default="divide", required=True)
    params = OperationBase.create_params_field(DivideParams)

    def calculate(self):
        return self.params.calculate()

class Power(OperationBase):
    type = types.StringType(default="power", required=True)
    params = OperationBase.create_params_field(PowerParams)

    def calculate(self):
        return self.params.calculate()

ValueBase.register("int", IntValue)
ValueBase.register("float", FloatValue)
ValueBase.register("expression", Expression)

ParamsBase.register("add_params", AddParams)
ParamsBase.register("subtract_params", SubtractParams)
ParamsBase.register("multiply_params", MultiplyParams)
ParamsBase.register("divide_params", DivideParams)
ParamsBase.register("power_params", PowerParams)

OperationBase.register("add", Add)
OperationBase.register("subtract", Subtract)
OperationBase.register("multiply", Multiply)
OperationBase.register("divide", Divide)
OperationBase.register("power", Power)
