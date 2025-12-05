from models.calculator import Calculator
from models.expression_parser import ExpressionParser
import json

# expr = "5+(3*4)*3+2-(35-(6-2+(3-2)))"
expr = "5+(3*4)*3+2-(35-(6-2+(3-2)))"
res_expr = 5+(3*4)*3+2-(35-(6-2+(3-2)))
model = ExpressionParser.parse(expr)
result = model.calculate()
print("Result:", result, res_expr)  # 17.0
