import logging

from derek.errors import DerekError, ResourceNotFound
from derek.cli_registry import Argument, command

from derek.defaults import REPO_DOC

__all__ = ["Repo", "RepoError"]

LOG = logging.getLogger(__name__)

class RepoError(DerekError):
    pass

class Repo(object):
    """Package repository."""

    def __init__(self, client, repo_id):
        """Constructor."""
        self._client = client
        self.repo_id = repo_id
        try:
            self.username, self.reponame = repo_id.split("/")
        except ValueError:
            LOG.error("'%s' is incorrect value for repository id" % repo_id)
            raise RepoError("Incorrect repository ID '%s'" % repo_id)
        self._repo_doc = None

    def __str__(self):
        """Return string representation of the instance."""
        return self.repo_id

    def __repr__(self):
        """Return repr representation of the instance."""
        return "<Repo: %s>" % self

    def _load(self):
        """Loads repo data from Derek."""

        context = {
            "username": self.username,
            "reponame": self.reponame
        }
        LOG.debug("Loading %s" % self.repo_id)
        self._repo_doc = self._client.getjson(
                        path="/users/%(username)s/repos/%(reponame)s" % context)
        LOG.debug("doc loaded: %r" % self._repo_doc)

    @property
    def _doc(self):
        """Return repo doc."""

        if self._repo_doc is None:
            self._load()
        return self._repo_doc

    def exists(self):
        """Check if repo exists in Derek."""

        try:
            self._load()
        except ResourceNotFound:
            return False

        return True

    @property
    def branches(self):
        """Return lists of Branch instances."""

        if self._repo_doc is None:
            self._load()
        return [self._client.branch("%s/%s" % (self.repo_id, bname))
                for bname in self._doc["branches"]]

@command([
])
def repo(env):
    "show various information about repository"

@command([
    Argument('-a', '--alias', help='add an alias after creation'),
    Argument('-A', '--force-alias', action='store_true',
                help='overwrite the existing alias'),
    Argument('-t', '--type', default='deb',
                help='repository type (default: %(default)s)'),
    Argument('repo', help=REPO_DOC)
])
def create(env):
    """create a new repository"""

@command([
#            {"repo", REPO_DOC
#            {"branch", "new branch name"}
])
def branch(env):
    "create a new branch"

@command([
#       {list, $l, "list", undefined, "list defined aliases"},
#       {add, $a, "add", string, "add an alias (<add> -- an alias to add)"},
#       {delete, $d, "delete", undefined, "delete an alias"},
#       {force, $f, "force", undefined, "force overwriting an existing alias"}
])
def alias(env):
    "manage repository aliases"

@command([
#           {"repo", REPO_DOC
#           {"branch", "branch name to merge from"}
])
def merge(env):
    "perform a merge"
