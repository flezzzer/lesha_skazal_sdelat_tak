from models.calculator import Calculator
from models.expression_parser import ExpressionParser
from models.model_serializer import ModelSerializer
import json

# expr = "5+(3*4)*3+2-(35-(6-2+(3-2)))"
expr = "(5+(3*4)*3+2-(35-(6-2+(4-2)**3))-1+(7+8))"
res_expr = float(5+(3*4)*3+2-(35-(6-2+(4-2)**3))-1+(7+8))
model = ExpressionParser.parse(expr)
result = model.calculate()
print(ModelSerializer.to_json(model))
print("Result:", result, res_expr, f"{res_expr==result}")
