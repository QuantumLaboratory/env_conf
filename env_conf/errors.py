class InvalidConfigError(ValueError):
    pass


class ParseError(InvalidConfigError):
    pass


class Missing(InvalidConfigError):
    pass
