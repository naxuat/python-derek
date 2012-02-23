
__all__ = ["Repo"]

class Repo(object):
    """Package repository."""

    def __init__(self):
        """Constructor."""
        pass

    @property
    def branches(self):
        """Return lists of Branch instances."""
        raise NotImplementedError

