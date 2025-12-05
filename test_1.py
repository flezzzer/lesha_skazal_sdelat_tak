from schematics import Model, types
from schematics.exceptions import ValidationError, DataError


# ==================== БАЗОВЫЕ КЛАССЫ ====================
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


# ==================== ПРОСТЫЕ VALUE-КЛАССЫ ====================
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


# ==================== ФУНКЦИИ CLAIM ====================
def value_claim_function(field_instance, data):
    """Определяет, какой Value-класс использовать на основе value_type"""
    value_type = data.get('value_type')
    if value_type == 'valueint':
        return ValueInt
    if value_type == 'valuefloat':
        return ValueFloat
    if value_type == 'valueexpression':
        return ValueExpression  # Будет определен позже
    return None


def operation_claim_function(field_instance, data):
    """Определяет, какой Operation-класс использовать на основе operation_type"""
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


# ==================== PARAMS КЛАССЫ (определяем сначала без args) ====================
class AddParams(ParamsBase):
    params_type = types.StringType(default='addparams', required=True)

    # args определим позже

    def calculate(self):
        return sum(arg.calculate() for arg in self.args)


class SubtractParams(ParamsBase):
    params_type = types.StringType(default='subtractparams', required=True)

    # args определим позже

    def calculate(self):
        if not self.args:
            return 0.0
        result = self.args[0].calculate()
        for arg in self.args[1:]:
            result -= arg.calculate()
        return result


class MultiplyParams(ParamsBase):
    params_type = types.StringType(default='multiplyparams', required=True)

    # args определим позже

    def calculate(self):
        result = 1.0
        for arg in self.args:
            result *= arg.calculate()
        return result


class DivideParams(ParamsBase):
    params_type = types.StringType(default='divideparams', required=True)

    # args определим позже

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

    # args определим позже

    def calculate(self):
        if not self.args:
            return 0.0
        result = self.args[0].calculate()
        for arg in self.args[1:]:
            result **= arg.calculate()
        return result


# ==================== OPERATION КЛАССЫ ====================
class AddOperation(OperationBase):
    operation_type = types.StringType(default='addoperation', required=True)
    # Временно используем ModelType вместо конкретного класса
    params = types.ListType(types.ModelType('AddParams'), required=True, min_size=1)

    def calculate(self):
        if not self.params:
            return 0.0
        return self.params[0].calculate()


class SubtractOperation(OperationBase):
    operation_type = types.StringType(default='subtractoperation', required=True)
    params = types.ListType(types.ModelType('SubtractParams'), required=True, min_size=1)

    def calculate(self):
        if not self.params:
            return 0.0
        return self.params[0].calculate()


class MultiplyOperation(OperationBase):
    operation_type = types.StringType(default='multiplyoperation', required=True)
    params = types.ListType(types.ModelType('MultiplyParams'), required=True, min_size=1)

    def calculate(self):
        if not self.params:
            return 0.0
        return self.params[0].calculate()


class DivideOperation(OperationBase):
    operation_type = types.StringType(default='divideoperation', required=True)
    params = types.ListType(types.ModelType('DivideParams'), required=True, min_size=1)

    def calculate(self):
        if not self.params:
            return 0.0
        return self.params[0].calculate()


class PowerOperation(OperationBase):
    operation_type = types.StringType(default='poweroperation', required=True)
    params = types.ListType(types.ModelType('PowerParams'), required=True, min_size=1)

    def calculate(self):
        if not self.params:
            return 0.0
        return self.params[0].calculate()


# ==================== СЛОЖНЫЙ VALUE-КЛАСС ====================
class ValueExpression(ValueBase):
    value_type = types.StringType(default='valueexpression', required=True)
    expression = types.PolyModelType(
        model_spec=[
            'AddOperation',
            'SubtractOperation',
            'MultiplyOperation',
            'DivideOperation',
            'PowerOperation'
        ],
        claim_function=operation_claim_function,
        required=True
    )

    def calculate(self):
        return self.expression.calculate()


# ==================== СОЗДАЕМ ArgsPolyList ПОСЛЕ ОПРЕДЕЛЕНИЯ ВСЕХ КЛАССОВ ====================
# Используем строки вместо классов для избежания циклических зависимостей
ValuePolyType = types.PolyModelType(
    model_spec=[
        'ValueInt',
        'ValueFloat',
        'ValueExpression'
    ],
    claim_function=value_claim_function
)

# Создаем ListType - здесь важно передать ОБЪЕКТ ValuePolyType
ArgsPolyList = types.ListType(ValuePolyType, required=True, min_size=1)

# Теперь добавляем args во все Params-классы
for params_class in [AddParams, SubtractParams, MultiplyParams, DivideParams, PowerParams]:
    params_class._fields['args'] = ArgsPolyList

# ==================== ПРОСТОЙ ТЕСТ ====================
if __name__ == "__main__":
    print("=== Простой тест ===")

    try:
        # Создаем ValueInt
        val_int = ValueInt({
            'value_type': 'valueint',
            'value': 10
        })
        val_int.validate()
        print(f"✓ ValueInt создан: {val_int.calculate()}")

        # Создаем ValueFloat
        val_float = ValueFloat({
            'value_type': 'valuefloat',
            'value': 3.5
        })
        val_float.validate()
        print(f"✓ ValueFloat создан: {val_float.calculate()}")

        # Создаем AddParams
        add_params = AddParams({
            'params_type': 'addparams',
            'args': [
                {'value_type': 'valueint', 'value': 5},
                {'value_type': 'valuefloat', 'value': 2.5}
            ]
        })
        add_params.validate()
        print(f"✓ AddParams создан")
        print(f"  args: {add_params.args}")
        print(f"  calculate: {add_params.calculate()}")

        # Создаем AddOperation
        add_op = AddOperation({
            'operation_type': 'addoperation',
            'params': [{
                'params_type': 'addparams',
                'args': [
                    {'value_type': 'valueint', 'value': 3},
                    {'value_type': 'valueint', 'value': 4}
                ]
            }]
        })
        add_op.validate()
        print(f"✓ AddOperation создан")
        print(f"  calculate: {add_op.calculate()}")

        # Создаем ValueExpression
        expr = ValueExpression({
            'value_type': 'valueexpression',
            'expression': {
                'operation_type': 'addoperation',
                'params': [{
                    'params_type': 'addparams',
                    'args': [
                        {'value_type': 'valueint', 'value': 7},
                        {'value_type': 'valueint', 'value': 8}
                    ]
                }]
            }
        })
        expr.validate()
        print(f"✓ ValueExpression создан")
        print(f"  calculate: {expr.calculate()}")

    except Exception as e:
        print(f"✗ Ошибка: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()