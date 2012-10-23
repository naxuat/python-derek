"""
Various operations that do not fall into a particular category
"""

from derek.cli_registry import Argument, command

# To be reviewed

@command([
    Argument('-D', action='store_true',
             help='run dinstall after upload'),
    Argument('-e', '--delayed', metavar='DELAYED', default=None,
             help="Upload to a delayed queue. Takes an argument from 0 to 15"),
    Argument('-f', '--force', action='store_true', help="Force an upload"),
    Argument('-l', action='store_true', help="Run lintian before upload"),
    Argument('-U', action='store_true',
             help="Do not write a .upload file after uploading"),
    Argument('-s', action='store_true', help="Simulate the upload only"),
    Argument('-u', action='store_true', help="Don't check GnuPG signature"),
    Argument('-V', action='store_true',
             help="Check the package version and then upload it"),
    Argument('-o', '--check-only', action='store_true',
                help='check package(s) only and do not upload')
])
def upload(_env):
    "upload new package(s)"

@command([
#       {arch, $a, "arch", {string, default},
#       "architecture (default: " ?DEFAULT_ARCH ")"}
], name='import')
def do_import(_env):
    "import an existing repository"
