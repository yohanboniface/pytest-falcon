from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

import pytest_falcon

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def is_pkg(line):
    return line and not line.startswith(('--', 'git', '#'))

with open('requirements.txt', encoding='utf-8') as reqs:
    install_requires = [l for l in reqs.read().split('\n') if is_pkg(l)]

setup(
    name='pytest-falcon',
    version=pytest_falcon.__version__,
    description=pytest_falcon.__doc__,
    long_description=long_description,
    url=pytest_falcon.__homepage__,
    author=pytest_falcon.__author__,
    author_email=pytest_falcon.__contact__,
    license='WTFPL',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: GIS',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='pytest falcon testing unittests',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    extras_require={'test': ['pytest']},
    include_package_data=True,
    entry_points={'pytest11': ['falcon = pytest_falcon.plugin']},
)
