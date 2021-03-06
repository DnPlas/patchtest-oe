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
import re
import patchtestdata
from patchtestdata import PatchTestInput as pti

class LicFilesChkSum(base.Metadata):
    metadata = 'LIC_FILES_CHKSUM'
    license  = 'LICENSE'
    closed   = 'CLOSED'
    licmark  = re.compile('%s|%s|CHECKSUM|CHKSUM' % (metadata, license), re.IGNORECASE)

    def setUp(self):
        # these tests just make sense on patches that can be merged
        if not pti.repo.canbemerged:
            self.skip('Patch cannot be merged')

    def test_lic_files_chksum_presence(self):
        if not self.added:
            self.skip('No added recipes, skipping test')

        for pn in self.added:
            rd = self.tinfoil.parse_recipe(pn)
            pathname = rd.getVar('FILE')
            # we are not interested in images
            if '/images/' in pathname:
                continue
            lic_files_chksum = rd.getVar(self.metadata)
            if rd.getVar(self.license) == self.closed:
                continue
            if not lic_files_chksum:
                self.fail('%s is missing in newly added recipe' % self.metadata,
                          'Specify the variable %s in %s' % (self.metadata, pn))

    def pretest_lic_files_chksum_modified_not_mentioned(self):
        if not self.modified:
            self.skip('No modified recipes, skipping pretest')
        # get the proper metadata values
        for pn in self.modified:
            rd = self.tinfoil.parse_recipe(pn)
            pathname = rd.getVar('FILE')
            # we are not interested in images
            if '/images/' in pathname:
                continue
            patchtestdata.PatchTestDataStore['%s-%s-%s' % (self.shortid(),self.metadata,pn)] = rd.getVar(self.metadata)

    def test_lic_files_chksum_modified_not_mentioned(self):
        if not self.modified:
            self.skip('No modified recipes, skipping test')

        # get the proper metadata values
        for pn in self.modified:
            rd = self.tinfoil.parse_recipe(pn)
            pathname = rd.getVar('FILE')
            # we are not interested in images
            if '/images/' in pathname:
                continue
            patchtestdata.PatchTestDataStore['%s-%s-%s' % (self.shortid(),self.metadata,pn)] = rd.getVar(self.metadata)
        # compare if there were changes between pre-merge and merge
        for pn in self.modified:
            pretest = patchtestdata.PatchTestDataStore['pre%s-%s-%s' % (self.shortid(),self.metadata, pn)]
            test    = patchtestdata.PatchTestDataStore['%s-%s-%s' % (self.shortid(),self.metadata, pn)]

            # TODO: this is workaround to avoid false-positives when pretest metadata is empty (not reason found yet)
            # For more info, check bug 12284
            if not pretest:
                return

            if pretest != test:
                # if any patch on the series contain reference on the metadata, fail
                for commit in self.commits:
                    if self.licmark.search(commit.shortlog) or self.licmark.search(commit.commit_message):
                       break
                else:
                    self.fail('LIC_FILES_CHKSUM changed on target %s but there was no explanation as to why in the commit message' % pn,
                              'Provide a reason for LIC_FILES_CHKSUM change in commit message',
                              data=[('Current checksum', pretest), ('New checksum', test)])
