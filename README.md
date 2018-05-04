# Env.conf

Env.conf is a utility library which helps you read and parse configurations from
environment.


[![Build Status](https://travis-ci.org/QuantumGhost/env_conf.svg?branch=master)](https://travis-ci.org/QuantumGhost/env_conf)
[![codecov](https://codecov.io/gh/QuantumGhost/env_conf/branch/master/graph/badge.svg)](https://codecov.io/gh/QuantumGhost/env_conf)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FQuantumGhost%2Fenv_conf.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FQuantumGhost%2Fenv_conf?ref=badge_shield)

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


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FQuantumGhost%2Fenv_conf.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FQuantumGhost%2Fenv_conf?ref=badge_large)