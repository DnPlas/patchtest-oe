# common pyparsing variables
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

# general
colon = pyparsing.Literal(":")
start = pyparsing.LineStart()
end   = pyparsing.LineEnd()
at = pyparsing.Literal("@")
lessthan = pyparsing.Literal("<")
greaterthan = pyparsing.Literal(">")
opensquare = pyparsing.Literal("[")
closesquare = pyparsing.Literal("]")

# word related
word = pyparsing.Word(pyparsing.alphas)
worddot = pyparsing.Word(pyparsing.alphas+".")
