#!/usr/bin/env python
# Install script for the isi-thorcam

import os
from os.path import join as pjoin
from setuptools import setup
from setuptools.command.install import install



longdescription = """
"""

setup(
    name = 'isi_thorcam',
    version = '0.1.8',
    author = 'Joao Couto',
    author_email = 'jpcouto@gmail.com',
    description = "We can't always get the camera we want...",
    long_description = longdescription,
    long_description_content_type='text/markdown',
    license = 'GPL',
    install_requires = [],
    url = "https://github.com/jcouto/isi-thorcam",
    packages = ['isi_thorcam'],
    entry_points = {
        'console_scripts': [
            'isi-thorcam = isi_thorcam.gui:main',
        ]
    },
)


