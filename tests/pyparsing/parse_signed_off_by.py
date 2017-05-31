# signed-off-by pyparsing definition
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


import pyparsing
import common

name = pyparsing.Regex('\S+.*(?= <)')
username = pyparsing.OneOrMore(common.worddot)
domain = pyparsing.OneOrMore(common.worddot)

# taken from https://pyparsing-public.wikispaces.com/Helpful+Expressions
email = pyparsing.Regex(r"(?P<user>[A-Za-z0-9._%+-]+)@(?P<hostname>[A-Za-z0-9.-]+)\.(?P<domain>[A-Za-z]{2,})")

email_enclosed = common.lessthan + email + common.greaterthan

signed_off_by_mark = pyparsing.Literal("Signed-off-by")
signed_off_by = common.start + signed_off_by_mark + common.colon + name + email_enclosed + common.end
