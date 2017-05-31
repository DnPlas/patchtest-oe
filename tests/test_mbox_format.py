# Checks correct parsing of mboxes
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

class MboxFormat(base.Base):

    def test_mbox_format(self):
        if self.unidiff_parse_error:
            self.fail('Series cannot be parsed correctly due to malformed diff lines',
                      'Create the series again using git-format-patch and ensure it can be applied using git am',
                      data=[('Diff line', re.sub('^.+:','',self.unidiff_parse_error))])
