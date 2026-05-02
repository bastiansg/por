import json


def get_pretty(
    obj: dict | list[dict],
    indent: int = 4,
    ensure_ascii: bool = False,
) -> str:
    return json.dumps(
        obj,
        indent=indent,
        ensure_ascii=ensure_ascii,
    )


def save_json(
    obj: dict | list[dict],
    file_path: str,
    indent: int = 4,
) -> None:
    with open(file_path, "w") as f:
        f.write(get_pretty(obj=obj, indent=indent))


def load_json(json_file_path: str) -> dict | list[dict]:
    with open(json_file_path, "r") as f:
        return json.loads(f.read())
