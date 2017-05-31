# Checks related to the patch's summary metadata variable
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
import subprocess

class Summary(bitbake.Bitbake):
    metadata = 'SUMMARY'

    def test_summary_presence(self):
        # get the summaries
        added_summaries = []
        for pn,pv in self.added_pnpvs:
            try:
                added_summaries.append(bitbake.getVar(self.metadata, pn))
            except subprocess.CalledProcessError:
                self.skip('Target %s cannot be parse by bitbake' % pn)

        for summary in added_summaries:
            # "${PN} version ${PN}-${PR}" is the default, so fail if default
            if summary.startswith('%s version %s' % (pn, pv)):
                self.fail('%s is missing in newly added recipe' % self.metadata,
                          'Specify the variable %s in %s' % (self.metadata, pn))
