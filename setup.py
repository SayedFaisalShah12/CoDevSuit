from setuptools import setup, find_packages

setup(
    name="codev_suite",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "radon",
        "mccabe",
        "networkx",
        "rich",
        "google-generativeai",
        "python-dotenv",
        "click",
        "matplotlib",
        "plotly",
        "pandas",
    ],
    entry_points={
        "console_scripts": [
            "codev=codev_suite.cli.main:cli",
        ],
    },
)
