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
    "type": "Expression",
    "expression": {
        "type": "Add",
        "params": {
            "type": "AddParams",
            "args": [
                {
                    "type": "IntValue",
                    "value": 10
                },
                {
                    "type": "FloatValue",
                    "value": 3.5
                },
                {
                    "type": "Expression",
                    "expression": {
                        "type": "Multiply",
                        "params": {
                            "type": "MultiplyParams",
                            "args": [
                                {
                                    "type": "IntValue",
                                    "value": 2
                                },
                                {
                                    "type": "FloatValue",
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

res_json = ModelSerializer.to_json(model)

print("Result:", result, res_expr, f"{res_expr==result}")

model_new = ModelSerializer.create_from_json(json_test)
model_new_json = ModelSerializer.to_json(model_new)

model_test_json_after_res = ModelSerializer.create_from_json(res_json)
print(model_test_json_after_res.calculate())
print(model_new.calculate())

print(model_new_json)

