from setuptools import find_packages, setup

import versioneer

setup(name='{{ pkg.pkgimp }}',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='{{ pkg.description }}',
      packages=['{{ pkg.pkgimp }}'],
      {% if pkg.requires %}
      install_requires='{{ pkg.requires }}',
      {% endif %}
      tests_require='pytest',
      zip_safe=False,
      include_package_data=True)
