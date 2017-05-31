# Checks related to the patch's bugzilla tag
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

import re
import base

class Bugzilla(base.Base):
    rexp_detect     = re.compile("\[.*YOCTO.*\]", re.IGNORECASE)
    rexp_validation = re.compile("\[(\s?YOCTO\s?#\s?(\d+)\s?,?)+\]", re.IGNORECASE)

    def test_bugzilla_entry_format(self):
        for commit in Bugzilla.commits:
            for line in commit.commit_message.splitlines():
                if self.rexp_detect.match(line):
                    if not self.rexp_validation.match(line):
                        self.fail('Yocto Project bugzilla tag is not correctly formatted',
                                  'Specify bugzilla ID in commit description with format: "[YOCTO #<bugzilla ID>]"',
                                  commit)

