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

'''Test FDTD CAD with Engine Licenses.
- Test 01: test python api use solve only
- Test 02: test python api use solve and threads
'''

import pytest
import os
from set_resources import SetResources

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestFdtdCadWithEngineLicenses():
    '''Test FDTD CAD with Engine Licenses.'''

    def test_use_solve_only(self):
        """Test 01: test python api use solve only."""
        self.resources = SetResources()
        resources = self.resources.setup("FDTD")
        self.file_name = resources[1]
        self.script_file = resources[3]

        fdtd = lumapi.FDTD(script=self.script_file, serverArgs={"use-solve" : True, "logall" : True})
        
        assert str(fdtd.getv("temp")) == "1.0"
        assert str(fdtd.getv("ErrMsg")) != ""
        
        fdtd.close()

        self.resources.teardown()

    def test_use_solve_and_threads(self):
        """Test 02: test python api use solve and threads."""
        self.resources = SetResources()
        resources = self.resources.setup("FDTD")
        self.file_name = resources[1]
        self.script_file = resources[3]
        
        fdtd = lumapi.FDTD(script=self.script_file, serverArgs={"use-solve" : True, "threads" : 4, "logall" : True})
        
        assert str(fdtd.getv("temp")) == "1.0"
        assert str(fdtd.getv("ErrMsg")) != ""
        
        fdtd.close()

        self.resources.teardown()
