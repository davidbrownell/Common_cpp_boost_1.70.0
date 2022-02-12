# ----------------------------------------------------------------------
# |
# |  Setup_custom.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2018-05-03 22:12:13
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2018-22.
# |  Distributed under the Boost Software License, Version 1.0.
# |  (See accompanying file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# |
# ----------------------------------------------------------------------
"""Performs repository-specific setup activities."""

# ----------------------------------------------------------------------
# |
# |  To setup an environment, run:
# |
# |     Setup(.cmd|.ps1|.sh) [/debug] [/verbose] [/configuration=<config_name>]*
# |
# ----------------------------------------------------------------------

import os
import sys

from collections import OrderedDict

import CommonEnvironment

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

# <Missing function docstring> pylint: disable = C0111
# <Line too long> pylint: disable = C0301
# <Wrong hanging indentation> pylint: disable = C0330
# <Class '<name>' has no '<attr>' member> pylint: disable = E1103
# <Unreachable code> pylint: disable = W0101
# <Wildcard import> pylint: disable = W0401
# <Unused argument> pylint: disable = W0613

fundamental_repo                            = os.getenv("DEVELOPMENT_ENVIRONMENT_FUNDAMENTAL")
assert os.path.isdir(fundamental_repo), fundamental_repo

sys.path.insert(0, fundamental_repo)
from RepositoryBootstrap import *                                           # <Unused import> pylint: disable = W0614
from RepositoryBootstrap.SetupAndActivate import CurrentShell               # <Unused import> pylint: disable = W0614
from RepositoryBootstrap.SetupAndActivate.Configuration import *            # <Unused import> pylint: disable = W0614

del sys.path[0]

from _custom_data import _CUSTOM_DATA

# ----------------------------------------------------------------------
# There are two types of repositories: Standard and Mixin. Only one standard
# repository may be activated within an environment at a time while any number
# of mixin repositories can be activated within a standard repository environment.
# Standard repositories may be dependent on other repositories (thereby inheriting
# their functionality), support multiple configurations, and specify version
# information for tools and libraries in themselves or its dependencies.
#
# Mixin repositories are designed to augment other repositories. They cannot
# have configurations or dependencies and may not be activated on their own.
#
# These difference are summarized in this table:
#
#                                                       Standard  Mixin
#                                                       --------  -----
#      Can be activated in isolation                       X
#      Supports configurations                             X
#      Supports VersionSpecs                               X
#      Can be dependent upon other repositories            X
#      Can be activated within any other Standard                  X
#        repository
#
# Consider a script that wraps common Git commands. This functionality is useful
# across a number of different repositories, yet doesn't have functionality that
# is useful on its own; it provides functionality that augments other repositories.
# This functionality should be included within a repository that is classified
# as a mixin repository.
#
# To classify a repository as a Mixin repository, decorate the GetDependencies method
# with the MixinRepository decorator.
#


# @MixinRepository # <-- Uncomment this line to classify this repository as a mixin repository
def GetDependencies():
    """
    Returns information about the dependencies required by this repository.

    The return value should be an OrderedDict if the repository supports multiple configurations
    (aka is configurable) or a single Configuration if not.
    """

    d = OrderedDict()

    d["standard"] = Configuration(
        "boost v1.70.0 - standard (No compiler dependencies)",
        [
            Dependency(
                "28F6B685610244468CBA2A80E84E021F",
                "Common_cpp_boost_Common",
                None,
                "https://github.com/davidbrownell/Common_cpp_boost_Common.git",
            ),
        ],
    )

    if CurrentShell.CategoryName == "Windows":
        architectures = ["x64", "x86"]

        compiler_factories = [
            lambda: (
                "MSVC_2019",
                "Common_cpp_MSVC_2019",
                "AB7D87C49C2449F79D9F42E5195030FD",
                "MSVC 2019",
                None,
            ),
            lambda: (
                "MSVC_2017",
                "Common_cpp_MSVC_2017",
                "8FC8ACE80A594D2EA996CAC5DBFFEBBC",
                "MSVC 2017",
                None,
            ),
            # lambda: (
            #     "Clang_10",
            #     "Common_cpp_Clang_10",
            #     "42DE100A1DAE4FFC9697F75566C63DEB",
            #     "Clang 10",
            #     None,
            # ),
            lambda: (
                "Clang_10",
                "Common_cpp_Clang_10",
                "42DE100A1DAE4FFC9697F75566C63DEB",
                "Clang 10 (ex)",
                "_ex",
            ),
            # lambda: (
            #     "Clang_8",
            #     "Common_cpp_Clang_8",
            #     "3DE9F3430E494A6C8429B26A1503C895",
            #     "Clang 8",
            #     None,
            # ),
            lambda: (
                "Clang_8",
                "Common_cpp_Clang_8",
                "3DE9F3430E494A6C8429B26A1503C895",
                "Clang 8 (ex)",
                "_ex",
            ),
        ]
    else:
        # Cross compiling on Linux is much more difficult on Linux than it is on
        # Windows. Only support the current architecture.
        architectures = [CurrentShell.Architecture]

        compiler_factories = [
            # lambda: (
            #     "Clang_10",
            #     "Common_cpp_Clang_10",
            #     "42DE100A1DAE4FFC9697F75566C63DEB",
            #     "Clang 10",
            #     None,
            # ),
            lambda: (
                "Clang_10",
                "Common_cpp_Clang_10",
                "42DE100A1DAE4FFC9697F75566C63DEB",
                "Clang 10 (ex)",
                "_ex",
            ),
            # lambda: (
            #     "Clang_8",
            #     "Common_cpp_Clang_8",
            #     "3DE9F3430E494A6C8429B26A1503C895",
            #     "Clang 8",
            #     None,
            # ),
            lambda: (
                "Clang_8",
                "Common_cpp_Clang_8",
                "3DE9F3430E494A6C8429B26A1503C895",
                "Clang 8 (ex)",
                "_ex",
            ),
        ]

    for compiler_factory in compiler_factories:
        (
            config_name,
            repo_name,
            repo_id,
            config_desc,
            architecture_configuration_suffix,
         ) = compiler_factory()

        architecture_configuration_suffix = architecture_configuration_suffix or ""

        for architecture in architectures:
            this_config_name = "{}_{}{}".format(config_name, architecture, architecture_configuration_suffix)
            this_config_desc = "boost 1.70.0 - {} ({})".format(config_desc, architecture)

            d[this_config_name] = Configuration(
                this_config_desc,
                [
                    Dependency(
                        "28F6B685610244468CBA2A80E84E021F",
                        "Common_cpp_boost_Common",
                        None,
                        "https://github.com/davidbrownell/Common_cpp_boost_Common.git",
                    ),
                    Dependency(
                        repo_id,
                        repo_name,
                        "{}{}".format(architecture, architecture_configuration_suffix),
                        "https://github.com/davidbrownell/{}.git".format(repo_name),
                    ),
                ],
            )

    return d


# ----------------------------------------------------------------------
def GetCustomActions(debug, verbose, explicit_configurations):
    """
    Returns an action or list of actions that should be invoked as part of the setup process.

    Actions are generic command line statements defined in
    <Common_Environment>/Libraries/Python/CommonEnvironment/v1.0/CommonEnvironment/Shell/Commands/__init__.py
    that are converted into statements appropriate for the current scripting language (in most
    cases, this is Bash on Linux systems and Batch or PowerShell on Windows systems.
    """

    actions = []

    if CurrentShell.CategoryName == "Windows":
        # ----------------------------------------------------------------------
        def FilenameToUri(filename):
            return CommonEnvironmentImports.FileSystem.FilenameToUri(filename).replace("%", "%%")

        # ----------------------------------------------------------------------
    else:
        FilenameToUri = CommonEnvironmentImports.FileSystem.FilenameToUri

    for name, version, path_parts in _CUSTOM_DATA:
        this_dir = os.path.join(*([_script_dir] + path_parts))
        assert os.path.isdir(this_dir), this_dir

        install_filename = os.path.join(this_dir, "Install.7z")

        actions += [
            CurrentShell.Commands.Execute(
                'python "{script}" Install "{name}" "{uri}" "{dir}" "/unique_id={version}" /unique_id_is_hash'.format(
                    script=os.path.join(
                        os.getenv("DEVELOPMENT_ENVIRONMENT_FUNDAMENTAL"),
                        "RepositoryBootstrap",
                        "SetupAndActivate",
                        "AcquireBinaries.py",
                    ),
                    name=name,
                    uri=FilenameToUri(install_filename),
                    dir=this_dir,
                    version=version,
                ),
            )
        ]

    return actions
