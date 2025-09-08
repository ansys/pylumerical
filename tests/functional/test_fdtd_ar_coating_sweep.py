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

"""Test FDTD AR Coating Sweep Example.
- Test 01: test AR coating sweep example
"""

import pytest
import os
from set_resources import SetResources

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestFdtdArCoatingSweepExample():
    """Test FDTD AR Coating Sweep Example."""

    def test_ar_coating_sweep_example(self):
        """Test 01: test AR coating sweep example."""
        self.resources = SetResources()
        resources = self.resources.setup("FDTD")
        self.project_temp_file = resources[0]

        fdtd = lumapi.FDTD(project = self.project_temp_file, hide = True)
        n_sweep_points = 5
        thickness = [x*0.15e-6 / (n_sweep_points - 1) for x in range(n_sweep_points)]
        r_list = list()

        for t in thickness:
            fdtd.switchtolayout()
            fdtd.setnamed("AR structure", "thickness", t)
            fdtd.run()
            r_list.append(fdtd.transmission("R"))

        assert all(r > 0.0 for r in r_list )
        
        fdtd.close()

        self.resources.teardown()
