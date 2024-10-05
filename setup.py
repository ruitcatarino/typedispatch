from setuptools import setup, find_packages

setup(
    name="typedispatch",
    version="0.3.0",
    author="Rui Catarino",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ruitcatarino/typedispatch",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
)
