#!/usr/bin/env python
from setuptools import find_packages, setup
setup(
    name="redis_cli",
    description="Python client for Redis database and key-value store",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    keywords=["Redis", "key-value store", "database"],
    version="0.1.1",
    packages=find_packages(
        include=[
            "redis_cli",
        ]
    ),
    url="https://github.com/will4j/redis-cli-py",
    author="will4j",
    author_email="williamw0825@gmail.com",
    python_requires=">=3.7",
    install_requires=[
        "redis>=4.3.5",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
