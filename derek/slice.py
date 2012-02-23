"""Derek slices."""

import logging

from derek.errors import DerekError

__all__ = ["SliceError", "Slice"]

LOG = logging.getLogger(__name__)

class SliceError(DerekError):
    """Slice error."""
    pass

class Slice(object):
    """Branch snapshot."""

    def __init__(self, client, slice_id):
        """Constructor."""
        self._client = client
        self.slice_id = slice_id
        try:
            self.username, self.reponame, self.hash = slice_id.split("/")
        except ValueError:
            LOG.error("'%s' is incorrect value for slice id" % slice_id)
            raise SliceError("Incorrect slice ID '%s'" % slice_id)

    def __str__(self):
        """Return string representation of the instance."""
        return self.slice_id

    def __repr__(self):
        """Return repr representation of the instance."""
        return "<Slice: %s>" % self

    def download_package(self, name, version, outdir):
        """Download package files."""
        raise NotImplementedError

    def history(self, limit, offset=0):
        """Return slice history."""
        raise NotImplementedError
