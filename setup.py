from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='googlecal',
    version='1.0.0',
    packages=['src'],
    install_requires=required,
    entry_points={
        'console_scripts': [
            'googlecal=src.client:googlecal'
        ]
    },
    license='LICENSE'
)
