#!/usr/bin/env python3
"""Setup module for pint"""

# Copyright (c) 2015 SUSE LLC, Robert Schweikert <rjschwei@suse.com>
#
# This file is part of ec2uploadimg.
#
# ec2uploadimg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ec2uploadimg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ec2uploadimg. If not, see <http://www.gnu.org/licenses/>.

import os
import sys

try:
    import setuptools
except ImportError:
    sys.stderr.write('Python setuptools required, please install.')
    sys.exit(1)


this_path = os.path.dirname(os.path.abspath(__file__))
mod_path = this_path + os.sep + 'lib/susepubliccloudinfoclient'
sys.path.insert(0, mod_path)

import version
src_version = version.VERSION

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as req_file:
    requirements = req_file.read().splitlines()

with open('requirements-dev.txt') as req_file:
    dev_requirements = req_file.read().splitlines()[2:]

description = 'Command-line tool to access SUSE Public Cloud Information '
description += 'Service'

if __name__ == '__main__':
    setuptools.setup(
        name='susepubliccloudinfo',
        description=(description),
        long_description=readme,
        long_description_content_type="text/markdown",
        url='https://github.com/SUSE-Enceladus/public-cloud-info-client',
        license='GPL-3.0+',
        author='SUSE Public Cloud Team',
        author_email='public-cloud-dev@susecloud.net',
        version=src_version,
        install_requires=requirements,
        extras_require={
            'dev': dev_requirements
        },
        include_package_data=True,
        packages=setuptools.find_packages('lib'),
        package_dir={
            '': 'lib',
        },
        scripts=['bin/pint'],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'License :: OSI Approved :: '
            'GNU General Public License v3 or later (GPLv3+)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
        ]
    )
