#!/usr/bin/env python
from setuptools import setup, find_packages  
from codecs import open
from os import path

package_root_dir = path.abspath(path.dirname(__file__))

with open(path.join(package_root_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'labtools',
    version = open('VERSION').readline().strip(),

    keywords = 'research psychology experiments',
    description = 'Resources for running behavioral experiments',
    long_description = long_description,
    url = 'https://github.com/pedmiston/labtools',
    
    author = 'Pierce Edmiston',
    author_email = 'pierce.edmiston@gmail.com',
    
    license = 'GNU GPL',
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
    ],
    
    packages = find_packages(exclude=['contrib', 'docs', '*.tests*']),
    install_requires=['pandas', 'numpy']
)
