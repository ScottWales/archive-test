#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import versioneer

setup(
        name = 'archive',
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        )
