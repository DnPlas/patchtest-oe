# Checks related to the patch's SRC_URI metadata variable
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

import patchtestdata
import subprocess
import base
import re
import os
from patchtestdata import PatchTestInput as pti

class SrcUri(base.Metadata):

    metadata  = 'SRC_URI'
    md5sum    = 'md5sum'
    sha256sum = 'sha256sum'
    git_regex = re.compile('^git\:\/\/.*')

    def setUp(self):
        # these tests just make sense on patches that can be merged
        if not pti.repo.canbemerged:
            self.skip('Patch cannot be merged')

    def pretest_src_uri_left_files(self):
        if not self.modified:
            self.skip('No modified recipes, skipping pretest')

        # get the proper metadata values
        for pn in self.modified:
            # we are not interested in images
            if 'core-image' in pn:
                continue
            rd = self.tinfoil.parse_recipe_file(pn)
            patchtestdata.PatchTestDataStore['%s-%s-%s' % (self.shortid(), self.metadata, pn)] = rd.getVar(self.metadata)

    def test_src_uri_left_files(self):
        if not self.modified:
            self.skip('No modified recipes, skipping pretest')

        # get the proper metadata values
        for pn in self.modified:
            # we are not interested in images
            if 'core-image' in pn:
                continue
            rd = self.tinfoil.parse_recipe(pn)
            patchtestdata.PatchTestDataStore['%s-%s-%s' % (self.shortid(), self.metadata, pn)] = rd.getVar(self.metadata)

        for pn in self.modified:
            pretest_src_uri = patchtestdata.PatchTestDataStore['pre%s-%s-%s' % (self.shortid(), self.metadata, pn)].split()
            test_src_uri    = patchtestdata.PatchTestDataStore['%s-%s-%s' % (self.shortid(), self.metadata, pn)].split()

            pretest_files = set([os.path.basename(patch) for patch in pretest_src_uri if patch.startswith('file://')])
            test_files    = set([os.path.basename(patch) for patch in test_src_uri    if patch.startswith('file://')])

            # check if files were removed
            if len(test_files) < len(pretest_files):

                # get removals from patchset
                filesremoved_from_patchset = set()
                for patch in self.patchset:
                    if patch.is_removed_file:
                        filesremoved_from_patchset.add(os.path.basename(patch.path))

                # get the deleted files from the SRC_URI
                filesremoved_from_usr_uri = pretest_files - test_files

                # finally, get those patches removed at SRC_URI and not removed from the patchset
                # TODO: we are not taking into account  renames, so test may raise false positives
                not_removed = filesremoved_from_usr_uri - filesremoved_from_patchset
                if not_removed:
                    self.fail('Patches not removed from tree',
                              'Amend the patch containing the software patch file removal',
                              data=[('Patch', f) for f in not_removed])

    def pretest_src_uri_checksums_not_changed(self):
        # get the proper metadata values
        for pn in self.modified:
            patchtestdata.PatchTestDataStore['%s-%s-sums' % (self.shortid(), pn)] = dict()
            rd = self.tinfoil.parse_recipe(pn)
            src_uri = rd.getVar(self.metadata)
            patchtestdata.PatchTestDataStore['%s-%s-%s' % (self.shortid(), self.metadata, pn)] = src_uri
            for uri in src_uri.split():
                 if not 'file:' in uri:
                     if self.git_regex.match(uri):
                         self.skip('No need to test SRC_URI checksums on a git source')
            for s in [self.md5sum, self.sha256sum]:
                for flag in rd.getVarFlags(self.metadata):
                    if s in flag:
                        patchtestdata.PatchTestDataStore['%s-%s-sums' % (self.shortid(), pn)][flag] = rd.getVarFlag(self.metadata, flag)

    def test_src_uri_checksums_not_changed(self):
        # get the proper metadata values
        for pn in self.modified:
            patchtestdata.PatchTestDataStore['%s-%s-sums' % (self.shortid(), pn)] = dict()
            rd = self.tinfoil.parse_recipe(pn)
            src_uri = rd.getVar(self.metadata)
            patchtestdata.PatchTestDataStore['%s-%s-%s' % (self.shortid(), self.metadata, pn)] = src_uri
            for s in [self.md5sum, self.sha256sum]:
                for flag in rd.getVarFlags(self.metadata):
                    if s in flag:
                        patchtestdata.PatchTestDataStore['%s-%s-sums' % (self.shortid(), pn)][flag] = rd.getVarFlag(self.metadata, flag)


        # loop on every src_uri and check if checksums change
        for pn in self.modified:
            pretest_src_uri = patchtestdata.PatchTestDataStore['pre%s-%s-%s' % (self.shortid(), self.metadata, pn)].split()
            test_src_uri    = patchtestdata.PatchTestDataStore['%s-%s-%s' % (self.shortid(), self.metadata, pn)].split()

            pretest_uri = set(uri.split(';')[0] for uri in pretest_src_uri if 'file:' not in uri)
            test_uri    = set(uri.split(';')[0] for uri in test_src_uri if 'file:' not in uri)

            if not pretest_uri:
                base.logger.warn('No SRC_URI found on %s' % pn)
            if not test_uri:
                base.logger.warn('No SRC_URI found on %s' % pn)

            if pretest_uri.difference(test_uri):
                # chksums must reflect the change
                for flag in patchtestdata.PatchTestDataStore['%s-%s-sums' % (self.shortid(), pn)].keys():
                    pretest_sum = patchtestdata.PatchTestDataStore['pre%s-%s-sums' % (self.shortid(), pn)][flag]
                    test_sum = patchtestdata.PatchTestDataStore['%s-%s-sums' % (self.shortid(), pn)][flag]
                    if pretest_sum == test_sum:
                        self.fail('SRC_URI changed but checksums are the same', 'Include the SRC_URI\'s checksums changes into your patch')
