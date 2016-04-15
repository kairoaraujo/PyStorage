#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
from os.path import dirname, join
from setuptools import setup, find_packages

with open(join(dirname(__file__), 'pystorage/VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name="PyStorage",
    version=version,
    description="Python Storage Disk Toolkit (EMC VNX, EMC VMAX and IBM DS8K)",
    long_description=open('README.rst').read(),
    author="Kairo Araujo",
    author_email="kairo@kairo.eti.br",
    maintainer="Kairo Araujo",
    maintainer_email="kairo@kairo.eti.br",
    url="https://github.com/kairoaraujo/PyStorage/",
    keywords="Python Storage Disk EMC VMX VNX IBM DS800 DS8K Toolkit",
    packages=find_packages(exclude=['*.test', 'tests.*']),
    package_data={'': ['license.txt', 'pystorage/VERSION']},
    include_package_data=True,
    license='BSD',
    platforms='Posix; MacOS X; Windows',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: System :: Archiving',
        'Topic :: System :: Hardware',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
