import json


class JsonService:
    """JSON file load/save and pretty-print helpers."""

    @staticmethod
    def load(path: str):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def save(path: str, data) -> str:
        if not path.lower().endswith(".json"):
            path = f"{path}.json"

        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return path

    @staticmethod
    def dumps(data) -> str:
        return json.dumps(data, indent=4, ensure_ascii=False)
