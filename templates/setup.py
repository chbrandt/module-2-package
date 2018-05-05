from setuptools import find_packages, setup

import versioneer

setup(name='{{ pkg.pkgimp }}',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='{{ pkg.description }}',
      packages=['{{ pkg.pkgimp }}'],
      install_requires='{{ pkg.requires }}',
      zip_safe=False,
      include_package_data=True)
