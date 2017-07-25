# Env.conf

Env.conf is a utility library which helps you read and parse configurations from
environment.


[![CircleCI](https://img.shields.io/circleci/project/github/QuantumGhost/env_conf.svg?style=plastic)](https://circleci.com/gh/QuantumGhost/env_conf)
[![codecov](https://codecov.io/gh/QuantumGhost/env_conf/branch/master/graph/badge.svg)](https://codecov.io/gh/QuantumGhost/env_conf)

## Usage

~~~py
from env_conf import EnvProvider, Field
from env_conf.types import String, Integer, List, Boolean


class Config(EnvProvider):
    debug = Field(Boolean, desc='debug mode flag', default=False)
    host = Field(String, desc='host the server listens on', default='127.0.0.0')
    port = Field(Integer, desc='port the server listens on', default=5000)
    # override environment variable name
    # this field is required and must be specified
    # the value is read from `DATABASE_URI` environment variable.
    db_uri = Field(String, name='DATABASE_URI', desc='database uri')
    # compound type
    slave_uris = Field(
        List(separator=';', item_type=String),
        desc="the list of slave database uri, separated by comma"
    )

# configurations are loaded and parsed at the time the `config`
# instance is created.
config = Config()
~~~

## TODO

 - Better documentation
 - More types
 - Allow builtin types used as `FieldType` (for example `Field(str)`)
   (By implement a `TypeWrapper` class and delegate parse to the type
   argument)
