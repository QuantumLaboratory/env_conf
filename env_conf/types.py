from typing import List as _List
from .errors import ParseError


class FieldType:
    def parse(self, value):
        raise NotImplementedError("subclass should implement this method.")

    def __str__(self):
        return '<{}>'.format(self.__class__.__name__)


class String(FieldType):
    def parse(self, value) -> str:
        return value


class Integer(FieldType):
    def parse(self, value) -> int:
        try:
            return int(value)
        except ValueError:
            raise ParseError(
                "Invalid value for type {}".format(self))


class Boolean(FieldType):
    _VALID_BOOL_VALUES = frozenset(['true', 'false'])

    def parse(self, value) -> bool:
        value = value.lower()
        if value.lower() not in self._VALID_BOOL_VALUES:
            raise ParseError("")
        return value == 'true'


class List(FieldType):
    def __init__(self, separator=',', item_type=String):

        self.separator = separator
        if (
                isinstance(item_type, type) and
                issubclass(item_type, FieldType)):
            self.item_type = item_type()
        elif isinstance(item_type, FieldType):
            self.item_type = item_type
        else:
            raise TypeError("The type of item_type is invalid.")

    def parse(self, value) -> _List:
        values = []
        for idx, val in enumerate(value.split(self.separator)):
            try:
                val = self.item_type.parse(val)
            except ParseError:
                msg = "Invalid value {} for type {} at index {}".format(
                    value, self.item_type, idx
                )
                raise ParseError(msg)
            values.append(val)
        return values
