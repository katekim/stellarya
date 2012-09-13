version = (0, 0, 1, 1)
versionStr = "%d.%d.%d%s" % (
    version[0],
    version[1],
    version[2],
    ("." + str(version[3])) if version[3] > 0 else "")
versionInt = version[0] * 1000 * 1000 * 1000 + \
             version[1] * 1000 * 1000 + \
             version[2] * 1000 + \
             version[3]
