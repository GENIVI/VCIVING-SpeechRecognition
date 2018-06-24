from setuptools import setup

setup(name='emucorebrain',
      version='0.3',
      description='Brain of EmulationCore',
      url='https://github.com/GENIVI/GENIVI-GSoC-18/tree/master/Brain/core',
      author='Chandeepa Dissanayake',
      author_email='chandeepadissanayake@gmail.com',
      license='Mozilla Public License 2.0',
      packages=['emucorebrain.consts', 'emucorebrain.core', 'emucorebrain.data', 'emucorebrain.data.abstracts', 'emucorebrain.data.models', 'emucorebrain.keywords'],
      zip_safe=False
)
