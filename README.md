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
cfg.env.json("MY_JSON_FILE")  # Precise the format
cfg.env("MY_INI_FILE")  # or let it guess using the file suffix

# you can also retrieve vars from env
cfg.env.string("MY_VAR", default="not found", name="myvar")  # you can give the name to use in the config (default take env var name)

# cfg.env.int, cfg.env.float also exists
cfg.env.bool(...)  # Value are case INsensitive tested.
                   # True value are "on", "True" or any non nulle number
                   # False value are "off", "False" or 0
        
# we can get a list too
cfg.list(...)
# and cast the result
cfg.list[int](...)  #  the value "1,2,3" becomes [1, 2, 3] and not ["1", "2", "3"]

cfg.dump_json("myfile.json")  # can be yaml but not ini file
```

Nb: most of the methods can be chained

```python
cfg = Config(...).update(...).env(...).load(...)
```



## Custom CLi parser

[argparse](https://docs.python.org/3/library/argparse.html), [click](https://click.palletsprojects.com/en/7.x/) and many others are goods, but i found them too complicated for most of the used i had.

Based on those two, here is another parser

```python
from confload.cli import Parser, SubParser, String, Int, Float, Bool, Toggle, List


parser = Parser(
    # Positional values
    [
        String("name"),
        Int("abcde"),
    ],

    # Optional values
    [
        String("lastname", aliases=["lastname", "l"]),
        List("children", aliases=["child", "c"]),
        Toggle("active", aliases=["active", "y"], default=False),
    ],
)


print(str(parser))
print(parser.aliases)
res = parser()

print(res)
```

Running `python3 test_parser.py -l abcde --child foo,bar --lastname trew -c another -c some,other test 56` we get the following output

```txt
[OPTIONS] NAME ABCDE
{'--lastname': lastname, '-l': lastname, '--child': children, '-c': children, '--active': active, '-y': active}
{'active': False, 'name': 'test', 'abcde': 56, 'lastname': 'trew', 'children': ['foo', 'bar', 'another', 'some', 'other']}
```



When we implement a tool, it is usefull to use subparser automaticly calling functions. (This is in progress)



## Futur

* add support for argparse
* documentation will be done, some change may appear as well.