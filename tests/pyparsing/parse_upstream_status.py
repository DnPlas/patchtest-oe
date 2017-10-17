# upstream-status pyparsing definition
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


import common
import pyparsing

upstream_status_literal_valid_status = ["Pending", "Accepted", "Backport", "Denied", "Inappropriate", "Submitted"]
upstream_status_nonliteral_valid_status = ["Pending", "Accepted", "Backport", "Denied", "Inappropriate [reason]", "Submitted [where]"]

upstream_status_valid_status = pyparsing.Or(
    [pyparsing.Literal(status) for status in upstream_status_literal_valid_status]
)

upstream_status_mark         = pyparsing.Literal("Upstream-Status")
inappropriate_status_mark    = common.inappropriate
submitted_status_mark        = common.submitted

upstream_status              = common.start + upstream_status_mark + common.colon + upstream_status_valid_status
upstream_status_inappropriate_info = common.start + upstream_status_mark + common.colon + common.inappropriateinfo
upstream_status_submitted_info = common.start + upstream_status_mark + common.colon + common.submittedinfo
