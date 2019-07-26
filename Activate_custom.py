# ----------------------------------------------------------------------
# |
# |  Activate_custom.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2018-05-07 08:59:57
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2018-19.
# |  Distributed under the Boost Software License, Version 1.0.
# |  (See accompanying file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# |
# ----------------------------------------------------------------------
"""Performs repository-specific activation activities."""

import os
import sys

sys.path.insert(0, os.getenv("DEVELOPMENT_ENVIRONMENT_FUNDAMENTAL"))
from RepositoryBootstrap.SetupAndActivate import CommonEnvironment, CurrentShell
from RepositoryBootstrap.Impl.ActivationActivity import ActivationActivity

del sys.path[0]

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

# Ensure that we are loading custom data from this dir and not some other repository.
sys.modules.pop("_custom_data", None)

from _custom_data import _CUSTOM_DATA

# <Class '<name>' has no '<attr>' member> pylint: disable = E1101
# <Unrearchable code> pylint: disable = W0101
# <Unused argument> pylint: disable = W0613

# ----------------------------------------------------------------------
def GetCustomActions(
    output_stream,
    configuration,
    version_specs,
    generated_dir,
    debug,
    verbose,
    fast,
    repositories,
    is_mixin_repo,
):
    """
    Returns an action or list of actions that should be invoked as part of the activation process.

    Actions are generic command line statements defined in
    <Common_Environment>/Libraries/Python/CommonEnvironment/v1.0/CommonEnvironment/Shell/Commands/__init__.py
    that are converted into statements appropriate for the current scripting language (in most
    cases, this is Bash on Linux systems and Batch or PowerShell on Windows systems.
    """

    actions = []

    if fast:
        actions.append(
            CurrentShell.Commands.Message(
                "** FAST: Activating without verifying content. ({})".format(_script_fullpath),
            ),
        )
    else:
        for name, version, path_parts in _CUSTOM_DATA:
            this_dir = os.path.join(*([_script_dir] + path_parts))
            assert os.path.isdir(this_dir), this_dir

            actions += [
                CurrentShell.Commands.Execute(
                    'python "{script}" Verify "{name}" "{dir}" "{version}"'.format(
                        script=os.path.join(
                            os.getenv("DEVELOPMENT_ENVIRONMENT_FUNDAMENTAL"),
                            "RepositoryBootstrap",
                            "SetupAndActivate",
                            "AcquireBinaries.py",
                        ),
                        name=name,
                        dir=this_dir,
                        version=version,
                    ),
                ),
            ]

        # Initialize the environment
        boost_dir = ActivationActivity.GetVersionedDirectory(
            version_specs.Libraries.get("C++", {}),
            _script_dir,
            "Libraries",
            "C++",
            "boost",
        )
        assert os.path.isdir(boost_dir), boost_dir

        boost_version = os.path.basename(boost_dir)
        if boost_version.startswith("v"):
            boost_version = boost_version[1:]

        actions += [
            CurrentShell.Commands.Set("DEVELOPMENT_ENVIRONMENT_BOOST_VERSION", boost_version),
            CurrentShell.Commands.Set(
                "DEVELOPMENT_ENVIRONMENT_BOOST_VERSION_SHORT",
                ".".join(boost_version.split(".")[:-1]),
            ),
            CurrentShell.Commands.Set("DEVELOPMENT_ENVIRONMENT_BOOST_ROOT", boost_dir),
            CurrentShell.Commands.Set(
                "DEVELOPMENT_ENVIRONMENT_BOOST_IS_STANDARD_CONFIGURATION",
                "1" if configuration == "standard" else "0",
            ),
        ]

    return actions


# ----------------------------------------------------------------------
def GetCustomScriptExtractors():
    """
    Returns information that can be used to enumerate, extract, and generate documentation
    for scripts stored in the Scripts directory in this repository and all repositories
    that depend upon it.

    ****************************************************
    Note that it is very rare to have the need to implement
    this method. In most cases, it is safe to delete it.
    ****************************************************

    There concepts are used with custom script extractors:

        - DirGenerator:             Method to enumerate sub-directories when searching for scripts in a
                                    repository's Scripts directory.

                                        def Func(directory, version_sepcs) -> [ (subdir, should_recurse), ... ]
                                                                              [ subdir, ... ]
                                                                              (subdir, should_recurse)
                                                                              subdir

        - CreateCommands:           Method that creates the shell commands to invoke a script.

                                        def Func(script_filename) -> [ command, ...]
                                                                     command
                                                                     None           # Indicates not supported

        - CreateDocumentation:      Method that extracts documentation from a script.

                                        def Func(script_filename) -> documentation string

        - ScriptNameDecorator:      Returns a new name for the script.

                                        def Func(script_filename) -> name string

    See <Common_Environment>/Activate_custom.py for an example of how script extractors
    are used to process Python and PowerShell scripts.
    """

    return
