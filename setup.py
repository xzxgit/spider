#! /usr/bin/env python

import sys

from setuptools import setup

setup_requires = ['setuptools', 'setuptools-git >= 0.3']

setup(name="spider",
      description="Crawling data from web sites.",
      long_description=open("README.rst").read(),
      version="1.0.0",
      packages=["spider"],
      python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
      setup_requires=setup_requires,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: BSD License",
          "License :: OSI Approved :: zlib/libpng License",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: Microsoft :: Windows",
          "Operating System :: POSIX",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Topic :: Software Development :: Build Tools",
          "Topic :: System :: Software Distribution"],
      zip_safe=True,
      entry_points={
          'console_scripts': ['spider=spider.__main__:main']
      },
      options={
          'bdist_wheel': {'universal': True},
      },
      platforms=['any'],
      )