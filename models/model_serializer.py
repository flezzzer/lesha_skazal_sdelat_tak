import json
from typing import Any, Dict
from schematics import types
from models.models import *

# ЧЕРЕЗ ФАБРИКУ РЕКУРСИВНО
# class ModelSerializer:
#     _TYPE_MAP = {
#         "int": IntValue,
#         "float": FloatValue,
#         "expression": Expression,
#         "add": Add,
#         "subtract": Subtract,
#         "multiply": Multiply,
#         "divide": Divide,
#         "power": Power,
#         "add_params": AddParams,
#         "subtract_params": SubtractParams,
#         "multiply_params": MultiplyParams,
#         "divide_params": DivideParams,
#         "power_params": PowerParams,
#     }
#
#     @staticmethod
#     def to_dict(model_instance) -> Dict[str, Any]:
#         if not hasattr(model_instance, '_data'):
#             return {}
#
#         result = {}
#
#         for field_name, field in model_instance._schema.fields.items():
#             if not hasattr(model_instance, field_name):
#                 continue
#
#             value = getattr(model_instance, field_name)
#
#             if value is None:
#                 continue
#
#             if isinstance(field, types.ListType):
#                 if isinstance(field.field, (types.PolyModelType, types.ModelType)):
#                     result[field_name] = [ModelSerializer.to_dict(item) for item in value]
#                 else:
#                     result[field_name] = value
#
#             elif isinstance(field, (types.PolyModelType, types.ModelType)):
#                 result[field_name] = ModelSerializer.to_dict(value)
#
#             elif isinstance(field, (types.StringType, types.IntType, types.FloatType, types.BooleanType)):
#                 result[field_name] = value
#
#             else:
#                 result[field_name] = value
#
#         return result
#
#     @staticmethod
#     def to_simple_dict(model_instance) -> Dict[str, Any]:
#         result = {}
#
#         if not hasattr(model_instance, '_data'):
#             return result
#
#         model_data = model_instance._data
#
#         for key, value in model_data.items():
#             if value is None:
#                 continue
#
#             if hasattr(value, '_data'):
#                 result[key] = ModelSerializer.to_simple_dict(value)
#
#             elif isinstance(value, list):
#                 result[key] = []
#                 for item in value:
#                     if hasattr(item, '_data'):
#                         result[key].append(ModelSerializer.to_simple_dict(item))
#                     else:
#                         result[key].append(item)
#
#             else:
#                 result[key] = value
#
#         return result
#
#     @classmethod
#     def export(cls, model_instance) -> Dict[str, Any]:
#         try:
#             return model_instance.to_primitive()
#         except Exception:
#             try:
#                 return model_instance.to_native()
#             except Exception:
#                 return cls.to_simple_dict(model_instance)
#
#     @classmethod
#     def to_json(cls, model_instance, indent: int = 2, **kwargs) -> str:
#         data = cls.export(model_instance)
#         default_kwargs = {
#             'indent': indent,
#             'ensure_ascii': False,
#             'sort_keys': True
#         }
#         default_kwargs.update(kwargs)
#         return json.dumps(data, **default_kwargs)
#
#     @classmethod
#     def save_to_file(cls, model_instance, filepath: str, indent: int = 2, **kwargs):
#         json_str = cls.to_json(model_instance, indent, **kwargs)
#         with open(filepath, 'w', encoding='utf-8') as f:
#             f.write(json_str)
#
#     @staticmethod
#     def validate_and_serialize(model_instance) -> Dict[str, Any]:
#         model_instance.validate()
#         return ModelSerializer.export(model_instance)
#
#     @classmethod
#     def create_from_json(cls, json_str: str, model_class) -> Any:
#         data = json.loads(json_str)
#         return cls._create_recursive(data, model_class)
#
#     @classmethod
#     def create_from_dict(cls, data: Dict[str, Any], model_class) -> Any:
#         return cls._create_recursive(data, model_class)
#
#     @classmethod
#     def load_from_file(cls, filepath: str, model_class) -> Any:
#         with open(filepath, 'r', encoding='utf-8') as f:
#             json_str = f.read()
#         return cls.create_from_json(json_str, model_class)
#
#     @classmethod
#     def _create_recursive(cls, data: Any, model_class=None, depth=0) -> Any:
#         if hasattr(data, '_data'):
#             return data
#
#         if isinstance(data, dict):
#             if 'type' in data:
#                 type_name = data['type']
#                 actual_class = cls._TYPE_MAP.get(type_name)
#
#                 if actual_class:
#                     if type_name == 'expression' and 'expression' in data:
#                         from .model_factory import ModelFactory
#                         inner_op = cls._create_recursive(data['expression'])
#                         return ModelFactory.create_expression(inner_op)
#
#                     elif type_name in ['add', 'subtract', 'multiply', 'divide', 'power']:
#                         from .model_factory import ModelFactory
#
#                         if 'params' in data:
#                             params_data = data['params']
#                             if isinstance(params_data, dict) and 'args' in params_data:
#                                 args_data = params_data['args']
#                                 processed_args = cls._create_recursive(args_data)
#
#                                 if type_name == 'add':
#                                     return ModelFactory.create_add_operation(processed_args)
#                                 elif type_name == 'subtract':
#                                     return ModelFactory.create_subtract_operation(processed_args)
#                                 elif type_name == 'multiply':
#                                     return ModelFactory.create_multiply_operation(processed_args)
#                                 elif type_name == 'divide':
#                                     return ModelFactory.create_divide_operation(processed_args)
#                                 elif type_name == 'power':
#                                     return ModelFactory.create_power_operation(processed_args)
#
#                     processed_data = {}
#                     for key, value in data.items():
#                         if key == 'type':
#                             processed_data[key] = value
#                         else:
#                             processed_data[key] = cls._create_recursive(value)
#
#                     instance = actual_class(processed_data, strict=False, validate=False)
#                     try:
#                         instance.validate()
#                     except:
#                         pass
#                     return instance
#
#             if model_class:
#                 processed_data = {}
#                 for key, value in data.items():
#                     processed_data[key] = cls._create_recursive(value)
#
#                 instance = model_class(processed_data, strict=False, validate=False)
#                 try:
#                     instance.validate()
#                 except:
#                     pass
#                 return instance
#
#         elif isinstance(data, list):
#             return [cls._create_recursive(item) for item in data]
#
#         return data

 # РЕКУРСИВНО ЧЕРЕЗ МОДЕЛИ

class ModelSerializer:
    _TYPE_MAP = {
        "int": IntValue,
        "float": FloatValue,
        "expression": Expression,
        "add": Add,
        "subtract": Subtract,
        "multiply": Multiply,
        "divide": Divide,
        "power": Power,
        "add_params": AddParams,
        "subtract_params": SubtractParams,
        "multiply_params": MultiplyParams,
        "divide_params": DivideParams,
        "power_params": PowerParams,
    }

    @staticmethod
    def to_dict(model_instance) -> Dict[str, Any]:
        if not hasattr(model_instance, '_data'):
            return {}

        result = {}

        for field_name, field in model_instance._schema.fields.items():
            if not hasattr(model_instance, field_name):
                continue

            value = getattr(model_instance, field_name)

            if value is None:
                continue

            if isinstance(field, types.ListType):
                if isinstance(field.field, (types.PolyModelType, types.ModelType)):
                    result[field_name] = [ModelSerializer.to_dict(item) for item in value]
                else:
                    result[field_name] = value

            elif isinstance(field, (types.PolyModelType, types.ModelType)):
                result[field_name] = ModelSerializer.to_dict(value)

            elif isinstance(field, (types.StringType, types.IntType, types.FloatType, types.BooleanType)):
                result[field_name] = value

            else:
                result[field_name] = value

        return result

    @staticmethod
    def to_simple_dict(model_instance) -> Dict[str, Any]:
        result = {}

        if not hasattr(model_instance, '_data'):
            return result

        model_data = model_instance._data

        for key, value in model_data.items():
            if value is None:
                continue

            if hasattr(value, '_data'):
                result[key] = ModelSerializer.to_simple_dict(value)

            elif isinstance(value, list):
                result[key] = []
                for item in value:
                    if hasattr(item, '_data'):
                        result[key].append(ModelSerializer.to_simple_dict(item))
                    else:
                        result[key].append(item)

            else:
                result[key] = value

        return result

    @classmethod
    def export(cls, model_instance) -> Dict[str, Any]:
        try:
            return model_instance.to_primitive()
        except Exception:
            try:
                return model_instance.to_native()
            except Exception:
                return cls.to_simple_dict(model_instance)

    @classmethod
    def to_json(cls, model_instance, indent: int = 2, **kwargs) -> str:
        data = cls.export(model_instance)
        default_kwargs = {
            'indent': indent,
            'ensure_ascii': False,
            'sort_keys': True
        }
        default_kwargs.update(kwargs)
        return json.dumps(data, **default_kwargs)

    @classmethod
    def save_to_file(cls, model_instance, filepath: str, indent: int = 2, **kwargs):
        json_str = cls.to_json(model_instance, indent, **kwargs)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(json_str)

    @staticmethod
    def validate_and_serialize(model_instance) -> Dict[str, Any]:
        model_instance.validate()
        return ModelSerializer.export(model_instance)

    @classmethod
    def create_from_json(cls, json_str: str, model_class=None) -> Any:
        data = json.loads(json_str)
        return cls._create_recursive(data)

    @classmethod
    def create_from_dict(cls, data: Dict[str, Any], model_class=None) -> Any:
        return cls._create_recursive(data)

    @classmethod
    def load_from_file(cls, filepath: str, model_class=None) -> Any:
        with open(filepath, 'r', encoding='utf-8') as f:
            json_str = f.read()
        return cls.create_from_json(json_str, model_class)

    @classmethod
    def _create_recursive(cls, data: Any) -> Any:
        if hasattr(data, '_data'):
            return data

        if isinstance(data, dict):
            if 'type' in data:
                type_name = data['type']
                actual_class = cls._TYPE_MAP.get(type_name)

                if not actual_class:
                    raise ValueError(f"Unknown type: {type_name}")

                processed_data = {}
                for key, value in data.items():
                    if key == 'type':
                        processed_data[key] = value
                    elif isinstance(value, dict):
                        processed_data[key] = cls._create_recursive(value)
                    elif isinstance(value, list):
                        processed_data[key] = [cls._create_recursive(item) for item in value]
                    else:
                        processed_data[key] = value

                return actual_class(processed_data)

        elif isinstance(data, list):
            return [cls._create_recursive(item) for item in data]

        return data