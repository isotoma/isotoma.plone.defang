import os

from setuptools import setup, find_packages
setup(name='isotoma.plone.defang',
      version="1.0.1",
      description="modify ZODBs for environment migration",
      long_description = open("README.rst").read() + "\n" + \
                         open("CHANGES.txt").read(),
      classifiers = [
        "Framework :: Buildout",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX",
        "License :: OSI Approved :: Apache Software License",
      ],
      packages=find_packages(),
      entry_points = {
        'console_scripts': ['defang=isotoma.plone.defang:main']
        },
      install_requires=['ZODB3'],
      zip_safe=False,
      include_package_data=True,
)
