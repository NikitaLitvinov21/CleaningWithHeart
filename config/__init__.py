from dotenv import load_dotenv
from pyaml_env import parse_config

load_dotenv()


def get_config(key: str) -> dict:
    return parse_config(path="./config/app.yaml")[key]


if __name__ == "__main__":
    print(get_config("database"))
