from schematics import models, types
from schematics.exceptions import ValidationError


class Base(models.Model):
    type = types.StringType(required=True)

    @classmethod
    def _claim_polymorphic(cls, data):
        return data.get('type') == cls.__name__


class ValueBase(Base):

    def calculate(self):
        raise NotImplementedError()


class IntValue(ValueBase):
    value = types.FloatType(required=True)

    def calculate(self):
        return float(self.value)


class FloatValue(ValueBase):
    value = types.FloatType(required=True)

    def calculate(self):
        return self.value


class Expression(ValueBase):
    expression = types.PolyModelType(model_spec=Base)

    def calculate(self):
        return self.expression.calculate()


class ParamsBase(Base):

    def calculate(self):
        raise NotImplementedError()


class AddParams(ParamsBase):
    args = types.ListType(
        types.PolyModelType(model_spec=ValueBase),
        required=True,
        min_size=2
    )

    def calculate(self):
        return sum(arg.calculate() for arg in self.args)


class SubtractParams(ParamsBase):
    args = types.ListType(
        types.PolyModelType(model_spec=ValueBase),
        required=True,
        min_size=2
    )

    def calculate(self):
        result = self.args[0].calculate()
        for arg in self.args[1:]:
            result -= arg.calculate()
        return result


class MultiplyParams(ParamsBase):
    args = types.ListType(
        types.PolyModelType(model_spec=ValueBase),
        required=True,
        min_size=2
    )

    def calculate(self):
        result = 1.0
        for arg in self.args:
            result *= arg.calculate()
        return result


class DivideParams(ParamsBase):
    args = types.ListType(
        types.PolyModelType(model_spec=ValueBase),
        required=True,
        min_size=2
    )

    def calculate(self):
        result = self.args[0].calculate()
        for arg in self.args[1:]:
            divisor = arg.calculate()
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

    def calculate(self):
        result = self.args[0].calculate()
        for arg in self.args[1:]:
            result **= arg.calculate()
        return result


class OperationBase(Base):
    params = types.PolyModelType(model_spec=ParamsBase)

    def calculate(self):
        return self.params.calculate()


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