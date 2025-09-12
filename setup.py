from setuptools import setup, find_packages

setup(
    name="pygeist",
    version="0.1.1",
    packages=[],  # empty core package
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "server": ["zeitgeist_server"],  # treat this as extra
    },
    include_package_data=True,
    description="Pygeist server package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
