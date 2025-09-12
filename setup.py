from setuptools import setup, find_packages

setup(
    name="pygeist",
    version="0.1.2",
    packages=find_packages(include=["zeitgeist_server*"]),
    python_requires=">=3.8",
    install_requires=[],
    include_package_data=True,
    description="Pygeist server package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
