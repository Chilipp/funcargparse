from setuptools import setup, find_packages
import sys

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='funcargparse',
      version='0.2.0',
      description=(
          'Create an argparse.ArgumentParser from function docstrings'),
      long_description=readme(),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Documentation',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
      ],
      keywords=('argparse re docrep'),
      url='https://github.com/Chilipp/funcargparse',
      author='Philipp Sommer',
      author_email='philipp.sommer@unil.ch',
      license="GPLv2",
      packages=find_packages(exclude=['docs', 'tests*', 'examples']),
      include_package_data=True,
      install_requires=[
          'docrep>=0.2.2',
          'six',
      ],
      setup_requires=pytest_runner,
      tests_require=['pytest'],
      zip_safe=False)
