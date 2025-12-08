import json
from typing import Any, Dict
from models.models import *


class ModelSerializer:
    @classmethod
    def _build(cls, data):
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, (dict, list)):
                    data[k] = cls._build(v)
            if 'type' in data:
                base_cls = ValueBase._registry.get(data['type']) or \
                           ParamsBase._registry.get(data['type']) or \
                           OperationBase._registry.get(data['type']) or \
                           ValueBase
                return base_cls(data)
            return data
        elif isinstance(data, list):
            return [cls._build(x) for x in data]
        return data

    @classmethod
    def create_from_json(cls, json_str):
        data = json.loads(json_str)
        return cls._build(data)

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