# Base class to be used by all test cases defined in the suite
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

import unittest
import logging
import json
import unidiff
from patchtestdata import PatchTestInput as pti
import mailbox
import collections
import sys, os
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pyparsing'))

logger = logging.getLogger('patchtest')
debug=logger.debug
info=logger.info
warn=logger.warn
error=logger.error

Commit = collections.namedtuple('Commit', ['author', 'subject', 'commit_message', 'shortlog', 'payload'])

class Base(unittest.TestCase):
    # if unit test fails, fail message will throw at least the following JSON: {"id": <testid>}

    endcommit_messages_regex = re.compile('\(From \w+-\w+ rev:|(?<!\S)Signed-off-by|(?<!\S)---\n')
    patchmetadata_regex   = re.compile('-{3} \S+|\+{3} \S+|@{2} -\d+,\d+ \+\d+,\d+ @{2} \S+')

    @classmethod
    def setUpClass(cls):

        def commit_message(payload):
            commit_message = payload.__str__()
            match = cls.endcommit_messages_regex.search(payload)
            if match:
                commit_message = payload[:match.start()]
            return commit_message

        def shortlog(shlog):
            # remove possible prefix (between brackets) before colon
            start = shlog.find(']', 0, shlog.find(':'))

            # remove also newlines and spaces at both sides
            return shlog[start + 1:].replace('\n', '').strip()

        # General objects: mailbox.mbox and patchset
        cls.mbox = mailbox.mbox(pti.repo.patch)

        # Patch may be malformed, so try parsing it
        cls.unidiff_parse_error = ''
        cls.patchset = None
        try:
            cls.patchset = unidiff.PatchSet.from_filename(pti.repo.patch, encoding=u'UTF-8')
        except unidiff.UnidiffParseError as upe:
            cls.patchset = []
            cls.unidiff_parse_error = str(upe)

        # Easy to iterate list of commits
        cls.commits = []
        for msg in cls.mbox:
            payload = msg.get_payload()
            subject = msg['subject']
            if  payload and subject:
                subject = subject.replace('\n', ' ').replace('  ', ' ')
                cls.commits.append(Commit(subject=subject,
                                   author=msg.get('From'),
                                   shortlog=shortlog(msg['subject']),
                                   commit_message=commit_message(payload),
                                   payload=payload))

        cls.setUpClassLocal()

    @classmethod
    def tearDownClass(cls):
        cls.tearDownClassLocal()

    @classmethod
    def setUpClassLocal(cls):
        pass

    @classmethod
    def tearDownClassLocal(cls):
        pass

    def fail(self, issue, fix=None, commit=None, data=None):
        """ Convert to a JSON string failure data"""
        value = {'id': self.id(),
                 'issue': issue}

        if fix:
            value['fix'] = fix
        if commit:
            value['commit'] = {'subject': commit.subject,
                               'shortlog': commit.shortlog}

        # extend return value with other useful info
        if data:
            value['data'] = data

        return super(Base, self).fail(json.dumps(value))

    def skip(self, issue, data=None):
        """ Convert the skip string to JSON"""
        value = {'id': self.id(),
                 'issue': issue}

        # extend return value with other useful info
        if data:
            value['data'] = data

        return super(Base, self).skipTest(json.dumps(value))

    def shortid(self):
        return self.id().split('.')[-1]

    def __str__(self):
        return json.dumps({'id': self.id()})
