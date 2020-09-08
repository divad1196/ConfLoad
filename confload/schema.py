from schema import Schema, And, Or, Use, Optional, Literal


def Nullable(validator):
    return Schema(Or(validator, None), description="Can be None if evaluated to False")

def HasKey(key):
    return Schema(lambda d: isinstance(d, dict) and key in d, name="has key {key}".format(key=key))


BOOLEAN_TRUE = ["true", "on"]
BOOLEAN_FALSE = ["false", "off"]

def Bool(data):
    if isinstance(data, str):
        data = data.strip().lower()
        if data in BOOLEAN_TRUE:
            data = True
        elif data in BOOLEAN_FALSE:
            data = False
    return Schema(Use(bool), name="Bool").validate(data)

def Int(data):
    return Schema(Use(int), name="Int").validate(data)

def Float(data):
    return Schema(Use(float), name="Float").validate(data)


class List:
    def __init__(self, callable_):
        self._callable = callable_

    def __getitem__(self, callable_):
        return List(callable_, self._separator)

    def __call__(self, data):
        return self.validate(data)

    def validate(self, data):
        if not isinstance(data, list):
            data = [data]
        return Schema([Use(self._callable)], name="Ensure List").validate(data)


class Split:
    def __init__(self, callable_=str, separator=","):
        self._callable = callable_
        self._separator = separator

    def __getitem__(self, callable_):
        return Split(callable_, self._separator)

    def __call__(self, data):
        return self.validate(data)

    def validate(self, data):
        if isinstance(data, str):
            data = [
                value.strip()
                for value in data.split(self._separator)
                if value.strip()
            ]
        return List(self._callable).validate(data)
