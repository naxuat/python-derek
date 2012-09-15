"""Derek client."""

import logging
import json

from restkit import Resource, BasicAuth # TODO: OAuth
from restkit import ResourceNotFound, Unauthorized, RequestFailed

from derek.slice import Slice
from derek.branch import Branch
from derek.user import User
from derek.repo import Repo
from derek.defaults import DEFAULT_PORT, DEFAULT_HOST

__all__ = ["Client"]

LOG = logging.getLogger(__name__)

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

    def post(self, path, payload = None):
        """Do POST request to Derek."""

        if payload is None:
            payload = {}

        headers = {
                      'content-type': 'application/x-www-form-urlencoded'
                  }

        resp = self.resource.post(path=path,
                                  payload=dict2qs(payload),
                                  headers=headers)
        return resp

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
        with resp.body_stream() as body:
            with open(out, 'wb') as handle:
                for block in body:
                    handle.write(block)

    def upload(self, path, filepath):
        """Upload file to server."""

        with open(filepath) as pfile:
            self.resource.post(path=path, payload=pfile)

    def branch(self, branch_id):
        """Return Branch object."""
        return Branch(self, branch_id)

    def slice(self, slice_id):
        """Return Slice object."""
        return Slice(self, slice_id)

    def user(self, username):
        """Return User object."""
        return User(self, username)

    def repo(self, repo_id):
        """Return repository object."""
        return Repo(self, repo_id)
