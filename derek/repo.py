from derek.errors import DerekError

__all__ = ["Repo", "RepoError"]

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

    @property
    def branches(self):
        """Return lists of Branch instances."""
        raise NotImplementedError

