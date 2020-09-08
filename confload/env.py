import os
from pathlib import Path
from . import schema

_sentinelle = object()

def file_from_env(var):
    value = os.environ.get(var)
    if value is not None:
        return Path(value).resolve()
    return value

def _get(key, validator, default=_sentinelle):
    if key not in os.environ:
        if default is _sentinelle:
            raise Exception("No environment variable {key}".format(
                key=key,
            ))
        return default
    return validator(os.environ[key].strip())

def String(key, default=_sentinelle):
    return _get(key, str, default)

def Bool(key, default=_sentinelle):
    return _get(key, schema.Bool, default)

def Int(key, default=_sentinelle):
    return _get(key, schema.Int, default)

def Float(key, default=_sentinelle):
    return _get(key, schema.Float, default)


class _List:
    __name__ = "List"
    def __init__(self, callable_=str, separator=","):
        self._callable = callable_
        self._separator = separator

    def __getitem__(self, callable_):
        return _List(callable_, self._separator)

    def __call__(self, key, default=_sentinelle):
        data = String(key, default)
        return schema.Split(self._callable, self._separator).validate(data)

List = _List()

class EnvList:
    __name__ = "List"

    def __init__(self, env_proxy, callable_=str, separator=","):
        self._env_proxy = env_proxy
        self._callable = callable_
        self._separator = separator

    def __getitem__(self, callable_):
        return EnvList(self._env_proxy, callable_, self._separator)

    def __call__(self, key, default=_sentinelle, name=_sentinelle):
        return self._env_proxy._get(List[self._callable], key, default, name)


class EnvProxy:
    def __init__(self, config):
        self._config = config
        self.list = EnvList(self)
        
    def _get(self, getter, key, default, name):
        value = getter(key, default)
        if name is not _sentinelle:
            key = name
        return self._config.update({key: value})

    def __call__(self, env):
        """
            Load the file represented by the given environment variable.
            The format is guessed by using the file suffix
        """
        fd = file_from_env(env)
        return self._config.load(fd)

    def json(self, env):
        """
            Load the json file represented by the given environment variable
        """
        fd = file_from_env(env)
        return self._config.load_json(file)

    def yaml(self, env):
        """
            Load the yaml file represented by the given environment variable
        """
        fd = file_from_env(env)
        return self._config.load_json(file)

    def ini(self, env):
        """
            Load the ini file represented by the given environment variable
        """
        fd = file_from_env(env)
        return self._config.load_ini(file)

    def string(self, key, default=_sentinelle, name=_sentinelle):
        return self._get(String, key, default, name)

    def bool(self, key, default=_sentinelle, name=_sentinelle):
        return self._get(Bool, key, default, name)

    def int(self, key, default=_sentinelle, name=_sentinelle):
        return self._get(Int, key, default, name)

    def float(self, key, default=_sentinelle, name=_sentinelle):
        return self._get(Float, key, default, name)
