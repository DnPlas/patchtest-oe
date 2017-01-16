#!/usr/bin/env python

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

class LicFilesChkSum(bitbake.Bitbake):
    metadata = 'LIC_FILES_CHKSUM'
    license  = 'LICENSE'
    closed   = 'CLOSED'
    licmark  = re.compile('%s|%s|CHECKSUM|CHKSUM' % (metadata, license), re.IGNORECASE)

    def test_lic_files_chksum_presence(self):
        if not self.added_pnpvs:
            self.skip('No added recipes, skipping test')

        # get the proper metadata values
        added_licsums = []
        for pn,pv in self.added_pnpvs:
            try:
                added_licsums.append(bitbake.getVar(self.metadata, pn))
            except subprocess.CalledProcessError:
                self.skip('Target %s cannot be parse by bitbake' % pn)

        for licsum in added_licsums:
            lic = bitbake.getVar(self.license, pn)
            if lic == self.closed:
                continue
            if not licsum:
                self.fail('%s is missing in newly added recipe' % self.metadata,
                          'Specify the variable %s in %s_%s' % (self.metadata, pn, pv))

    def pretest_lic_files_chksum_modified_not_mentioned(self):
        if not (self.modified_pnpvs + self.added_pnpvs):
            self.skip('No added or modified recipes, skipping pretest')

        # get the proper metadata values
        for pn,_ in self.modified_pnpvs + self.added_pnpvs:
            try:
                patchtestdata.PatchTestDataStore['%s-%s-%s' % (self.shortid(),self.metadata, pn)] = bitbake.getVar(self.metadata, pn)
            except subprocess.CalledProcessError:
                self.skip('Target %s cannot be parse by bitbake' % pn)

    def test_lic_files_chksum_modified_not_mentioned(self):
        if not (self.modified_pnpvs + self.added_pnpvs):
            self.skip('No modified or added recipes, skipping test')

        # get the proper metadata values
        for pn,_ in self.modified_pnpvs + self.added_pnpvs:
            try:
                patchtestdata.PatchTestDataStore['%s-%s-%s' % (self.shortid(),self.metadata, pn)] = bitbake.getVar(self.metadata, pn)
            except subprocess.CalledProcessError as cpe:
                self.skip('Target %s cannot be parse by bitbake' % pn)

        # compare if there were changes between pre-merge and merge
        for pn,_ in self.modified_pnpvs + self.added_pnpvs:
            pretest = patchtestdata.PatchTestDataStore['pre%s-%s-%s' % (self.shortid(),self.metadata, pn)]
            test    = patchtestdata.PatchTestDataStore['%s-%s-%s' % (self.shortid(),self.metadata, pn)]

            if pretest != test:
                # if any patch on the series contain reference on the metadata, fail
                for commit in self.commits:
                    if self.licmark.search(commit.shortlog) or self.licmark.search(commit.commit_message):
                       break
                else:
                    self.fail('LIC_FILES_CHKSUM changed on target %s but there was no explanation as to why in the commit message' % pn,
                              'Provide a reason for LIC_FILES_CHKSUM change in commit message')
