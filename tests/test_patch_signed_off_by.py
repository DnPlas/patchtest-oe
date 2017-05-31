# Checks related to the patch's signed-off-by lines
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
import parse_signed_off_by
import re

class PatchSignedOffBy(base.Base):

    @classmethod
    def setUpClassLocal(cls):
        cls.newpatches = []
        # get just those relevant patches: new software patches
        for patch in cls.patchset:
            if patch.path.endswith('.patch') and patch.is_added_file:
                cls.newpatches.append(patch)

        cls.mark = str(parse_signed_off_by.signed_off_by_mark).strip('"')

        # match PatchSignedOffBy.mark with '+' preceding it
        cls.prog = re.compile("(?<=\+)%s" % cls.mark)

    def setUp(self):
        if self.unidiff_parse_error:
            self.skip('Parse error %s' % self.unidiff_parse_error)

    def test_signed_off_by_presence(self):
        if not PatchSignedOffBy.newpatches:
            self.skip("There are no new software patches, no reason to test %s presence" % PatchSignedOffBy.mark)

        for newpatch in PatchSignedOffBy.newpatches:
            payload = newpatch.__str__()
            for line in payload.splitlines():
                if self.patchmetadata_regex.match(line):
                    continue
                if PatchSignedOffBy.prog.search(payload):
                    break
            else:
                self.fail('A patch file has been added, but does not have a Signed-off-by tag',
                          'Sign off the added patch file (%s)' % newpatch.path)
