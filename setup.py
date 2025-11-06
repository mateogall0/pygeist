from setuptools import setup, find_packages
import pathlib
import re


init_file = pathlib.Path("pygeist/__init__.py").read_text()


version_match = re.search(r'__version__\s*=\s*"([^"]+)"', init_file)
if not version_match:
    raise RuntimeError("Unable to find version string in pygeist/__init__.py.")

v = version_match.group(1)

setup(
    name="pygeist",
    version=v,
    packages=find_packages(include=["pygeist*"]),
    python_requires=">=3.10",
    install_requires=open("requirements.txt").read().splitlines(),
    include_package_data=True,
    description="Pygeist server package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
