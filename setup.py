from setuptools import setup, find_packages

setup(
    name             = 'aweber_tools',
    version          = '0.1.1',
    description      = 'AWeber API Python tools',
    packages         = find_packages(),
    classifiers = [
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'future',
        'aweber_api',
    ]
)