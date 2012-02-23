import logging
import json

from restkit import Resource, BasicAuth # TODO: OAuth

from derek.parsers import deb_changes
from derek.slice import Slice
from derek.branch import Branch
from derek.errors import DerekError

__all__ = ["Client"]

LOG = logging.getLogger(__name__)

DEFAULT_PORT = 9000
DEFAULT_HOST = "localhost"

def dict2qs(dictionary):
    """Convert dictionary to query string."""

    # don't touch non-dictionaries
    if not isinstance(dictionary, dict):
        return dictionary

    chunks = ["%s=%s" % (key, value) for key, value in dictionary.items()]
    return "&".join(chunks)

class Client(object):
    """Derek client."""

    def __init__(self, username, password,
                 host=DEFAULT_HOST, port=DEFAULT_PORT):
        """Constructor."""

        auth = BasicAuth(username, password)
        self.resource = Resource("http://%s:%d" % (host, port), filters=[auth])

    def postjson(self, path, payload):
        """Do POST request to Derek and expect JSON in response."""

        headers = {
                      'accept': 'application/json',
                      'content-type': 'application/x-www-form-urlencoded'
                  }

        resp = self.resource.post(path=path,
                                  payload=dict2qs(payload),
                                  headers=headers)
        return json.loads(resp.body_string())

    def getjson(self, path, params=None):
        """Do GET request to Derek and expect JSON in response."""

        if params is None:
            params = {}

        headers = {'accept': 'application/json'}
        resp = self.resource.get(path=path, headers=headers, **params)
        return json.loads(resp.body_string())

    def download(self, path, out):
        """Download file."""

        resp = self.resource.get(path=path)
        with self.resp.body_stream() as body:
            with open(out, 'wb') as handle:
                for block in body:
                    handle.write(block)

    def upload(self, path, filepath):
        """Upload file to server."""

        with open(filepath) as pf:
            self.resource.post(path=path, payload=pf)

    def branch(self, id):
        """Return Branch object."""
        return Branch(self, id)

    def slice(self, id):
        """Return Slice object."""
        return Slice(self, id)

    def user(self, username):
        """Return User object."""
        raise NotImplementedError

    def repo(self, id):
        """Return repository object."""
        raise NotImplementedError
