# freecad_dist
install freecad modules with distutils

## example setup.py file
```python
from freecad_dist import fc_install                 # custom freecad install
from distutils.core import setup

setup(cmdclass={'install': fc_install},
      install_requires=["numpy"],
      name='package_name',
      version='0.1',
      description='freecad workbench for my application',
      url='my_website',
      author='my_name',
      license='LGPL2',
      packages=["path_to_wb_directory"],
      package_data = {"": ["*.svg", "*.json"]})     # not std files (.py)
```

## upload to pypi-testing:
preparation for upload to pypi: http://peterdowns.com/posts/first-time-with-pypi.html

### register package
```bash
python setup.py register -r pypitest
```
### upload package
```bash
python setup.py sdist upload -r pypitest
```
### test install
```bash
 pip install -i https://testpypi.python.org/pypi <package name>
```

## upload to pypi:

### register package
```bash
python setup.py register -r pypi
```
### upload package
```bash
python setup.py sdist upload -r pypi
```
### install
```bash
 pip install <package name>
```