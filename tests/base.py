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
import sys
import os
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pyparsing'))

logger = logging.getLogger('patchtest')
debug=logger.debug
info=logger.info
warn=logger.warn
error=logger.error

Commit = collections.namedtuple('Commit', ['author', 'subject', 'commit_message', 'shortlog', 'payload'])

def get_metadata_stats(patchset):
    """Get lists of added, modified and removed metadata files"""
    # Matches PN and PV from a recipe filename
    pnpv = re.compile("(?P<pn>[a-zA-Z0-9\-]+)_?")

    added_paths = []
    modified_paths = []
    removed_paths  = []

    for patch in patchset:
        if patch.path.endswith('.bb') or patch.path.endswith('.bbappend') or patch.path.endswith('.inc'):
            if patch.is_added_file:
                added_paths.append(patch.path)
            elif patch.is_modified_file:
                modified_paths.append(patch.path)
            elif patch.is_removed_file:
                removed_paths.append(patch.path)

    added_matches    = [pnpv.match(os.path.basename(path)) for path in added_paths]
    modified_matches = [pnpv.match(os.path.basename(path)) for path in modified_paths]
    removed_matches  = [pnpv.match(os.path.basename(path)) for path in removed_paths]

    added = [(match.group('pn'), None) for match in added_matches if match]
    modified = [(match.group('pn'), None) for match in modified_matches if match]
    removed = [(match.group('pn'), None) for match in removed_matches if match]

    return added, modified, removed

def setup_tinfoil(config_only=False):
    """Initialize tinfoil api from bitbake"""

    tinfoil = None
    # import relevant libraries
    try:
        scripts_path = os.path.join(pti.repodir, 'scripts', 'lib')
        if scripts_path not in sys.path:
            sys.path.insert(0, scripts_path)
        import scriptpath
        scriptpath.add_bitbake_lib_path()
        import bb.tinfoil
    except ImportError:
        return tinfoil

    # Load tinfoil
    try:
        builddir = os.environ.get('BUILDDIR')
        if not builddir:
            logger.warn('Bitbake environment not loaded?')
            return tinfoil
        orig_cwd = os.path.abspath(os.curdir)
        os.chdir(builddir)
        tinfoil = bb.tinfoil.Tinfoil()
        tinfoil.prepare(config_only=config_only)
    except bb.tinfoil.TinfoilUIException as te:
        tinfoil.shutdown()
        tinfoil = None
    except:
        tinfoil.shutdown()
        raise
    finally:
        os.chdir(orig_cwd)

    return tinfoil

class Base(unittest.TestCase):
    # if unit test fails, fail message will throw at least the following JSON: {"id": <testid>}

    endcommit_messages_regex = re.compile('\(From \w+-\w+ rev:|(?<!\S)Signed-off-by|(?<!\S)---\n')
    patchmetadata_regex   = re.compile('-{3} \S+|\+{3} \S+|@{2} -\d+,\d+ \+\d+,\d+ @{2} \S+')


    @staticmethod
    def msg_to_commit(msg):
        payload = msg.get_payload()
        return Commit(subject=msg['subject'].replace('\n', ' ').replace('  ', ' '),
                      author=msg.get('From'),
                      shortlog=Base.shortlog(msg['subject']),
                      commit_message=Base.commit_message(payload),
                      payload=payload)

    @staticmethod
    def commit_message(payload):
        commit_message = payload.__str__()
        match = Base.endcommit_messages_regex.search(payload)
        if match:
            commit_message = payload[:match.start()]
        return commit_message

    @staticmethod
    def shortlog(shlog):
        # remove possible prefix (between brackets) before colon
        start = shlog.find(']', 0, shlog.find(':'))
        # remove also newlines and spaces at both sides
        return shlog[start + 1:].replace('\n', '').strip()

    @classmethod
    def setUpClass(cls):

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
            if msg['subject'] and msg.get_payload():
                cls.commits.append(Base.msg_to_commit(msg))

        # get info about added/modified/remove recipes
        cls.added, cls.modified, cls.removed = get_metadata_stats(cls.patchset)

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
