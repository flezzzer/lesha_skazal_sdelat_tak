# from models.model_registry import init_models
# init_models()

from models import Calculator, ModelFactory

print("Тест 1: 5 + 3 =", Calculator.test_simple())

print("Тест 2: 5 + (3 * 4) =", Calculator.test_nested())

multiply_args = [
    ModelFactory.create_int(7),
    ModelFactory.create_int(7)
]
multiply_op = ModelFactory.create_multiply_operation(multiply_args)
multiply_expr = ModelFactory.create_expression(multiply_op)

power_args = [
    ModelFactory.create_int(7),
    ModelFactory.create_int(2)
]
power_op = ModelFactory.create_power_operation(power_args)
power_expr = ModelFactory.create_expression(power_op)

add_args = [multiply_expr, power_expr]
add_op = ModelFactory.create_add_operation(add_args)

result = Calculator.calculate(add_op)
print(f"Тест 3: (7*7) + (7**2) = {result}")