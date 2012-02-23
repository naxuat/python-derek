from derek.errors import DerekError

__all__ = ["SliceError", "Slice"]

class SliceError(DerekError):
    pass

class Slice(object):
    """Branch snapshot."""

    def __init__(self, client, id):
        """Constructor."""
        self._client = client
        self.id = id
        try:
            self.username, self.reponame, self.hash = id.split("/")
        except ValueError:
            LOG.error("'%s' is incorrect value for branch id" % id)
            raise SliceError("Incorrect slice ID '%s'" % id)

    def __str__(self):
        """Return string representation of the instance."""
        return self.id

    def __repr__(self):
        """Return repr representation of the instance."""
        return "<Slice: %s>" % self

    def download_package(self, name, version, outdir):
        """Download package files."""
        raise NotImplementedError

