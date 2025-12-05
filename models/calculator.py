from models.model_factory import ModelFactory


class Calculator:
    @staticmethod
    def calculate(operation):
        operation.validate()
        return operation.calculate()

    @staticmethod
    def test_simple():
        args = [
            ModelFactory.create_int(5),
            ModelFactory.create_int(3)
        ]
        op = ModelFactory.create_add_operation(args)
        return Calculator.calculate(op)

    @staticmethod
    def test_nested():
        multiply_args = [
            ModelFactory.create_int(3),
            ModelFactory.create_int(4)
        ]
        multiply_op = ModelFactory.create_multiply_operation(multiply_args)
        multiply_expr = ModelFactory.create_expression(multiply_op)
        add_args = [
            ModelFactory.create_int(5),
            multiply_expr
        ]
        add_op = ModelFactory.create_add_operation(add_args)
        return Calculator.calculate(add_op)