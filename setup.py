from setuptools import setup, find_packages

setup(
    name="saaschurn",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rich",
        "requests",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "saaschurn=saaschurn.cli:main",
        ],
    },
)
