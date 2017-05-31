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

class SignedOffBy(base.Base):

    revert_shortlog_regex = re.compile('Revert\s+".*"')

    @classmethod
    def setUpClassLocal(cls):
        # match self.mark with no '+' preceding it
        cls.mark = str(parse_signed_off_by.signed_off_by_mark).strip('"')
        cls.prog = re.compile("(?<!\+)%s" % cls.mark)

    def test_signed_off_by_presence(self):
        for commit in SignedOffBy.commits:
            # skip those patches that revert older commits, these do not required the tag presence
            if self.revert_shortlog_regex.match(commit.shortlog):
                continue
            if not SignedOffBy.prog.search(commit.payload):
                self.fail('Patch is missing Signed-off-by',
                          'Sign off the patch (either manually or with "git commit --amend -s")',
                          commit)
