# Checks related to the patch's CVE lines
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
import re

class CVE(base.Base):

    re_cve_pattern = re.compile("CVE\-\d{4}\-\d+", re.IGNORECASE)
    re_cve_tag     = re.compile("CVE:(\s+CVE\-\d{4}\-\d+)+", re.IGNORECASE)

    def setUp(self):
        if self.unidiff_parse_error:
            self.skip('Parse error %s' % self.unidiff_parse_error)

        # we are just interested in series that introduce CVE patches, thus discard other
        # possibilities: modification to current CVEs, patch directly introduced into the
        # recipe, upgrades already including the CVE, etc.
        new_cves = [p for p in self.patchset if p.path.endswith('.patch') and p.is_added_file]
        if not new_cves:
            self.skip('No new CVE patches introduced')

    def test_cve_presence_in_commit_message(self):
        for commit in CVE.commits:
            if self.re_cve_pattern.search(commit.subject):
                if not self.re_cve_pattern.search(commit.commit_message):
                    self.fail('Missing or incorrectly formatted CVE tag in commit message',
                              'Include a "CVE-xxxx-xxxx" tag in the commit message',
                              commit)

    def test_cve_tag_format(self):
        for commit in CVE.commits:
            if self.re_cve_pattern.search(commit.shortlog):
                if not self.re_cve_tag.search(commit.payload):
                    self.fail('Missing or incorrectly formatted CVE tag in included patch file',
                              'Correct or include the CVE tag on cve patch with format: "CVE: CVE-YYYY-XXXX"',
                              commit)
