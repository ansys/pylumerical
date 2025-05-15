"""
lumerical.

Core
"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

import ansys.api.lumerical

# Make common names from lumapi available in the top-level namespace
from ansys.api.lumerical.lumapi import (FDTD, MODE, DEVICE, INTERCONNECT, SimObject, SimObjectResults, SimObjectId)
from . import autodiscovery

if len(ansys.api.lumerical.lumapi.InteropPaths.LUMERICALINSTALLDIR) == 0:
    install_dir = autodiscovery.locate_lumerical_install()
    if install_dir is not None:
        ansys.api.lumerical.lumapi.InteropPaths.setLumericalInstallPath(install_dir)
    else:
        # TODO: how to handle this warning?
        print(
            "Warning: Lumerical installation not found. Please use InteropPaths.setLumericalInstallPath "
            "to set the interop library location.")
    del install_dir  # remove the local variable to exclude from the namespace

__version__ = importlib_metadata.version(__name__.replace(".", "-"))
