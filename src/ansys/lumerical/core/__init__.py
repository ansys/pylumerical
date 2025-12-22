# Copyright (C) 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Set up the imports for PyLumerical."""

import ansys.api.lumerical

# Make common names from lumapi available in the top-level namespace
from ansys.api.lumerical.lumapi import DEVICE, FDTD, INTERCONNECT, MODE, InteropPaths, SimObject, SimObjectId, SimObjectResults

from . import autodiscovery

__version__ = "0.2.0"
"""Lumerical API version."""

if len(ansys.api.lumerical.lumapi.InteropPaths.LUMERICALINSTALLDIR) == 0:
    install_dir = autodiscovery.locate_lumerical_install()
    if install_dir is not None:
        ansys.api.lumerical.lumapi.InteropPaths.setLumericalInstallPath(install_dir)
    else:
        print("Lumerical installation not found. Please use InteropPaths.setLumericalInstallPath to set the interop library location.")
    del install_dir  # remove the local variable to exclude from the namespace
