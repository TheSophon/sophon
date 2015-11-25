#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
from sophon import __version__

tests_requirements = [
    "pytest >= 2.8.3, < 3.0.0",
    "pylint >= 1.4.4, < 2.0.0"
]

setup(
    name="sophon",
    version=__version__,
    url="https://github.com/TheSophon/sophon",
    license="MIT",
    description="Simple IT automation web service based on Ansible",
    long_description=open("README.md").read(),
    author="The Sophon",
    author_email="",
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    install_requires=[
        "tornado >= 4.3, < 5.0",
    ] + tests_requirements,
    tests_require=tests_requirements
)
