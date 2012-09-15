"""
A registry of CLI commands
"""

from derek.errors import DerekError

__all__ = ['Argument', 'command', 'add_parsers']

def _firstline(item):
    """
    extract first non-empty line from the item's docstring
    """
    assert hasattr(item, '__doc__')

    lines = [line.strip() for line in item.__doc__.splitlines()]

    return [line for line in lines if line][0]

class Argument(object):
    """
    parameter storage for arguments
    """

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def add(self, parser):
        """
        add an argument for argparse
        """
        return parser.add_argument(*self._args, **self._kwargs)

class _CommandRegistry(object):
    """
    ...
    """

    _commands = {}

    @staticmethod
    def register(func, args, kwargs):
        """
        ...
        """
        name = kwargs.get('name', func.__name__)

        if name in _CommandRegistry._commands:
            raise DerekError('Command %s is already defined' % name)

        _CommandRegistry._commands[name] = (func, args, kwargs)

    @staticmethod
    def add_parsers(subp):
        """
        ...
        """
        for name in sorted(_CommandRegistry._commands.keys()):
            func, args, kwargs = _CommandRegistry._commands[name]

            parser = subp.add_parser(name, help=_firstline(func))

            for arg in args:
                arg.add(parser)

            parser.set_defaults(command=func)

def command(args, **kwargs):
    """
    decorate a function so it can be used with ArgumentParser
    """
    assert all([isinstance(arg, Argument) for arg in args]), \
           'Wrong kind of parameter for command decorator'

    def _command_r(func):
        """
        register the command
        """
        _CommandRegistry.register(func, args, kwargs)

        return func

    return _command_r

def add_parsers(subparser):
    """
    ...
    """
    _CommandRegistry.add_parsers(subparser)
