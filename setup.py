from distutils.core import setup
import freecad_dist

setup(name='freecad_dist',
      version= freecad_dist.__version__,
      description='custom installer for freecad workbenches',
      author='looooo',
      url='https://github.com/looooo/freecad_dist',
      license='GPL3',
      packages=["freecad_dist"])

