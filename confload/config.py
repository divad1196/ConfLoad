import json
import yaml
import requests
from pathlib import Path
from .tools import file_from_env, recursive_dict_merge, ini_file_to_dict
from copy import deepcopy

VALIDES_CONFIG_STRATS = [
    "merge",
    "replace"
]

DEFAULT_CONFIG_STRAT = VALIDES_CONFIG_STRATS[0]

def _validate_strat(strat):
    if strat in VALIDES_CONFIG_STRATS:
        return strat
    return DEFAULT_CONFIG_STRAT

class Config:
    def __init__(self, values={}, strat=DEFAULT_CONFIG_STRAT):
        self._values = values
        self._strat = _validate_strat(strat)

    def __getitem__(self, key):
        if key in self._values:
            value = self._values[key]
        else:
            value = {}
            self._values[key] = value
        if isinstance(value, dict):
            return Config(value)
        return value

    def __str__(self):
        return str(self._values)

    def __repr__(self):
        return repr(self._values)

    def __setitem__(self, key, value):
        self._values[key] = value

    def __iter__(self):
        return iter(self._values)

    def dict(copy=False):
        """
            Return the inner dict object.
            if copy is True, then a copy is return instead
        """
        if copy:
            return deepcopy(self._values)
        return self._values()

    def items(self):
        return self._values.items()

    def keys(self):
        """
            return the config keys
        """
        return self._values.keys()

    def values(self):
        """
            return an iterator on the dict values
        """
        for val in self._values.values():
            if isinstance(val, dict):
                yield Config(val)
            else:
                yield val

    def __contains__(self, item):
        return self._values.__contains__(item)

    def get(self, key, default=None):
        """
            get the value if exists, otherwise return the default value
        """
        if key not in self._values:
            return default
        return self[key]

    def update(self, *values, **kwargs):
        """
            Update the config using the strategy of the config
        """
        if self._strat == "merge":
            return self.merge(*values, **kwargs)
        elif self._strat == "replace":
            return self.replace(*values, **kwargs)
        return self

    def replace(self, *values, **kwargs):
        """
            Update the config by replacing existing values
        """
        for val in values:
            self._values.update(val)
        self._values.update(kwargs)
        return self

    def merge(self, *values, **kwargs):
        """
            Merge dict lists and named parameter recursively
        """
        for value in values:
            recursive_dict_merge(value, self._values)
        recursive_dict_merge(kwargs, self._values)
        return self

    # From file
    def load(self, file):
        """
            Load the file.
            The format is guessed by using the file suffix
        """
        path = Path(file).resolve()
        suffix = path.suffix.lower()
        if suffix == ".json":
            return self.load_json(str(path))
        elif suffix in [".yml", ".yaml"]:
            return self.load_yaml(str(path))
        elif suffix == ".ini":
            return self.load_ini(str(path))
        return self

    def load_json(self, file):
        """
            Load the json file
        """
        with open(file, "r") as f:
            data = json.load(f)
        self.update(data)
        return self
    
    def load_yaml(self, file):
        """
            Load the yaml file
        """
        with open(file, "r") as f:
            data = yaml.safe_load(f)
        self.update(data)
        return self

    def load_ini(self, file):
        """
            Load the ini file
        """
        data = ini_file_to_dict(file)
        self.update(data)
        return self

    # From env
    def env(self, env):
        """
            Load the file represented by the given environment variable.
            The format is guessed by using the file suffix
        """
        fd = file_from_env(env)
        return self.load(fd)

    def env_json(self, env):
        """
            Load the json file represented by the given environment variable
        """
        fd = file_from_env(env)
        return self.load_json(file)

    def env_yaml(self, env):
        """
            Load the yaml file represented by the given environment variable
        """
        fd = file_from_env(env)
        return self.load_json(file)

    def env_ini(self, env):
        """
            Load the ini file represented by the given environment variable
        """
        fd = file_from_env(env)
        return self.load_ini(file)

    # From http
    def request_json(self, *args, **kwargs):
        """
            Request config in json format.
            Parameters are passed to get function from requests module
        """
        response = requests.get(*args, **kwargs)
        data = response.json()
        return self.update(data)

    def request_yaml(self, *args, **kwargs):
        """
            Request config in yaml format.
            Parameters are passed to get function from requests module
        """
        response = requests.get(*args, **kwargs)
        data = yaml.safe_load(response.text)
        return self.update(data)

    def request_ini(self, *args, **kwargs):
        """
            Request config in ini format.
            Parameters are passed to get function from requests module
        """
        response = requests.get(*args, **kwargs)
        data = ini_string_to_dict(response.text)
        return self.update(data)


    # Dump to file
    def dump_json(self, file):
        """
            dump config in file in json format
        """
        with open(file, "w") as f:
            json.dump(self._values, f, indent=4, sort_keys=True)

    def dump_yaml(self, file):
        """
            dump config in file in yaml format
        """
        with open(file, "w") as f:
            yaml.dump(self._values, f, default_flow_style=False)
        