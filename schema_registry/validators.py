import json
from pathlib import Path

import jsonschema


class JSONSchemaValidator:
    def __init__(self, source_name: str, event_type: str, version: int = 1):
        base_path = Path(__file__)
        schema_path = base_path.parent / f"schemas/{source_name}/{event_type}/v{version}.json"
        with open(schema_path, "r") as file:
            schema = json.load(file)
        self.schema = schema

    def is_valid(self, instance) -> bool:
        result = True
        try:
            jsonschema.validate(instance, self.schema)
        except jsonschema.ValidationError as exc:
            # TODO: впендюрить логгер
            print(exc)
            result = False
        finally:
            return result


class UserStreamingSchemaValidator(JSONSchemaValidator):
    def __init__(self, version: int = 1):
        super().__init__(source_name="user", event_type="streaming", version=version)


class UserRoleSchemaValidator(JSONSchemaValidator):
    def __init__(self, version: int = 1):
        super().__init__(source_name="user", event_type="role", version=version)


class TaskStreamingSchemaValidator(JSONSchemaValidator):
    def __init__(self, version: int = 1):
        super().__init__(source_name="task", event_type="streaming", version=version)


class TaskDoneSchemaValidator(JSONSchemaValidator):
    def __init__(self, version: int = 1):
        super().__init__(source_name="task", event_type="done", version=version)
