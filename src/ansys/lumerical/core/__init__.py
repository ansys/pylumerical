"""
lumerical.

Core
"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

from ansys.api.lumerical.lumapi import InteropPaths, FDTD, MODE, DEVICE, INTERCONNECT
from .autodiscovery import locate_lumerical_install

if len(InteropPaths.LUMERICALINSTALLDIR) == 0:
    install_dir = locate_lumerical_install()
    if install_dir is not None:
        InteropPaths.setLumericalInstallPath(install_dir)
    else:
        print("Warning: Lumerical installation not found. Please use InteropPaths.setLumericalInstallPath to set the interop library location.")

__version__ = importlib_metadata.version(__name__.replace(".", "-"))
