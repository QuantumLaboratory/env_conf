import os

from .errors import Missing
from .types import FieldType


class Field:
    def __init__(
            self, type_, desc=None, name=None,
            optional=False, default=None):
        self.type_ = type_
        self.name = name
        self.desc = desc
        self.optional = optional
        self.default = default
        self._cache = None

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
                raise Missing("")
            return None
        if isinstance(self.type_, type):
            if issubclass(self.type_, FieldType):
                type_ = self.type_()
            else:
                raise ValueError("Invalid field type.")
        elif isinstance(self.type_, FieldType):
            type_ = self.type_
        else:
            raise ValueError("Invalid value")
        self._cache = type_.parse(value)
        return self._cache

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.resolve(owner.env)


class ProviderMeta(type):
    def __new__(mcs, name, bases, attrs):
        fields = []
        for k, v in attrs.items():
            if isinstance(v, Field):
                if v.name is None:
                    v.name = k
                fields.append(v)
        attrs['_fields'] = fields
        return super().__new__(mcs, name, bases, attrs)


class EnvProvider(metaclass=ProviderMeta):
    def __init__(self):
        self._load()

    @property
    def env(self):
        return os.environ

    def _load(self):
        for i in self._fields:
            i.resolve(self.env)

    def __str__(self):
        frags = []
        for i in self._fields:
            item = '{}={}'.format(i.name, i.resolve(self.env))
            frags.append(item)
        return '<Env()>'.format(', '.join(frags))
