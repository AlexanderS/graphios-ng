#!/usr/bin/env python
from setuptools import setup

# get version
with open('graphios_ng/version.py') as version_file:
    exec(version_file.read())

setup(
    name='graphios-ng',
    version=__version__,
    author='Alexander Sulfrian',
    include_package_data=True,
    extras_require=dict(
        test=[
            'pep8',
            'pylint',
        ],
    ),
    install_requires=[
        'pyyaml',
        'pyinotify',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'graphios = graphios_ng.graphios:main'
        ]
    }
)
