"""
Derek default values
"""

DEFAULT_PORT = 9000
DEFAULT_HOST = "localhost"

DEFAULT_CONFDIR = '~/.drkrc'

DEFAULT_BRANCH = "unstable"
DEFAULT_ARCH = "i386,armel"
DEFAULT_REPO = "default"

ALIASES_NAME = "aliases"

REPO_DOC = ("repository (<alias>, <alias>:<branch>, <user>/<name>, "
            "<user>/<name>/<branch>, if <branch> is not specified, %s"
            " will be used)") % (DEFAULT_BRANCH)
