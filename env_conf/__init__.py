from .provider import EnvProvider, Field

VERSION = (0, 1, 0)


def get_version():
    return "{}.{}.{}".format(*VERSION)

__all__ = ['EnvProvider', 'Field', 'get_version']
