#!/usr/bin/env python3

from setuptools import setup, find_packages


with open('requirements.txt') as req_file:
    install_requires = req_file.readlines()

dependency_links = []
setup_requires = []
extras_require = {}

setup(
    name = 'feizi-py',
    version = "0.0.1",
    description = '...',
    author = 'Sumit Nawathe',
    author_email = 'sumit.nawathe@gmail.com',
    packages = find_packages( exclude = [ "samples.*", "samples", "configs.*", "configs", "tests.*", "tests" ] ),
    package_data = { },
    install_requires = install_requires,
    setup_requires = setup_requires,
    extras_require = extras_require,
    dependency_links = dependency_links,
    test_suite = "tests",
    zip_safe = True,
    include_package_data = True
)
