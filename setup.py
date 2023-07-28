
import setuptools
from setuptools import setup

setup(
    name='limbo',
    version='0.1',
    include_package_data=True,
    packages=setuptools.find_packages(),
    license='GPL 3',
    description="Shape optimization and data generation using CAD-CFD",
    long_description=open('README.md').read(),
    python_requires='>3.6',
    # do not list standard packages
    install_requires=[
        'numpy==1.20.3',
        'matplotlib',
        'numpy-stl',
        'kajiki',
        'pyDOE',
        'GPyOpt',
        'parea',
        'pandas'
            ],
    entry_points={
        'console_scripts': [
            'limbo = limbo.src.__main__:run'
        ]
    }
)
