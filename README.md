# ConfLoad

A tool to handle configurations

[Pypi Linkl](https://pypi.org/project/confload)

## Support

format:

* ini
* json
* yaml

origins:

* url
* environment
* objects
* files



## Installation

```bash
pip3 install confload
```



## Use

```python
from confload import Config

# Construct config with default values
cfg = Config({"test": 43})

# load from yaml, json or ini specificly
cfg.load_yaml("test.yml")

# guess loading type from suffix
cfg.load("test.ini")

cfg["abcd"]["test4"]["test2"] = 4  # automaticly create dict if key does not exists

dict(cfg)  # convertible to dict, best is to use dict method
cfg.dict(copy=False)

# update methods are currently merge and replace
cfg["abcd"].merge(test4={"test3": 5})  # Merge recursively merge two dicts objects
cfg["abcd"].replace(test4={"test3": 5})  # replace will replace objects as dict's update builtins method
cfg["abcd"].update(test4={"test3": 5})  # use the strategy defined on cfg build

# You can also load your config from an url (method's parameters are passed to requests.get method)
cfg.request_json("my_site.com/config.json")

# Or from your env
cfg.env_json("MY_JSON_FILE")  # Precise the format
cfg.env("MY_INI_FILE")  # or let it guess using the file suffix

cfg.dump_json("myfile.json")  # can be yaml but not ini file
```

Nb: most of the methods can be chained

```python
cfg = Config(...).update(...).env(...).load(...)
```



## Futur

* add support for argparse
* add support for environment variables that are not files (e.g.: MY_CUSTOM_PORT=80)
* documentation will be done, some change may appear as well.