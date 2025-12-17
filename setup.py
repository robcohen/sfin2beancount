#!/usr/bin/env python
from distutils.core import setup

setup(
    name='sfin2beancount',
    version='0.1.0',
    description='SimpleFIN to Beancount formatter',
    author='Rob Cohen',
    author_email='rob@robcohen.io',
    packages=[],
    py_modules=['sfin2beancount'],
    package_data={},
    install_requires=[
        'argparse',
    ],
    scripts=[
        'sfin2beancount',
    ]
)
