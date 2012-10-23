"""Derek branches."""

import logging
LOG = logging.getLogger(__name__)

import os

from derek.errors import DerekError
from derek.parsers import deb_changes

__all__ = ["BranchError", "Branch"]

class BranchError(DerekError):
    """Branch error."""
    pass

class Branch(object):
    """Repository branch."""

    def __init__(self, client, branch_id):
        """Constructor."""

        self._client = client
        self.branch_id = branch_id
        self._slice = None
        self._packages = None
        try:
            self.username, self.reponame, self.name = branch_id.split("/")
        except ValueError:
            LOG.error("'%s' is incorrect value for branch id" % branch_id)
            raise BranchError("Incorrect branch ID '%s'" % branch_id)

    def __str__(self):
        """Return string representation of the instance."""
        return self.branch_id

    def __repr__(self):
        """Return repr representation of the instance."""
        return "<Branch: %s>" % self

    def _load(self):
        """Loads branch data from Derek."""

        context = {
            "username": self.username,
            "reponame": self.reponame,
            "name":     self.name
        }
        LOG.debug("Loading %s" % self.branch_id)
        doc = self._client.getjson(path="/users/%(username)s/repos/%(reponame)s"
                                        "/branches/%(name)s" % context)
        LOG.debug("doc loaded: %r" % doc)
        slice_id = "%(username)s/%(reponame)s/%(slice_id)s" % {
            "username": self.username,
            "reponame": self.reponame,
            "slice_id": doc["slice_id"]
        }
        self._slice = self._client.slice(slice_id)
        self._packages = doc["packages"]

    def fork(self, new_name):
        """Fork branch."""

        context = {
            "id":       self.branch_id,
            "username": self.username,
            "reponame": self.reponame,
            "name":     self.name,
            "new_name": new_name
        }
        LOG.debug("Forking branch %(id)s to "
                  "%(username)s/%(reponame)s/%(new_name)s" % context)
        self._client.postjson(path="/users/%(username)s/"
                                   "repos/%(reponame)s/"
                                   "branches/%(name)s/fork" % context,
                              payload={"new_branch": new_name})

        return Branch(self._client, "%(username)s/%(reponame)s/%(new_name)s" %
                                     context)

    def merge(self, branch):
        """Merge packages from another branch."""

        if branch.username != self.username or branch.reponame != self.reponame:
            raise BranchError("Branch to merge must be in the same repository")

        context = {
            "username": self.username,
            "reponame": self.reponame,
            "name":     self.name
        }
        LOG.debug("Merging from %r to %r" % (branch, self))
        self._client.postjson(path="/users/%(username)s/repos/%(reponame)s/"
                                   "branches/%(name)s/merge" % context,
                              payload={"from_branch": branch.name})

    def upload_packages(self, packages):
        """Upload packages to branch."""

        context = {
            "username": self.username,
            "reponame": self.reponame,
            "name":     self.name
        }

        filepaths = [os.path.join(os.path.dirname(path), pfile['filename'])
                     for path in packages
                     for pfile in deb_changes(path)['files']]
        filepaths.extend(packages)

        # get upload token
        resp = self._client.postjson(path="/users/%(username)s/"
                                          "repos/%(reponame)s/"
                                          "branches/%(name)s/get_upload_token" %
                                           context,
                                     payload={})
        token = resp['utoken']
        for pfile in filepaths:
            self._client.upload(path="/upload/%s/send/%s" %
                                      (token, os.path.basename(pfile)),
                                filepath=pfile)
        self._client.post(path="/upload/%s/dput" % token)

    def download_package(self, name, version, outdir):
        """Download package files."""

        # TODO: reimplement with Slice.download_package()
        # self.slice.download_package(name, version, outdir)
        def get_pkg_id(pkgs, name, version):
            """Look up package ID from list of package infos."""
            for pinfo in pkgs:
                if pinfo["name"] == name and pinfo["version"] == version:
                    return "%(name)s/%(version)s/%(id)s" % pinfo
            raise DerekError("No package %s %s in the branch" % (name, version))

        pkg = self._client.getjson(path="/packages/%s" %
                                    get_pkg_id(self.packages, name, version))
        for pfile in pkg['files']:
            self._client.download(path="/users/%(username)s/repos/%(reponame)s/"
                                       "slices/%(slice_id)s/"
                                       "%(name)s/%(version)s/%(filename)s" %
                                       {
                                           "username": self.username,
                                           "reponame": self.reponame,
                                           "slice_id": self.slice.hash,
                                           "name":     name,
                                           "version":  version,
                                           "filename": pfile["name"]
                                       },
                                  out=os.path.join(outdir, pfile["name"]))
        LOG.debug("Package download complete")

    @property
    def slice(self):
        """Return current slice."""

        if self._slice:
            return self._slice

        LOG.debug("Branch doc hasn't been cached. Loading...")
        self._load()
        return self._slice

    @property
    def packages(self):
        """Return current list of packages in the branch."""

        if self._packages:
            return self._packages

        self._load()
        return self._packages

