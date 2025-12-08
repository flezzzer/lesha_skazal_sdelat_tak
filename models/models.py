from schematics import Model, types
from schematics.exceptions import ValidationError


class PolymorphicBase(Model):
    _registry = {}
    _type_field = None

    @classmethod
    def register(cls, class_key, model_class):
        cls._registry[class_key] = model_class

    @classmethod
    def _claim(cls, data):
        if cls._type_field:
            if isinstance(data, cls) and hasattr(data, cls._type_field):
                return type(data)
            if isinstance(data, dict) and cls._type_field in data:
                target_type = data[cls._type_field]
                return cls._registry.get(target_type)
            if isinstance(data, Model):
                for model_class in cls._registry.values():
                    if isinstance(data, model_class):
                        return type(data)
        return None


class ValueBase(PolymorphicBase):
    _type_field = "type"
    type = types.StringType(required=True)

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

    def calculate(self):
        raise NotImplementedError()


class AddParams(ParamsBase):
    type = types.StringType(default="add", required=True)
    args = types.ListType(
        types.PolyModelType(
            model_spec=ValueBase,
        ),
        required=True,
        min_size=2
    )

    def calculate(self):
        return sum(a.calculate() for a in self.args)


class SubtractParams(ParamsBase):
    type = types.StringType(default="subtract", required=True)
    args = types.ListType(
        types.PolyModelType(
            model_spec=ValueBase,
        ),
        required=True,
        min_size=2
    )

    def calculate(self):
        r = self.args[0].calculate()
        for a in self.args[1:]:
            r -= a.calculate()
        return r


class MultiplyParams(ParamsBase):
    type = types.StringType(default="multiply", required=True)
    args = types.ListType(
        types.PolyModelType(
            model_spec=ValueBase,
        ),
        required=True,
        min_size=2
    )

    def calculate(self):
        r = 1.0
        for a in self.args:
            r *= a.calculate()
        return r


class DivideParams(ParamsBase):
    type = types.StringType(default="divide", required=True)
    args = types.ListType(
        types.PolyModelType(
            model_spec=ValueBase,
        ),
        required=True,
        min_size=2
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
    type = types.StringType(default="power", required=True)
    args = types.ListType(
        types.PolyModelType(
            model_spec=ValueBase,
        ),
        required=True,
        min_size=2
    )

    def calculate(self):
        r = self.args[0].calculate()
        for a in self.args[1:]:
            r **= a.calculate()
        return r


class OperationBase(PolymorphicBase):
    _type_field = "type"
    type = types.StringType(required=True)

    def calculate(self):
        raise NotImplementedError()


class Add(OperationBase):
    type = types.StringType(default="add", required=True)
    params = types.PolyModelType(
        model_spec=ParamsBase,
        required=True
    )

    def calculate(self):
        return self.params.calculate()


class Subtract(OperationBase):
    type = types.StringType(default="subtract", required=True)
    params = types.PolyModelType(
        model_spec=ParamsBase,
        required=True
    )

    def calculate(self):
        return self.params.calculate()


class Multiply(OperationBase):
    type = types.StringType(default="multiply", required=True)
    params = types.PolyModelType(
        model_spec=ParamsBase,
        required=True
    )

    def calculate(self):
        return self.params.calculate()


class Divide(OperationBase):
    type = types.StringType(default="divide", required=True)
    params = types.PolyModelType(
        model_spec=ParamsBase,
        required=True
    )

    def calculate(self):
        return self.params.calculate()


class Power(OperationBase):
    type = types.StringType(default="power", required=True)
    params = types.PolyModelType(
        model_spec=ParamsBase,
        required=True
    )

    def calculate(self):
        return self.params.calculate()


class Expression(ValueBase):
    type = types.StringType(default="expression", required=True)
    expression = types.PolyModelType(
        model_spec=OperationBase,
        required=True,
    )

    def calculate(self):
        return self.expression.calculate()


ValueBase.register("int", IntValue)
ValueBase.register("float", FloatValue)
ValueBase.register("expression", Expression)

ParamsBase.register("add", AddParams)
ParamsBase.register("subtract", SubtractParams)
ParamsBase.register("multiply", MultiplyParams)
ParamsBase.register("divide", DivideParams)
ParamsBase.register("power", PowerParams)

OperationBase.register("add", Add)
OperationBase.register("subtract", Subtract)
OperationBase.register("multiply", Multiply)
OperationBase.register("divide", Divide)
OperationBase.register("power", Power)
