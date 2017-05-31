# Checks related to the patch's LIC_FILES_CHKSUM  metadata variable
#
# Copyright (C) 2016 Intel Corporation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import bitbake
import re
import patchtestdata
import subprocess

class License(bitbake.Bitbake):
    metadata = 'LICENSE'

    def test_license_presence(self):
        if not self.added_pnpvs:
            self.skip('No added recipes, skipping test')

        for pn,pv in self.added_pnpvs:
            try:
                bitbake.bitbake(['-e', pn])
            except subprocess.CalledProcessError as e:
                for lines in e.output.split('\n'):
                    if 'This recipe does not have the LICENSE field set' in lines:
                         self.fail('Recipe does not have the LICENSE field set',
                                   'Include a LICENSE into the new recipe')
                self.skip('Target %s cannot be parse by bitbake' % pn)

