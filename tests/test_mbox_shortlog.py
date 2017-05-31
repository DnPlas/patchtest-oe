# Checks related to the patch's  summary
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
import parse_shortlog
import pyparsing

maxlength = 90

class Shortlog(base.Base):

    def test_shortlog_format(self):
        for commit in Shortlog.commits:
            shortlog = commit.shortlog
            if not shortlog.strip():
                self.skip('Empty shortlog, no reason to execute shortlog format test')
            else:
                # no reason to re-check on revert shortlogs
                if shortlog.startswith('Revert "'):
                    continue
                try:
                    parse_shortlog.shortlog.parseString(shortlog)
                except pyparsing.ParseException as pe:
                    self.fail('Shortlog does not follow expected format',
                              'Commit shortlog (first line of commit message) should follow the format "<target>: <summary>"',
                              commit)

    def test_shortlog_length(self):
        for commit in Shortlog.commits:
            # no reason to re-check on revert shortlogs
            shortlog = commit.shortlog
            if shortlog.startswith('Revert "'):
                continue
            l = len(shortlog)
            if l > maxlength:
                self.fail('Commit shortlog is too long',
                          'Edit shortlog so that it is %d characters or less (currently %d characters)' % (maxlength, l),
                          commit)
