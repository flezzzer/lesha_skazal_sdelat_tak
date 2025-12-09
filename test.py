from models import OperationBase, ModelFactory
from models.calculator import Calculator
from models.expression_parser import ExpressionParser
from models.model_serializer import ModelSerializer
from models.models import Expression
import json

# expr = "5+(3*4)*3+2-(35-(6-2+(3-2)))"
# expr = "(3+3+3+4)"
# res_expr = float(3+3+3+4)
# model = ExpressionParser.parse(expr)
# result = model.calculate()
# json_test = """
# {
#     "type": "Expression",
#     "expression": {
#         "type": "Add",
#         "params": {
#             "type": "AddParams",
#             "args": [
#                 {
#                     "type": "IntValue",
#                     "value": 10
#                 },
#                 {
#                     "type": "FloatValue",
#                     "value": 3.5
#                 },
#                 {
#                     "type": "Expression",
#                     "expression": {
#                         "type": "Multiply",
#                         "params": {
#                             "type": "MultiplyParams",
#                             "args": [
#                                 {
#                                     "type": "IntValue",
#                                     "value": 2
#                                 },
#                                 {
#                                     "type": "FloatValue",
#                                     "value": 4.0
#                                 }
#                             ]
#                         }
#                     }
#                 }
#             ]
#         }
#     }
# }
# """
#
# res_json = ModelSerializer.to_json(model)
#
# print("Result:", result, res_expr, f"{res_expr==result}")
# print (res_json)
# model_new = ModelSerializer.create_from_json(json_test)
# model_new_json = ModelSerializer.to_json(model_new)
#
# model_test_json_after_res = ModelSerializer.create_from_json(res_json)
# print(model_test_json_after_res.calculate())
# print(model_new.calculate())
#
# print(model_new_json)
import datetime
start = datetime.datetime.now()
expr = "price * quantity + tax"
model = ExpressionParser.parse(expr)
end = datetime.datetime.now()
print(end-start)

context = {'price': 100, 'quantity': 5, 'tax': 20}
result = model.calculate(context)
print(f"Result: {result}")  # 100 * 5 + 20 = 520

context2 = {'price': 50, 'quantity': 10, 'tax': 30}
result2 = model.calculate(context2)
print(f"New result: {result2}")  # 50 * 10 + 30 = 530

from models.model_serializer import ModelSerializer
json_str = ModelSerializer.to_json(model)
print(json_str)
model_restored = ModelSerializer.create_from_json(json_str)

result3 = model_restored.calculate(context)
print(f"Restored result: {result3}")  # 520



add_op = ModelFactory.create_operation('add', [10, 20, 30])
json_add_op = ModelSerializer.to_json(add_op)
print(json_add_op)
# add_op = ModelFactory.create_add_operation([10, 20, 30])

expr = ModelFactory.create_expression(add_op)


context = {'x': 5, 'y': 10}
result = expr.calculate(context)
print(f"Result: {result}")

