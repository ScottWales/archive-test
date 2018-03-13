#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import versioneer

setup(
        name = 'archive',
        packages = find_packages('src'),
        package_dir = {'': 'src'},
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        install_requires = [
            'click',
            'sqlalchemy',
            ],
        entry_points = {
            'console_scripts': [
                'archive-test = archive.cli:cli',
                ]}
        )
