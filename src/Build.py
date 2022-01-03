# ----------------------------------------------------------------------
# |
# |  Build.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-04-17 15:21:33
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-22
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Builds the boost libraries"""

import os
import sys

import CommonEnvironment
from CommonEnvironment import BuildImpl
from CommonEnvironment import CommandLine
from CommonEnvironment.StreamDecorator import StreamDecorator

from CommonBoost import BoostBuildImpl

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

_boost_root                                 = os.getenv("DEVELOPMENT_ENVIRONMENT_BOOST_ROOT")
_is_standard_configuration                  = os.getenv("DEVELOPMENT_ENVIRONMENT_BOOST_IS_STANDARD_CONFIGURATION") == "1"

# ----------------------------------------------------------------------
Build                                       = BoostBuildImpl.CreateBuild(_boost_root, _is_standard_configuration)
Clean                                       = BoostBuildImpl.CreateClean(_boost_root)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        sys.exit(BuildImpl.Main(BuildImpl.Configuration( name="boost",
                                                         requires_output_dir=False,
                                                       )))
    except KeyboardInterrupt:
        pass
