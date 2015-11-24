__all__= ["fc_install"]
__version__ = "0.1.5"

import os
import sys
import subprocess
import tempfile
from setuptools.command.install import install as dist_install

def get_freecad_path():
        if os.getuid() == 0:
            command = "FreeCAD.getHomePath()"
        else:
            command = "FreeCAD.getUserAppDataDir()"

        with open( tempfile.gettempdir() + "/get_freecad_app_data.py", "w") as fp:
            fp.write("print("+ command +")\nexit()")
            fp.close()
        try:
            a = subprocess.Popen("freecad -c "+ fp.name, shell=True, stdout=subprocess.PIPE, stderr=None)
            installation_path = str(a.stdout.readlines()[-1][:-2])
            while (installation_path[0] not in "C/"):
                installation_path = installation_path[1:]
            return installation_path + "/Mod"
        except:
            print("INSTALLATION ERROR: this package needs freecad to be installed")
            sys.exit()


def check():
    pass


class fc_install(dist_install):
    """add the freecad installation at the end of the install
    - create a start_python_extern directory in the get_freecad_path()
    - create a Init.py and a InitGui.py file (these files get executed (exec) at freecad startup
        here we place the information to get our module started. This have to be a exec() for importing
        the InitGui.py and Init.py of our module. Import won't work because of some decision of 
        how freecad loads modules at startup. Consider some strange python behaviour with these 
        files. (eg. class workbench can be used without an import) because it is defined in the file
        where the exec comes from."""

    def if_not_exist_create_file(self, path, text=None, force=False, first_line=None):
        print(text)
        if not os.path.exists(path) or force:
            with open(path, "w") as fp:
                if text:
                    with open(text) as in_file:
                        if first_line:
                            fp.write(first_line)
                        txt = in_file.read()
                        fp.write(txt)

    def if_not_exist_create_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)


    def run(self):
        DIR = os.path.dirname(__file__) + "/"
        fcad_py_ex_path = get_freecad_path() + "/start_python_extern" + str(os.getuid())
        init_path = fcad_py_ex_path + "/Init.py"
        initgui_path = fcad_py_ex_path + "/InitGui.py"
        package_path = fcad_py_ex_path + "/packages.txt"
        apply_line = "packages_txt = '" + package_path + "'\n"
        self.if_not_exist_create_dir(fcad_py_ex_path)
        self.if_not_exist_create_file(init_path, text=DIR + "Init.py",
                                      force=True, first_line=apply_line)
        self.if_not_exist_create_file(initgui_path, text=DIR + "InitGui.py",
                                      force=True, first_line=apply_line)
        self.if_not_exist_create_file(package_path)
        if os.getuid() == 0:
            uid = int(os.environ.get('SUDO_UID'))
            gid = int(os.environ.get('SUDO_GID'))
            os.chown(package_path, uid, gid)

        dist_install.run(self)
        package_name = self.distribution.packages[0]
        append_name = True
        with open(package_path, "r") as package_file:
            for line in package_file:
                if package_name in line:
                    append_name = False
                    break
        if append_name:
            with open(package_path, "a") as package_file:
                package_file.write(package_name + "\n")
