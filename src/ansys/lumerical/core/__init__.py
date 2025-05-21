"""Set up the imports for PyLumerical."""
import ansys.api.lumerical

# Make common names from lumapi available in the top-level namespace
from ansys.api.lumerical.lumapi import DEVICE, FDTD, INTERCONNECT, MODE, SimObject, SimObjectId, SimObjectResults

from . import autodiscovery

__version__ = "0.1.dev0"
"""Lumerical API version."""

if len(ansys.api.lumerical.lumapi.InteropPaths.LUMERICALINSTALLDIR) == 0:
    install_dir = autodiscovery.locate_lumerical_install()
    if install_dir is not None:
        ansys.api.lumerical.lumapi.InteropPaths.setLumericalInstallPath(install_dir)
    else:
        # TODO(dylanm-ansys): how to handle this warning?
        print(
            "Warning: Lumerical installation not found. Please use InteropPaths.setLumericalInstallPath "
            "to set the interop library location.")
    del install_dir  # remove the local variable to exclude from the namespace
