import pytest

from env_conf.errors import ParseError
from env_conf.types import Boolean, Bytes, Integer, List, String


def test_boolean_with_valid_values():
    t = Boolean()
    for i in ['true', 'TRUE', 'True']:
        assert t.parse(i)
    for i in ['false', 'FALSE', 'False']:
        assert not t.parse(i)


def test_boolean_with_invalid_values():
    t = Boolean()
    for value in ['0', '', 'foobar', '1', ' ', 'yes', 'no']:
        with pytest.raises(ParseError):
            t.parse(value)


def test_string():
    t = String()
    for i in ['0', 'foobar', '', 'true']:
        assert i == t.parse(i)


class TestList:
    def test_one_element_string(self):
        assert List().parse('foo') == ['foo']

    def test_two_list_string(self):
        assert List().parse('foo,bar,baz') == ['foo', 'bar', 'baz']

    def test_string_with_trailing_separator(self):
        assert List().parse('foo,bar,') == ['foo', 'bar', '']

    def test_empty_string(self):
        assert List().parse('') == ['']

    def test_separator_semicolon(self):
        l = List(';')
        assert l.parse('foo;bar') == ['foo', 'bar']
        assert l.parse('foo,bar') == ['foo,bar']

    def test_item_types(self):
        l1 = List(item_type=Integer)
        l2 = List(item_type=Integer())
        for l in (l1, l2):
            with pytest.raises(ParseError):
                l.parse('foo')
            with pytest.raises(ParseError):
                l.parse('1,2,')
            with pytest.raises(ParseError):
                l.parse('1,foo')
            assert l.parse('1') == [1]
            assert l.parse('1,2') == [1, 2]

    def test_with_invalid_types(self):
        for i in (str, bytes.fromhex):
            with pytest.raises(TypeError):
                List(item_type=i)


def test_bytes():
    b = Bytes()
    assert b.parse("xxx") == b"xxx"
    assert b.parse("你好") == b'\xe4\xbd\xa0\xe5\xa5\xbd'
