import glob, os, sys
from distutils.core import *

VERSION = "0.1"

def setupWin():

    sys.path.append(os.getcwd())

    dllsrc = r"C:\Python27\Lib\site-packages\PyQt4\plugins"

    import py2exe

    py2exe_opts = {
        'compressed' : False,
        'optimize' : 1,
        'bundle_files' : 3,
        'packages' : ["BeautifulSoup",
                      "sip"]
        }

    setup(name='stellarya-bin',
          options={'py2exe' : py2exe_opts},
          windows=[{
              'dest_base' : 'stellarya-bin',
              'script' : 'root/lib/site-packages/stellarya/Stellarya.py',
              'icon_resources' : [(1, 'root/lib/site-packages/stellarya/resources/stellarya.ico')]}],
          data_files = [
              ("codecs", glob.glob(os.path.join(dllsrc, "codecs", "*.dll"))),
              ("imageformats", glob.glob(os.path.join(dllsrc, "imageformats", "*.dll")))],
          zipfile="src.zip")

def setupUnix():
    setup(
        name = "stellarya",
        version = VERSION,
        packages = [
            'stellarya',
            'stellarya.action',
            'stellarya.resource',
            'stellarya.ui',
            ],

        package_dir = {
            'stellarya' : 'src/stellarya',
            'stellarya.action' : 'src/stellarya/action',
            'stellarya.resource' : 'src/stellarya/resource',
            'stellarya.ui' : 'src/stellarya/ui',
            },

        package_data = {
            'stellarya' : ["default.yaml"],
            'stellarya.resource' : ["*.png", "*.ico"],
            'stellarya.ui' : ["*.ui"],
            },
        )

if 'py2exe' in sys.argv:
    setupWin()
else:
    setupUnix()
