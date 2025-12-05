from schematics import Model, types

class ValueBase(Model):
    def calculate(self):
        raise NotImplementedError()

class OperationBase(Model):
    operation_type = types.StringType(required=True)
    def calculate(self):
        raise NotImplementedError()

class ParamsBase(Model):
    params_type = types.StringType(required=True)

    def calculate(self):
        raise NotImplementedError()