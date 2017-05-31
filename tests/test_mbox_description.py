# Checks related to the patch's commit_message
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

class CommitMessage(base.Base):

    def test_commit_message_presence(self):
        self.skip('Until general agreement with the community, disabling it')
        for commit in CommitMessage.commits:
            if not commit.commit_message.strip():
                self.fail('Patch is missing a descriptive commit message',
                          'Please include a commit message on your patch explaining the change (most importantly why the change is being made)',
                          commit)

