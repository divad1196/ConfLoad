import os
from pathlib import Path
import inspect


try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

# def get_env(var, default=None, type=str):
#     val = os.environ.get(var)
#     if val is None:
#         return default
#     return type(val)

def file_from_env(var):
    value = os.environ.get(var)
    if value is not None:
        return Path(value).resolve()
    return value

def recursive_dict_merge(src, dest):
    for key, value in src.items():
        if not isinstance(value, dict) or key not in dest:
            dest[key] = value
        else:
            dest_value = dest[key]
            if isinstance(dest_value, dict):
                recursive_dict_merge(value, dest_value)
            else:
                dest[key] = value


def ini_file_to_dict(file):
    cfg = ConfigParser()
    cfg.read(file)
    data = {
        section: dict(values)
        for section, values in cfg.items()
    }
    return data

def ini_string_to_dict(text):
    cfg = ConfigParser()
    cfg.read_string(text)
    data = {
        section: dict(values)
        for section, values in cfg.items()
    }
    return data

def get_home_path():
    return str(Path.home().resolve())

def get_current_file_path():
    stack = inspect.stack()
    layer = stack[1]  # previous stack, 0 is the current in the function
    frame = layer.frame
    if "__file__" not in frame.f_globals:
        return ""
    return str(Path(frame.f_globals["__file__"]).resolve())
