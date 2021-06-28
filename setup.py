from setuptools import setup, find_packages
import sys

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='funcargparse',
      version='0.2.4',
      description=(
          'Create an argparse.ArgumentParser from function docstrings'),
      long_description=readme(),
      long_description_content_type="text/x-rst",
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Documentation',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
      ],
      keywords=('argparse re docrep'),
      url='https://github.com/Chilipp/funcargparse',
      project_urls={
          'Documentation': 'https://funcargparse.readthedocs.io',
          'Source': 'https://github.com/Chilipp/psyplot',
          'Tracker': 'https://github.com/Chilipp/funcargparse/issues',
      },
      author='Philipp S. Sommer',
      author_email='philipp.sommer@hereon.de',
      license="Apache-2.0",
      packages=find_packages(exclude=['docs', 'tests*', 'examples']),
      include_package_data=True,
      install_requires=[
          'docrep>=0.3.0',
          'six',
      ],
      setup_requires=pytest_runner,
      tests_require=['pytest'],
      zip_safe=False)
