import os


def env(name: str) -> str or None:
    return os.environ.get(name, None)
