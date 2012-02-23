import rfc822

def line2dict(line):
    md5, size, section, priority, filename = line.split()
    return dict(md5=md5, size=size, section=section, priority=priority,
                filename=filename)

def deb_changes(filepath):
    """Parse .changes file.

    The code has been borrowed from the dput utility
    """

    with open(filepath, 'r') as chg_fd:
        if chg_fd.read(5) != '-----':
            chg_fd.seek(0)
        else: # found a PGP header, skip the next 3 lines
            chg_fd.readline() # eat the rest of the line
            chg_fd.readline() # Hash: SHA1
            chg_fd.readline() # empty line
        if not chg_fd.readline().find('Format') != -1:
            chg_fd.readline()
        changes = rfc822.Message(chg_fd)
        return dict(files=[line2dict(line)
                           for line in changes.dict['files'].splitlines()])
