from .model_factory import ModelFactory

class Calculator:
    @staticmethod
    def calculate(operation):
        operation.validate()
        return operation.calculate()


    # @staticmethod
    # def test_simple():
    #     args = [
    #         ModelFactory.create_int(5),
    #         ModelFactory.create_int(3)
    #     ]
    #     op = ModelFactory.create_add_operation(args)
    #     return Calculator.calculate(op)
    #
    # @staticmethod
    # def test_nested():
    #     multiply_args = [
    #         ModelFactory.create_int(3),
    #         ModelFactory.create_int(4)
    #     ]
    #     multiply_op = ModelFactory.create_multiply_operation(multiply_args)
    #     multiply_expr = ModelFactory.create_expression(multiply_op)
    #
    #     add_args = [
    #         ModelFactory.create_int(5),
    #         multiply_expr
    #     ]
    #     add_op = ModelFactory.create_add_operation(add_args)
    #     return Calculator.calculate(add_op)
    #
    # @staticmethod
    # def test_complex():
    #     multiply_args = [
    #         ModelFactory.create_int(7),
    #         ModelFactory.create_int(7)
    #     ]
    #     multiply_op = ModelFactory.create_multiply_operation(multiply_args)
    #     multiply_expr = ModelFactory.create_expression(multiply_op)
    #
    #     power_args = [
    #         ModelFactory.create_int(7),
    #         ModelFactory.create_int(2)
    #     ]
    #     power_op = ModelFactory.create_power_operation(power_args)
    #     power_expr = ModelFactory.create_expression(power_op)
    #
    #     add_args = [
    #         multiply_expr,
    #         power_expr
    #     ]
    #     add_op = ModelFactory.create_add_operation(add_args)
    #     return Calculator.calculate(add_op)
