
__all__ = ["User"]

class User(object):
    """Represents user."""

    def __init__(self, client, username):
        """Constructor."""

        self._client = client
        self.username = username

    def create_repo(self, name):
        """Create new repository."""
        raise NotImplementedError
