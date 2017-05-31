# Checks related to patch line lengths
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
import re

class MaxLength(base.Base):
    add_mark = re.compile('\+ ')
    max_length = 180

    def test_max_line_length(self):
        self.skip('Until general agreement with the community, disabling it')
        for patch in self.patchset:
            # for the moment, we are just interested in metadata
            if patch.path.endswith('.patch'):
                continue
            payload = str(patch)
            for line in payload.splitlines():
                if self.add_mark.match(line):
                    current_line_length = len(line[1:])
                    if current_line_length > self.max_length:
                        self.fail('Patch line too long (current length %s)' % current_line_length,
                                  'Shorten the corresponding patch line (max length supported %s)' % self.max_length,
                                  data=[('Patch', patch.path), ('Line', '%s ...' % line[0:80])])
