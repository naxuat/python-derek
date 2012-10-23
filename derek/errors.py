"""Derek errors."""

from restkit.errors import ResourceNotFound, Unauthorized, RequestFailed

__all__ = ["DerekError", "ResourceNotFound", "Unauthorized", "RequestFailed"]

class DerekError(Exception):
    """Derek error."""
    pass
