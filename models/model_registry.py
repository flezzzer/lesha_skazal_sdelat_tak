
from schematics import types

def init_models():
    from models.value_models import ValueInt, ValueFloat, ValueExpression
    from models.operation_models import AddOperation, SubtractOperation, MultiplyOperation, DivideOperation, PowerOperation
    from models.params_models import AddParams, SubtractParams, MultiplyParams, DivideParams, PowerParams

    all_operations = [AddOperation, SubtractOperation, MultiplyOperation, DivideOperation, PowerOperation]

    def operation_claim_function(field_instance, data):
        op_type = data.get('operation_type')
        if op_type == 'addoperation':
            return AddOperation
        if op_type == 'subtractoperation':
            return SubtractOperation
        if op_type == 'multiplyoperation':
            return MultiplyOperation
        if op_type == 'divideoperation':
            return DivideOperation
        if op_type == 'poweroperation':
            return PowerOperation
        return None

    def params_claim_function(field_instance, data):
        params_type = data.get('params_type')
        if params_type == 'addparams':
            return AddParams
        if params_type == 'subtractparams':
            return SubtractParams
        if params_type == 'multiplyparams':
            return MultiplyParams
        if params_type == 'divideparams':
            return DivideParams
        if params_type == 'powerparams':
            return PowerParams
        return None


    ValueExpression._fields['expression'] = types.PolyModelType(
        model_spec=all_operations,
        claim_function=operation_claim_function,
        required=True
    )

    def value_expression_calculate(self):
        return self.expression.calculate()

    ValueExpression.calculate = value_expression_calculate

    operation_params_map = {
        AddOperation: AddParams,
        SubtractOperation: SubtractParams,
        MultiplyOperation: MultiplyParams,
        DivideOperation: DivideParams,
        PowerOperation: PowerParams
    }
    #
    # for operation_class, params_class in operation_params_map.items():
    #     if 'params' not in operation_class._fields:
    #         operation_class._fields['params'] = types.ListType(
    #             types.ModelType(params_class),
    #             required=True,
    #             min_size=1
    #         )

    def operation_calculate(self):
        if not self.params:
            return 0.0
        return self.params[0].calculate()

    for op_class in all_operations:
        op_class.calculate = operation_calculate