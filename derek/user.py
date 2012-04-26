
__all__ = ["User"]

class User(object):
    """Represents user."""

    def __init__(self, client, username):
        """Constructor."""

        self._client = client
        self.username = username
        self._user_doc = None

    def __str__(self):
        """Return string representation of the instance."""
        return self.username

    def __repr__(self):
        """Return repr representation of the instance."""
        return "<User: %s>" % self

    def reset_cache(self):
        """Reset local cache."""
        self._user_doc = None

    @property
    def _doc(self):
        """Return User document."""

        if not self._user_doc:
            self._user_doc = self._client.getjson("/users/%s" % self.username)

        return self._user_doc

    @property
    def repos(self):
        """Return list of Repo objects."""
        return [self._client.repo("%s/%s" % (self.username, repo_id))
                for repo_id in self._doc["repos"]]

    def add_repo(self, name, repo_type = "deb", archs=None):
        """Add new repository."""

        if archs is None:
            archs = ["i386"]
        assert isinstance(archs, list)

        archs_str = " ".join(archs)
        self._client.post("/users/%s/addrepo" % self.username,
                          {
                              "reponame": name,
                              "type":     repo_type,
                              "archs":    archs_str
                          })
        self.reset_cache()
