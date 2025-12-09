from schematics import models, types
from schematics.exceptions import ValidationError


class Base(models.Model):
    type = types.StringType(required=True)

    @classmethod
    def _claim_polymorphic(cls, data):
        return data.get('type') == cls.__name__

    def calculate(self, context=None):
        raise NotImplementedError()


class ValueBase(Base):
    pass


class IntValue(ValueBase):
    value = types.FloatType(required=True)

    def calculate(self, context=None):
        return float(self.value)


class FloatValue(ValueBase):
    value = types.FloatType(required=True)

    def calculate(self, context=None):
        return self.value


class Variable(ValueBase):
    name = types.StringType(required=True)

    def calculate(self, context=None):
        context = context or {}
        if self.name not in context:
            raise ValueError(f"Variable '{self.name}' not found in context")
        value = context[self.name]
        if not isinstance(value, (int, float)):
            raise ValueError(f"Variable '{self.name}' must be numeric")
        return float(value)


class Expression(ValueBase):
    expression = types.PolyModelType(model_spec=Base)

    def calculate(self, context=None):
        return self.expression.calculate(context)


class ParamsBase(Base):
    pass


class AddParams(ParamsBase):
    args = types.ListType(
        types.PolyModelType(model_spec=ValueBase),
        required=True,
        min_size=2
    )

    def calculate(self, context=None):
        return sum(arg.calculate(context) for arg in self.args)


class SubtractParams(ParamsBase):
    args = types.ListType(
        types.PolyModelType(model_spec=ValueBase),
        required=True,
        min_size=2
    )

    def calculate(self, context=None):
        result = self.args[0].calculate(context)
        for arg in self.args[1:]:
            result -= arg.calculate(context)
        return result


class MultiplyParams(ParamsBase):
    args = types.ListType(
        types.PolyModelType(model_spec=ValueBase),
        required=True,
        min_size=2
    )

    def calculate(self, context=None):
        result = 1.0
        for arg in self.args:
            result *= arg.calculate(context)
        return result


class DivideParams(ParamsBase):
    args = types.ListType(
        types.PolyModelType(model_spec=ValueBase),
        required=True,
        min_size=2
    )

    def calculate(self, context=None):
        result = self.args[0].calculate(context)
        for arg in self.args[1:]:
            divisor = arg.calculate(context)
            if divisor == 0:
                raise ValueError("Division by zero")
            result /= divisor
        return result


class PowerParams(ParamsBase):
    args = types.ListType(
        types.PolyModelType(model_spec=ValueBase),
        required=True,
        min_size=2
    )

    def calculate(self, context=None):
        result = self.args[0].calculate(context)
        for arg in self.args[1:]:
            result **= arg.calculate(context)
        return result


class OperationBase(Base):
    params = types.PolyModelType(model_spec=ParamsBase)

    def calculate(self, context=None):
        return self.params.calculate(context)


class Add(OperationBase):
    pass


class Subtract(OperationBase):
    pass


class Multiply(OperationBase):
    pass


class Divide(OperationBase):
    pass


class Power(OperationBase):
    pass