from setuptools import find_packages, setup

setup(
    name="langchain",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
)