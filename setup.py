from setuptools import setup

from lemontwist import __version__

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
      scripts=['bin/lemon'],
      license='MIT',
      packages=['lemon', 'lemon.peel', 'lemon.meringue', 'lemon.twist'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
