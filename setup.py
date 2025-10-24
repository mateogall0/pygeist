from setuptools import setup, find_packages

setup(
    name="pygeist",
    version="0.3.0",
    packages=find_packages(include=["pygeist*"]),
    python_requires=">=3.10",
    install_requires=[],
    include_package_data=True,
    description="Pygeist server package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
