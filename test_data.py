from models import OperationBase, ModelFactory
from models.calculator import Calculator
from models.expression_parser import ExpressionParser
from models.model_serializer import ModelSerializer
from random_func import *


import datetime
start = datetime.datetime.now()
expr = "price * quantity + tax"
model = ExpressionParser.parse(expr)
end = datetime.datetime.now()
print(end-start)

file_ctx = ModelSerializer().create_from_file('test_data.txt')
test_factory = ModelFactory().calcualte_big_context_func(model, file_ctx)
print(len(test_factory), test_factory)

formula_vars = {
    'price': 'float',
    'quantity': 'int',
    'tax': 'float',
    'discount': 'float',
    'shipping': 'float',
    'weight': 'float',
    'height': 'float',
    'width': 'float',
    'depth': 'float'
}

start = datetime.datetime.now()
print("Тест 1: Сложное выражение с вложенными операциями")
expr_str1 = "((price * quantity) / (1 + discount)) + (tax * (quantity / 10)) - shipping"
results1 = test_model_factory(formula_vars, expr_str1, 1000000)
end = datetime.datetime.now()
print(f"Время 1 теста {end - start}\n")

start = datetime.datetime.now()
print("\nТест 2: Экстремально сложное выражение")
expr_str2 = "(price * (quantity ** 1.1)) + (tax / (1 + discount)) - (shipping * 0.8) + ((weight * height) / 100) - (price * discount ** 2)"
results2 = test_model_factory(formula_vars, expr_str2, 1000000)
end = datetime.datetime.now()
print(f"Время 2 теста {end - start}\n")

start = datetime.datetime.now()
print("\nТест 3: Многоуровневое выражение")
expr_str3 = "((((price + tax) * quantity) - (price * discount)) / (1 + shipping/100)) * (weight/height) + (width * depth) ** 0.5"
results3 = test_model_factory(formula_vars, expr_str3, 1000000)
end = datetime.datetime.now()
print(f"Время 3 теста {end - start}\n")

# start = datetime.datetime.now()
# print("\nТест 4: Степени и корни")
# expr_str4 = "(price ** 1.5) + (quantity ** 0.7) - (tax ** (1 + discount)) + ((weight * height * width) ** (1/3))"
# results4 = test_model_factory(formula_vars, expr_str4, 1000)
# end = datetime.datetime.now()
# print(f"Время 4 теста {end - start}\n")

start = datetime.datetime.now()
print("\nТест 5: Максимально сложная формула")
expr_str5 = "((price * quantity * (1 - discount) ** 2) + (tax / (quantity + 1)) * (1 + shipping/price)) ** (1/(1 + discount)) - ((weight + height + width) / 3) * 0.15"
results5 = test_model_factory(formula_vars, expr_str5, 1000000)
end = datetime.datetime.now()
print(f"Время 5 теста {end - start}\n")

