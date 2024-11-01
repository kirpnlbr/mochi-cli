from setuptools import setup, find_packages

setup(
    name="mochi-cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.28.0",
        "python-dotenv>=0.19.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "mochi=mochi_cli.cli:main",
        ],
    },
)