# Check if mbox was merged by patchtest
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

import subprocess
import base
from patchtestdata import PatchTestInput as pti

def headlog():
    output = subprocess.check_output(
        "cd %s; git log --pretty='%%h#%%aN#%%cD:#%%s' -1" % pti.repodir,
        universal_newlines=True,
        shell=True
        )
    return output.split('#')

class Merge(base.Base):

    def test_series_merge_on_head(self):
        if not pti.repo.ismerged:
            commithash, author, date, shortlog = headlog()
            self.fail('Series does not apply on top of target branch',
                      'Rebase your series on top of targeted branch',
                      data=[('Targeted branch', '%s (currently at %s)' % (pti.repo.branch, commithash))])
