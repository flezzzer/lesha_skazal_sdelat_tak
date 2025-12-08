from models import OperationBase
from models.calculator import Calculator
from models.expression_parser import ExpressionParser
from models.model_serializer import ModelSerializer
from models.models import Expression
import json

# expr = "5+(3*4)*3+2-(35-(6-2+(3-2)))"
expr = "(5+(3*4)*3+2-(35-(6-2+(4-2)**3))-1+(7+8))"
res_expr = float(5+(3*4)*3+2-(35-(6-2+(4-2)**3))-1+(7+8))
model = ExpressionParser.parse(expr)
result = model.calculate()
json_test = """
{
    "type": "expression",
    "expression": {
        "type": "add",
        "params": {
            "type": "add_params",
            "args": [
                {
                    "type": "int",
                    "value": 10
                },
                {
                    "type": "float",
                    "value": 3.5
                },
                {
                    "type": "expression",
                    "expression": {
                        "type": "multiply",
                        "params": {
                            "type": "multiply_params",
                            "args": [
                                {
                                    "type": "int",
                                    "value": 2
                                },
                                {
                                    "type": "float",
                                    "value": 4.0
                                }
                            ]
                        }
                    }
                }
            ]
        }
    }
}
"""
# model = ModelSerializer.create_from_json()
res_json = ModelSerializer.to_json(model)
# print(res_json)
# print("Result:", result, res_expr, f"{res_expr==result}")
model_new = ModelSerializer.create_from_json(json_test, Expression)
print(model_new.calculate())
model_json = ModelSerializer.create_from_json(json_test, Expression)
print(model_new)

