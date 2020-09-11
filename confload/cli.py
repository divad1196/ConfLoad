import sys
from . import schema
from schema import Schema
from pathlib import Path

_sentinelle = object()

def _make_option(name):
    alias = name.strip("- ")
    if len(alias) == 1:
        return "-" + alias
    if len(alias) > 1:
        return "--" + alias
    raise Exception("Invalid option {name}".format(
        name=name,
    ))

def _get_program_name():
    path = Path(sys.argv[0])
    name = path.stem
    return name


class Argument:
    def __init__(self, name, aliases=None, default=_sentinelle, schema=str):
        self.name = name
        if aliases is None:
            aliases = [name]
        self.aliases = [ _make_option(alias) for alias in aliases]
        self.schema = Schema(schema)

    def __call__(self, values, alias, cursor):
        text = next(cursor)
        values[self.name] = self.schema.validate(text)

class Int(Argument):
    def __init__(self, *args, **kwargs):
        kwargs["schema"] = schema.Int
        super().__init__(*args, **kwargs)

class Float(Argument):
    def __init__(self, *args, **kwargs):
        kwargs["schema"] = schema.Float
        super().__init__(*args, **kwargs)

## Particular
# set default and toggle it with param ? e.g. default is False, using --mybool set it to True
# force a following argument: --mybool on/off  # simpliest here
# use 2 differents aliases, one for each value
# Make one classe for each?
class Bool(Argument):
    def __init__(self, **kwargs):
        kwargs["schema"] = schema.Bool
        super().__init__(**kwargs)

class List(Argument):
    def __init__(self, **kwargs):
        kwargs["schema"] = schema.List
        super().__init__(**kwargs)

    def __call__(self, values, alias, cursor):
        text = next(cursor)
        if self.name not in values:
            values[self.name] = []
        values[self.name] += self.schema.validate(text)

class SubParser:
    def __init__(self, **kwargs):
        self._parsers = kwargs

    def __str__(self):
        return "\n".join(self._parsers.keys())
    
    def __call__(self, args=None):
        if args is None:
            args = sys.argv[1:]

        if not args:
            raise Exception("")
    
        name = args[0]
        args = args[1:]
        parser = self._parsers.get(name)
        if parser is None:
            raise Exception("Parser {name} is not defined".format(
                name=name,
            ))
        return parser(args)


class Parser:
    def __init__(self, args=[], options=[], name=None):
        if name is None:
            name = _get_program_name()
        self.name = name
        self._args = args
        self._options = options
        self.aliases = self._get_aliases()

    def __str__(self):
        return "[OPTIONS] {positionals}".format(
            positionals=" ".join(
                arg.name.upper()
                for arg in self._args
            )
        )

    def __call__(self, args=None):
        if args is None:
            args = sys.argv[1:]
        
        defaults = self._default_prefilled_values()
        values = {}

        nb_positional = len(self._args)
        positional = args[-nb_positional:]
        optionals = args[:-nb_positional]

        for i in range(nb_positional):
            value = positional[i]
            arg = self._args[i]
            arg(values, value)

        options = iter(optionals)
        for opt in options:
            if opt not in self.aliases:
                raise Exception("Unknown alias {name}".format(
                    name=opt,
                ))
            self.aliases[opt](values, opt, options)

        defaults.update(values)
        return defaults

    def _default_prefilled_values(self):
        return {
            opt.name: opt.default
            for opt in self._options
            if opt.default is not _sentinelle
        }

    def _check_keys(self):
        keys = []
        for param in self._args + self._options:
            k = param.name.lower()
            if k in keys:
                raise Exception("Option {name} defined multiple times (Case insensitive)".format(
                    name=param.name,
                ))
            keys.append(k)
        
    def _get_aliases(self):
        aliases = {}
        for opt in self._options:
            for alias in opt.aliases:
                if alias in aliases:
                    raise Exception("Alias {name} defined multiple times".format(
                        name=alias,
                    ))
                aliases[alias] = opt
        return aliases




# p1 = Parser(
#     [
#         String("name"),
#     ],
#     [
#         String("lastname", aliases=["lastname", "l"])
#     ],
# )

# p1()