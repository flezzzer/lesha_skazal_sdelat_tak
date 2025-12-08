import json
from typing import Any, Dict
from models.models import *


class ModelSerializer:
    @classmethod
    def create_from_json(cls, json_str: str) -> Any:
        data = json.loads(json_str)
        return cls._build(data)

    @classmethod
    def _build(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'type' not in data:
                return data

            type_name = data['type']

            if type_name in ['int', 'float']:
                if type_name == 'int':
                    return IntValue(data)
                else:
                    return FloatValue(data)

            processed = {}
            for key, value in data.items():
                if key == 'type':
                    processed[key] = value
                elif isinstance(value, (dict, list)):
                    processed[key] = cls._build(value)
                else:
                    processed[key] = value

            if type_name == 'expression':
                return Expression(processed)
            elif type_name in ['add', 'subtract', 'multiply', 'divide', 'power']:
                return OperationBase._claim(None, processed)(processed)
            elif type_name.endswith('_params'):
                return ParamsBase._claim(None, processed)(processed)
            else:
                return ValueBase._claim(None, processed)(processed)

        elif isinstance(data, list):
            return [cls._build(item) for item in data]

        return data

    @classmethod
    def to_json(cls, model_instance, indent: int = 2) -> str:
        data = cls._extract(model_instance)
        return json.dumps(data, indent=indent, ensure_ascii=False)

    @classmethod
    def _extract(cls, model_instance) -> Any:
        if not hasattr(model_instance, '_data'):
            return model_instance

        result = {}
        for key, value in model_instance._data.items():
            if value is None:
                continue

            if hasattr(value, '_data'):
                result[key] = cls._extract(value)
            elif isinstance(value, list):
                result[key] = [cls._extract(item) if hasattr(item, '_data') else item for item in value]
            else:
                result[key] = value

        return result

    @classmethod
    def create_from_dict(cls, data: Dict[str, Any]) -> Any:
        return cls._build(data)

    @classmethod
    def load_from_file(cls, filepath: str) -> Any:
        with open(filepath, 'r', encoding='utf-8') as f:
            json_str = f.read()
        return cls.create_from_json(json_str)