#!/usr/bin/env python

from distutils.core import setup

setup(
    name='rraw',
    version='0.1 alpha',
    description='Super lightweight wrapper for the reddit API',
    author='Daniel Walsh',
    author_email='459dan@gmail.com',
    packages=['rraw'],
    install_requires=[
        'requests-oauthlib>=0.7.0',
    ],
)
