# ----------------------------------------------------------------------
# |
# |  _custom_data.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-04-12 11:51:46
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Contains data used by both Setup_custom.py and Activate_custom.py"""

import os

import CommonEnvironment

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
#  ----------------------------------------------------------------------

_CUSTOM_DATA                                = [
    (
        "boost - 1.70.0",
        "0BC6EEB01484831568BB6BD0FDF92BEB9AD2CA9748DE9CF2C825FA12865B2DB0",
        [
            "Libraries",
            "C++",
            "boost",
            "v1.70.0",
        ],
    ),
]
