"""
Various operations that do not fall into a particular category
"""

from derek.cli_registry import Argument, command

# To be reviewed

@command([
    Argument('-o', '--check-only', action='store_true',
                help='check package(s) only and do not upload')
])
def upload(env):
    "upload new package(s)"

@command([
#       {arch, $a, "arch", {string, default},
#       "architecture (default: " ?DEFAULT_ARCH ")"}
], name='import')
def do_import(env):
    "import an existing repository"
