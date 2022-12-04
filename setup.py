#!/usr/bin/env python
from setuptools import find_packages, setup
setup(
    name="redis-cli",
    version="0.1.1",
    packages=find_packages(
        include=[
            "redis_cli",
        ]
    )
)
