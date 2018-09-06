# -*- coding:utf-8; -*-

#  SCons_PkgConfig – Support for using pkg-config command in SCons.
#
#  Copyright © 2018  Russel Winder
#
#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU
#  General Public License as published by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
#  the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
#  License for more details.
#
#  You should have received a copy of the GNU General Public License along with this program.  If not, see
#  <http://www.gnu.org/licenses/>.

import re
import subprocess

def get_pkgconfig_data(dependency, **kwargs):
    if 'version' in kwargs:
        matches = re.search(r'([><]?=)\s*([0-9]+\.[0-9]+\.[0-9]+)', kwargs['version'])
        if matches:
            relation, version_number = matches.group(1, 2)
            if relation == '>=':
                operation = 'atleast-version'
            elif relation == '<=':
                operation = 'max-version'
            elif relation == '=':
                operation = 'exact-version'
            else:
                raise Exception('Version number relation not in <=, =, >=.')
            if subprocess.run(('pkg-config', f'--{operation}={version_number}', dependency)).returncode != 0:
                raise Exception(f'Version number constraint for {dependency} not met.')
        else:
            print('Version number not parsable in expected structure.')
            return ([], [])
    cflags = subprocess.run(('pkg-config', '--cflags', dependency), stdout=subprocess.PIPE).stdout.decode().split()
    lflags = subprocess.run(('pkg-config', '--libs', dependency), stdout=subprocess.PIPE).stdout.decode().split()
    return (cflags, lflags)
