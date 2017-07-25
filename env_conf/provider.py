import os

from .errors import Missing
from .types import FieldType


class Field:
    def __init__(
            self, type_, desc=None, name=None,
            optional=False, default=None):
        self.name = name
        self.desc = desc
        self.optional = optional
        self.default = default
        self._cache = None
        if isinstance(type_, type):
            if issubclass(type_, FieldType):
                self.type_ = type_()
            else:
                raise TypeError("Invalid field type for {}.".format(self.name))
        elif isinstance(type_, FieldType):
            self.type_ = type_
        else:
            raise TypeError("Invalid value for {}.".format(self.name))

    def resolve(self, env):
        if self._cache is not None:
            return self._cache
        value = env.get(self.name)
        if value is None:
            if self.default is not None:
                return self.default
            elif self.optional:
                return None
            else:
                raise Missing("Required variable {} not set".format(self.name))
        self._cache = self.type_.parse(value)
        return self._cache

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.resolve(instance.env)

    def __str__(self):
        return "<Field(name={}, type={})>".format(self.name, self.type_)

    def __repr__(self):
        return str(self)


class ProviderMeta(type):
    def __new__(mcs, name, bases, attrs):
        fields = []
        for key, value in attrs.items():
            if isinstance(value, Field):
                if value.name is None:
                    value.name = key
                fields.append(value)
        attrs['fields'] = tuple(fields)
        return super().__new__(mcs, name, bases, attrs)


class EnvProvider(metaclass=ProviderMeta):
    def __init__(self, eager=True):
        if eager:
            self.load()

    @property
    def env(self):
        return os.environ

    def load(self):
        for i in self.fields:   # pylint: disable=no-member
            i.resolve(self.env)

    def __str__(self):
        frags = []
        for i in self.fields:   # pylint: disable=no-member
            item = '{}={}'.format(i.name, repr(i.resolve(self.env)))
            frags.append(item)
        return '<Env({})>'.format(', '.join(frags))
