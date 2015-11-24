import imp
path_list = []
package_list = []
with open(packages_txt, 'r') as package_file:
    for package in package_file:
        package = package.replace("\n", "")
        try:
            path = os.path.realpath(imp.find_module(package)[1])
            package_list.append(package)
            path_list.append(path)
        except ImportError:
            print('package ' + package + ' not found')
for path in path_list:
    with open(path + '/InitGui.py') as init_file:
        exec(init_file.read())
with open(packages_txt, 'w') as package_file:
    for package in package_list:
        package_file.write(package + "\n")