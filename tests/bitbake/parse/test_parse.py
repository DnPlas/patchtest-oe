import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from oediff import OEDiff
from patchtestdata import PatchTestInput as pti
from subprocess import check_output, CalledProcessError, STDOUT
from os.path import basename
from re import compile
from oebase import warn
import bitbakemsg as msg

def bitbake_check_output(args):
    bitbake_cmd = 'bitbake %s' % ' '.join(args)

    # change dir, prepare system and exec bitbake
    cmd = 'cd %s;source %s/oe-init-build-env;%s' % (pti.repodir,
                                                    pti.repodir,
                                                    bitbake_cmd)
    return check_output(cmd, stderr=STDOUT, shell=True)

class OEBitbakeParse(OEDiff):

    @classmethod
    def setUpClassLocal(cls):
        cls.newrecipes = []
        cls.modifiedrecipes = []
        # get just those patches touching python files
        for patchset in cls.patchsets:
            for patch in patchset:
                if patch.path.endswith('.bb') or patch.path.endswith('.bbappend'):
                    if patch.is_added_file:
                        cls.newrecipes.append(patch)
                    elif patch.is_modified_file:
                        cls.modifiedrecipes.append(patch)

    def pretest_bitbake_parse(self):
        try:
            bitbake_check_output(['-p'])
        except CalledProcessError as e:
            raise self.fail(self.formaterror(msg.pretest_bitbake_parse.reason,
                                             msg.pretest_bitbake_parse.error,
                                             msg.pretest_bitbake_parse.fix))

    def test_bitbake_parse(self):
        try:
            bitbake_check_output(['-p'])
        except CalledProcessError as e:
            raise self.fail(self.formaterror(msg.test_bitbake_parse.reason,
                                             msg.test_bitbake_parse.error,
                                             msg.test_bitbake_parse.fix))

    def pretest_bitbake_environment(self):
        try:
            bitbake_check_output(['-e'])
        except CalledProcessError as e:
            raise self.fail(self.formaterror(msg.pretest_bitbake_environment.reason,
                                             msg.pretest_bitbake_environment.error,
                                             msg.pretest_bitbake_environment.fix))

    def test_bitbake_environment(self):
        try:
            bitbake_check_output(['-e'])
        except CalledProcessError as e:
            raise self.fail(self.formaterrror(msg.test_bitbake_environment.reason,
                                              msg.test_bitbake_environment.error,
                                              msg.test_bitbake_environment.fix))

    def pretest_bitbake_environment_on_target(self):
        if not OEBitbakeParse.modifiedrecipes:
            self.skipTest(msg.bitbake.patch_has_no_bbfiles)

        prog = compile("(?P<pn>^[a-zA-Z]+)")
        pn_pv_list = [basename(recipe.path) for recipe in OEBitbakeParse.modifiedrecipes]
        pn_list = [(pn_pv, prog.match(pn_pv)) for pn_pv in pn_pv_list]

        for pn_pv, match in pn_list:
            if not match:
                warn('Target name cannot be extracted from %s' % pn_pv)
            else:
                pn = match.group('pn')
                try:
                    bitbake_check_output(['-e', pn])
                except CalledProcessError as e:
                    raise self.fail(self.formaterror(msg.pretest_bitbake_environment_on_target.reason,
                                                     msg.pretest_bitbake_environment_on_target.error,
                                                     msg.pretest_bitbake_environment_on_target.fix))

    def test_bitbake_environment_on_target(self):
        prog = compile("(?P<pn>^[a-zA-Z]+)")
        pn_pv_list = [basename(recipe.path) for recipe in OEBitbakeParse.modifiedrecipes]
        pn_list = [(pn_pv, prog.match(pn_pv)) for pn_pv in pn_pv_list]

        for pn_pv, match in pn_list:
            if not match:
                warn('Target name cannot be extracted from %s' % pn_pv)
            else:
                pn = match.group('pn')
                try:
                    bitbake_check_output(['-e', pn])
                except CalledProcessError as e:
                    raise self.fail(self.formaterror(msg.test_bitbake_environment_on_target.reason,
                                                     msg.test_bitbake_environment_on_target.error,
                                                     msg.test_bitbake_environment_on_target.fix))
