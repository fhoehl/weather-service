from setuptools import setup, find_packages

setup(
    name='weather',
    version='0.0.1',
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    zip_safe=True
)
