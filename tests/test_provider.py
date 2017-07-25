import os
from unittest import mock

import pytest

from env_conf import EnvProvider, Field
from env_conf.errors import Missing
from env_conf.types import String

_TEST_DATA = {
    "string": "value",
    "integer": "1",
    "boolean": "true",
    "another-string": "another-value",
}

class Config(EnvProvider):
    string = Field(String)
    string2 = Field(String, name='another-string')


class TestField:
    def test_with_type_class(self):
        field = Field(String, name="string")
        assert field.resolve(_TEST_DATA) == "value"

    def test_with_type_instance(self):
        field = Field(String(), name="string")
        assert field.resolve(_TEST_DATA) == "value"

    def test_with_invalid_field_type(self):
        for i in (str, bytes.fromhex):
            with pytest.raises(TypeError):
                Field(i)

    def test_resolve_with_default_value(self):
        default = "foo"
        field = Field(String, name="string", default=default)
        assert field.resolve({}) == default

    def test_resolve_for_optional_field(self):
        field = Field(String, name="string", optional=True)
        assert field.resolve({}) is None

    def testing_missing_value(self):
        field = Field(String, name="string")
        with pytest.raises(Missing):
            field.resolve({})

    def test_repr_and_str(self):
        field = Field(String, name="host")
        assert "host" in repr(field)
        assert "host" in str(field)


class TestEnvProvider:
    def test_eager_load(self):
        with mock.patch.dict(os.environ, _TEST_DATA):
            config = Config()

        assert config.string == 'value'
        assert config.string2 == "another-value"

    def test_lazy_load(self):
        config = Config(eager=False)
        with mock.patch.dict(os.environ, _TEST_DATA):
            assert config.string == "value"
            assert config.string2 == "another-value"
        assert config.string == "value"
        assert config.string2 == "another-value"

    def test_naming(self):
        assert Config.string.name == "string"
        assert Config.string2.name == "another-string"

    def test_get_env(self):
        with mock.patch.dict('os.environ', _TEST_DATA, clear=True):
            config = Config()
            assert config.env == _TEST_DATA

    def test_fields(self):
        assert {Config.string, Config.string2} ==\
             set(Config.fields)   # pylint: disable=no-member

    def test_str(self):
        config = Config(eager=False)
        assert "string" in str(config)
        assert "another-string" in str(config)
