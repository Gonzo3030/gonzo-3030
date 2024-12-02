from setuptools import setup, find_packages

setup(
    name="gonzo-3030",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'pytest>=7.4.3',
        'pytest-cov>=4.1.0',
        'pytest-mock>=3.12.0',
        'pytest-asyncio>=0.21.1',
        'pytest-env>=1.1.1',
        'hypothesis>=6.87.1',
        'factory-boy>=3.3.0',
        'pytest-xdist>=3.3.1',
        'freezing>=2.4.0',
    ],
)