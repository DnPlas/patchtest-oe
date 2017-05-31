# subject pyparsing definition
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

# NOTE:This is an oversimplified syntax of the mbox's summary

import pyparsing
import common

target        = pyparsing.OneOrMore(pyparsing.Word(pyparsing.printables.replace(':','')))
summary       = pyparsing.OneOrMore(pyparsing.Word(pyparsing.printables))
shortlog       = common.start + target + common.colon + summary + common.end
