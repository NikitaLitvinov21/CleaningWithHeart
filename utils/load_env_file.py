from os import environ


def load_env_file(filepath=".env"):
    with open(filepath) as f:
        for line in f:
            # Remove comments and empty lines!
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split as "KEY=VALUE"
            key, value = line.split("=", 1)
            environ[key] = value


load_env_file()
