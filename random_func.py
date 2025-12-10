import json
import time
import random
import sys
from models.expression_parser import ExpressionParser


def generate_contexts(count=1000, formula_vars=None):
    if formula_vars is None:
        formula_vars = {'price': 'float', 'quantity': 'int', 'tax': 'float'}

    random.seed(time.time_ns())

    contexts = []
    for i in range(count):
        context = {}
        for var_name, var_type in formula_vars.items():
            if var_type == 'int':
                context[var_name] = random.randint(1, 1000)
            elif var_type == 'float':
                context[var_name] = round(random.uniform(1.0, 1000.0), 2)
            else:
                context[var_name] = random.uniform(1.0, 1000.0)

        contexts.append(context)
    return contexts


def test_model_factory(formula_vars, expr_str, count=1000):
    contexts = generate_contexts(count, formula_vars)

    start_time = time.time()

    results = []
    model = ExpressionParser.parse(expr_str)

    for i, context in enumerate(contexts):
        result = model.calculate(context)
        results.append(result)

        if (i + 1) % 100 == 0:
            sys.stdout.write(f"\r{i + 1}/{len(contexts)}")
            sys.stdout.flush()

    end_time = time.time()

    print(f"\nВремя: {end_time - start_time:.3f} сек")
    print(f"Скорость: {count / (end_time - start_time):.0f} контекстов/сек")

    unique_results = set(round(r, 4) for r in results)
    print(f"Уникальных результатов: {len(unique_results)} из {count}")

    print("\nПримеры (первые 3):")
    for i in range(min(3, len(results))):
        ctx_str = ', '.join(f"{k}={v}" for k, v in contexts[i].items())
        print(f"  {i}: {ctx_str} => {results[i]:.2f}")

    return results
