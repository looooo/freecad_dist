__all__= ["fc_install"]
__version__ = "0.1.1"

import os
import subprocess
import tempfile

from setuptools.command.install import install as dist_install

class fc_install(dist_install):
    def initialize_options(self):
        dist_install.initialize_options(self)
        path = self.get_freecad_path()
        self.install_base = path
        self.install_lib = path
        self.install_headers = path
        self.install_scripts = path
        self.install_data = path

    def get_freecad_path(self):
        if os.getuid() == 0:
            command = "FreeCAD.getHomePath()"
        else:
            command = "FreeCAD.getUserAppDataDir()"

        with open( tempfile.gettempdir() + "/get_freecad_app_data.py", "w") as fp:
            fp.write("print("+ command +")\nexit()")
            fp.close()
        try:
            a = subprocess.Popen("freecad -c "+ fp.name, shell=True, stdout=subprocess.PIPE, stderr=None)
            installation_path = a.stdout.readlines()[-1][:-2]
            return installation_path + "/Mod"
        except:
            print("INSTALLATION ERROR: this package needs freecad to be installed")
            sys.exit()
