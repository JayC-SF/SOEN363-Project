import json
from typing import Type, TypeVar, Any, Dict

T = TypeVar('T')


class JsonToObjectMapper:
    def __init__(self, mapping: Dict[str, str]):
        """
        Initialize the mapper with a specific mapping.

        :param mapping: A dictionary representing the mapping from object attributes to JSON paths.
        """
        self.mapping = mapping

    def map(self, json_data: str | Dict[str, Any], cls: Type[T]) -> T:
        """
        Maps JSON data to an object of the specified class based on the provided mapping.

        :param json_data: A string containing JSON or a dictionary representing an object.
        :param cls: The class type to which the JSON data is to be mapped.
        :return: An instance of cls filled with data from the json_data.
        """
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data

        # Process each mapping and extract the corresponding value from JSON.
        obj_data = {}
        for attr, json_path in self.mapping.items():
            keys = json_path.split('.')
            value = data
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    value = None
                    break
            obj_data[attr] = value

        obj = cls(**obj_data)
        return obj
