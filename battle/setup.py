#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
        name='Programming Battle',
        version='1.0.0',
        install_requires=[
            'tornado',
            'sqlalchemy',
            'psycopg2',
            'pyyaml',
            'pytz',
            'Pygments',
        ],
        packages=find_packages()
)

