import time
import random
import sys
import multiprocessing
from multiprocessing import Process, Queue
from models.expression_parser import ExpressionParser
import datetime


def generate_contexts(count=1000, formula_vars=None, seed_offset=0):
    if formula_vars is None:
        formula_vars = {'price': 'float', 'quantity': 'int', 'tax': 'float'}

    random.seed(time.time_ns() + seed_offset)

    contexts = []
    for i in range(count):
        context = {}
        for var_name, var_type in formula_vars.items():
            if var_type == 'int':
                context[var_name] = random.randint(1, 1000)
            elif var_type == 'float':
                context[var_name] = round(random.uniform(1.0, 1000.0), 2)
        contexts.append(context)
    return contexts


def worker_process(worker_id, chunk_size, formula_vars, expr_str, result_queue):
    contexts = generate_contexts(chunk_size, formula_vars, seed_offset=worker_id * 1000)
    model = ExpressionParser.parse(expr_str)

    results = []
    for i, context in enumerate(contexts):
        result = model.calculate(context)
        results.append(result)

    result_queue.put((worker_id, results))


def test_model_factory(formula_vars, expr_str, total_count=10000, num_workers=5):
    chunk_size = total_count // num_workers
    remainder = total_count % num_workers

    print(f"Процессов: {num_workers}")
    print(f"Контекстов всего: {total_count}")

    start_time = time.time()

    result_queue = Queue()
    processes = []

    for i in range(num_workers):
        current_chunk = chunk_size
        if i == num_workers - 1 and remainder > 0:
            current_chunk += remainder

        p = Process(
            target=worker_process,
            args=(i, current_chunk, formula_vars, expr_str, result_queue)
        )
        processes.append(p)
        p.start()

    all_results = []
    worker_results = []

    for _ in range(num_workers):
        worker_id, results = result_queue.get()
        worker_results.append((worker_id, results))
        all_results.extend(results)

    for p in processes:
        p.join()

    end_time = time.time()

    worker_results.sort(key=lambda x: x[0])

    print(f"Время: {end_time - start_time:.3f} сек")
    print(f"Скорость: {total_count / (end_time - start_time):.0f} контекстов/сек")

    unique_all = set(round(r, 4) for r in all_results)
    print(f"Уникальных результатов: {len(unique_all)}")

    print("Примеры (первые 3):")
    for i in range(min(3, len(all_results))):
        print(f"  {i}: {all_results[i]:.2f}")

    return all_results


if __name__ == "__main__":
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
    expr_str = "((price * quantity) / (1 + discount)) + (tax * (quantity / 10)) - shipping"
    start = datetime.datetime.now()
    print("Тест 1: Сложное выражение с вложенными операциями")


    results = test_model_factory(formula_vars, expr_str, 1000000, 5)
    end = datetime.datetime.now()

    print(f"\nОбщее время выполнения: {end - start}")
    print(f"Всего результатов: {len(results)}")