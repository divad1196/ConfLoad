import sys
from . import schema
from schema import Use
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
    def __init__(self, name, aliases=None, default=_sentinelle, schema=str, need_value=True):
        self.name = name
        if aliases is None:
            aliases = [name]
        self.aliases = [ _make_option(alias) for alias in aliases]
        self.schema = Use(schema)
        self.default = default
        self.need_value = need_value

    def __call__(self, values, val):
        res = self.schema.validate(val)
        values[self.name] = self.schema.validate(res)

    def __repr__(self):
        return self.name

class String(Argument):
    def __init__(self, *args, **kwargs):
        kwargs["schema"] = str
        super().__init__(*args, **kwargs)

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
    """
        Boolean value only meant to be used as option without value.
        Default value is mandatory (either True or False).
        Using the options toggle the default value
    """
    def __init__(self, *args, **kwargs):
        kwargs["schema"] = schema.Bool
        super().__init__(*args, **kwargs)

class Toggle(Argument):
    """
        Boolean value only meant to be used as option without value.
        Default value is mandatory (either True or False).
        Using the options toggle the default value
    """
    def __init__(self, *args, default=False, **kwargs):
        if default not in [True, False]:
            raise Exception("Default Value must be either True or False")
        kwargs["schema"] = schema.Bool
        kwargs["need_value"] = False
        kwargs["default"] = default
        super().__init__(*args, **kwargs)

    def __call__(self, values, val):
        """
            Parameter 'val' is ignored.
            Set the option has the invert of default value.
        """
        values[self.name] = not self.default

class List(Argument):
    def __init__(self, *args, **kwargs):
        kwargs["schema"] = schema.Split()
        super().__init__(*args, **kwargs)

    def __call__(self, values, val):
        if self.name not in values:
            values[self.name] = []
        values[self.name] += self.schema.validate(val)

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

        # TODO: do not split positional at first, only handle them when no more option is found
        nb_positional = len(self._args)
        positional = args[-nb_positional:]
        optionals = args[:-nb_positional]

        if len(positional) != nb_positional:
            raise Exception("Missing positional arguments")

        for i in range(nb_positional):
            val = positional[i]
            arg = self._args[i]
            arg(values, val)

        options = iter(optionals)
        for opt in options:
            if opt not in self.aliases:
                raise Exception("Unknown alias {name}".format(
                    name=opt,
                ))
            alias = self.aliases[opt]

            val = None
            if alias.need_value:
                val = next(options, None)
                if val is None:
                    raise Exception("Missing value after alias {alias}".format(
                        alias=opt,
                    ))
            alias(values, val)
        
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