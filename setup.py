from setuptools import setup

setup(
    name             = 'aweber_tools',
    version          = '0.1',
    description      = 'AWeber API Python tools',
    author           = 'foo',
    maintainer       = 'bar',
    packages         = ['aweber_tools'],
    classifiers = [
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'future',
        'aweber_api'
    ]
)