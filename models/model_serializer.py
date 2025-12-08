import json
from typing import Any, Dict, Optional
from schematics import types


class ModelSerializer:
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