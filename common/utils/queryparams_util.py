from flask import request


def get_bool_from_arg(key: str) -> bool:
    value: str = request.args.get(key, "").strip().lower()
    return value in ["true", "yes", "on", "1"]
