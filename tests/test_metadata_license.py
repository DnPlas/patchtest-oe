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

import base
import os
from patchtestdata import PatchTestInput as pti

class License(base.Metadata):
    metadata = 'LICENSE'
    invalid_license = 'PATCHTESTINVALID'

    def setUp(self):
        # these tests just make sense on patches that can be merged
        if not pti.repo.canbemerged:
            self.skip('Patch cannot be merged')

    def test_license_presence(self):
        if not self.added:
            self.skip('No added recipes, skipping test')

        # TODO: this is a workaround so we can parse the recipe not
        # containing the LICENSE var: add some default license instead
        # of INVALID into auto.conf, then remove this line at the end
        auto_conf = os.path.join(os.environ.get('BUILDDIR'), 'conf', 'auto.conf')
        open_flag = 'w'
        if os.path.exists(auto_conf):
            open_flag = 'a'
        with open(auto_conf, open_flag) as fd:
            for pn in self.added:
                fd.write('LICENSE ??= "%s"\n' % self.invalid_license)

        self.tinfoil = base.setup_tinfoil()
        if not self.tinfoil:
            self.skip('Tinfoil could not be prepared, possible wrong oe-core repository path')

        try:
            no_license = False
            for pn in self.added:
                rd = self.tinfoil.parse_recipe(pn)
                license = rd.getVar(self.metadata)
                if license == self.invalid_license:
                    no_license = True
                    break

            # remove auto.conf line or the file itself
            if open_flag == 'w':
                os.remove(auto_conf)
            else:
                fd = open(auto_conf, 'r')
                lines = fd.readlines()
                fd.close()
                with open(auto_conf, 'w') as fd:
                    fd.write(''.join(lines[:-1]))
        finally:
            self.tinfoil.shutdown()

        if no_license:
            self.fail('Recipe does not have the LICENSE field set', 'Include a LICENSE into the new recipe')

