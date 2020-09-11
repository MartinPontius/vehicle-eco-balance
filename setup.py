import io

from pip._internal.req import parse_requirements
from setuptools import setup, find_packages

# loading requirements
requirements = list(parse_requirements('requirements.txt', session='hack'))
requirements = [r.requirement for r in requirements]


def parse_long_description():
    return io.open('README.md', encoding="utf-8").read()


setup(
    name="vehicle-eco-balance",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={
        "": ["*.txt"]
    },
    include_package_data=True,
    version="0.0.1",
    description="Python Utilities for estimating the eco balance of moving vehicles",
    long_description=parse_long_description(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/MartinPontius/vehicle-eco-balance",
    keywords=["trajectory", "energy consumption", "fuel consumption", "CO2 emissions", "xFCD", "enviroCar"],
    install_requires=requirements,
    test_suite="tests",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
