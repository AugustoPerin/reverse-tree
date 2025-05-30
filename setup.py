#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="reverse-tree",
    version="1.0.0",
    author="Augusto Perin",
    author_email="augustooperin@gmail.com",
    description="A tool to create directory structures from tree format files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AugustoPerin/reverse-tree",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "reverse-tree=reverse_tree.main:main",
        ],
    },
)