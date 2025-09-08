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

"""Test INTERCONNECT Automatic Reload CML.
- Test 01: test automatic reload CML
"""

import pytest
import os
import shutil
import time
from set_resources import SetResources

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestAutomaticReloadCML():
    """Test Automatic Reload CML."""

    def _run_simulation(self):
        """_run_simulation."""
        
        self.intc.run()
        self.intc.eval('gd = getresult("ONA_1", "input 1/mode 1/peak/group delay");')
        self.intc.eval('gd = gd.getattribute("TE group delay (s)");')
        
        return self.intc.getv("gd")

    def test_automatic_reload_cml(self):
        """Test 01: test automatic reload CML."""
        self.resources = SetResources()
        resources = self.resources.setup("INTERCONNECT")    
        self.project_temp_file = resources[0] 
        self.file_name = resources[1]
        self.resource_path = resources[2]

        self.intc = lumapi.INTERCONNECT(project=self.project_temp_file, hide=True)
        self.intc.installdesignkit("N_eff_1/lib_test.cml", ".")
        self.intc.addelement("COMPOUND_1")
        self.intc.connect("COMPOUND_1", "port 1", "ONA_1", "output")
        self.intc.connect("COMPOUND_1", "port 2", "ONA_1", "input 1")
        gd_short = self._run_simulation() * 10**15
        print ("N = 1, group delay is: " + str(gd_short)) 
        
        self.intc.switchtodesign()
        compound_path = os.path.join(self.resource_path, 'N_eff_3', 'COMPOUND_1.ice')
        temp_path = os.path.join(self.resource_path, 'New folder')
        
        if not os.path.isdir(temp_path):
            os.mkdir(temp_path)
           
        shutil.copy(compound_path, temp_path)
        time.sleep(0.5)
        gd_long = self._run_simulation() * 10**15
        print("N = 3, group delay is: " + str(gd_long)) 
        
        assert gd_short * 3 == pytest.approx(gd_long, abs = 1e-4)

        shutil.rmtree(temp_path)

        self.intc.close()

        ich_file = "%s_temp.ich" % self.file_name
        self.resources.teardown(delete_file=ich_file)
