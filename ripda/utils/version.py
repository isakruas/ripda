def get_version(version=None):
    version = tuple(str(i) for i in version)
    return '.'.join(version[0:4]) + version[4]
