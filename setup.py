from setuptools import setup, find_packages
from pygeist import __version__

setup(
    name="pygeist",
    version=__version__,
    packages=find_packages(include=["pygeist*"]),
    python_requires=">=3.10",
    install_requires=open("requirements.txt").read().splitlines(),
    include_package_data=True,
    description="Pygeist server package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
