from typing import Any, Dict
import json
from models.models import *
import typing
import math

class ModelSerializer:
    @classmethod
    def create_from_json(cls, json_str: str) -> Any:
        data = json.loads(json_str)
        return Expression(data)

    @classmethod
    def create_from_dict(cls, data: Dict[str, Any]) -> Any:
        return Expression(data)

    @classmethod
    def to_json(cls, model_instance, indent: int = 2) -> str:
        return json.dumps(cls._extract(model_instance), indent=indent, ensure_ascii=False)

    @classmethod
    def _extract(cls, obj):
        if isinstance(obj, list):
            return [cls._extract(x) for x in obj]
        elif hasattr(obj, '_data'):
            return {k: cls._extract(v) for k, v in obj._data.items() if v is not None}
        else:
            return obj

    @classmethod
    def load_from_file(cls, filepath: str) -> Any:
        with open(filepath, 'r', encoding='utf-8') as f:
            return cls.create_from_json(f.read())


    @staticmethod
    def create_from_file(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                contexts = json.load(f)
        except Exception as e:
            raise ValueError(f"Error loading contexts from file: {str(e)}")

        if not isinstance(contexts, list):
            contexts = [contexts]

        return contexts
