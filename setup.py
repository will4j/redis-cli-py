#!/usr/bin/env python
from setuptools import find_packages, setup
setup(
    name="redis-cli",
    packages=find_packages(
        include=[
            "redis_cli",
        ]
    )
)
