"""
Command line interface
"""

import sys

from argparse import ArgumentParser

# {{{ import these to initialize CLI registry
import derek.client
import derek.repo
import derek.misc
# }}}

from derek.cli_registry import add_parsers
from derek.defaults import DEFAULT_CONFDIR

def main(args=None):
    """
    entry point
    """
    parser = ArgumentParser()

    parser.add_argument('-C', '--confdir', default=DEFAULT_CONFDIR,
                        metavar='DIR',
                        help='specify configuration directory '
                             '(default: %(default)s)')
    parser.add_argument('-v', '--version', action='store_true',
                        help='show version and exit')

    add_parsers(parser.add_subparsers(title='commands'))

    if args is None:
        args = sys.argv[1:]

    env = parser.parse_args(args)

    sys.exit(env.command(env))

if __name__ == '__main__':
    main()
