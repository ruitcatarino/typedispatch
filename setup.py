import os
from setuptools import setup, find_packages

version = os.getenv("PACKAGE_VERSION", "0.0.1")

setup(
    name="typedispatch",
    version=version,
    author="Rui Catarino",
    description="TypeDispatch is a Python utility for registering and dispatching functions based on object types and predicates, supporting inheritance through method resolution order (MRO).",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ruitcatarino/typedispatch",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
)
