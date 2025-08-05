import tomllib


def load_config(file_name):
    with open(file_name, "rb") as f:
        config = tomllib.load(f)

    return config


config = load_config("config.toml")
