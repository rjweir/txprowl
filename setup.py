from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

setup(name='txprowl',
      version=version,
      description="Prowl support for Twisted",
      long_description="""""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Rob Weir',
      author_email='rweir@ertius.org',
      url='http://ertius.org/code/txprowl/',
      license='GNU GPL v2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
