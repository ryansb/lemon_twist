from setuptools import setup

from lemon import __version__

setup(name='lemon',
      version=__version__,
      description="A Twisted take on a classic Drink.",
      long_description="",
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[],
      keywords='',
      author='Ryan S. Brown',
      author_email='sb@ryansb.com',
      url='http://github.com/ryansb/lemon_twist',
      scripts=['bin/lemontwist'],
      package_data={'conf': 'lemon.example.cfg'},
      license='MIT',
      packages=['lemon', 'lemon.peel', 'lemon.meringue', 'lemon.twist', 'lemon.test'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          "twisted",
          "sqlalchemy",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
