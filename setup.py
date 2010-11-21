import os

from setuptools import setup, find_packages
setup(name='isotoma.plone.defang',
      version="1.0",
      packages=find_packages(),
      entry_points = {
        'console_scripts': ['defang=isotoma.plone.defang:main']
        },
      install_requires=['ZODB3'],
      zip_safe=False,
      include_package_data=True,
)
