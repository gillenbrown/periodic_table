from setuptools import setup, find_packages

setup(
    name="periodic_table",
    version="1.0.0",
    author="Gillen Brown",
    author_email="gillenbrown@gmail.com",
    packages=find_packages(exclude=["tests"]),
    install_requires=["numpy", "betterplotlib", "matplotlib"],
)
