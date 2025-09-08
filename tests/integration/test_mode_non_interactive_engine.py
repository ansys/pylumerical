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

"""Test MODE CAD with Engine Licenses.
- Test 01: test 'use-solve' EME
- Test 02: test 'use-solve' varFDTD
- Test 03: test 'use-solve' FDE
- Test 04: test 'use-solve' with disabled command
"""

import pytest
import os
from set_resources import SetResources

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestModeCadWithEngineLicenses():

    def _set_and_run_solver_test(self, cml_options):
        """set and run solver test."""
        self.resources = SetResources()
        resources = self.resources.setup("MODE")
        self.project_temp_file = resources[0]
        self.file_name = resources[1]

        self.mode = lumapi.MODE(project=self.project_temp_file, hide=True, serverArgs=cml_options)
        self.mode.switchtolayout()
        self.mode.setactivesolver(self.solver_name)
        self.mode.eval("temp = 1;")
        
        if self.solver_name == "FDE":
            self.mode.findmodes()
            
        assert str(self.mode.getv("temp")) == "1.0"
        
        if self.run:
            run_failed = False
            try:
                self.mode.run()
            except:
                run_failed = True
            finally:
                assert run_failed
                
        self.mode.close()

        self.resources.teardown()
    
    def test_use_solve_eme(self):
        """Test 01: test 'use-solve' EME."""
        print("\nTesting EME use-solve")
        
        self.solver_name = "EME"
        self.run = False
        self._set_and_run_solver_test({"use-solve" : True, "logall" : True})
        self._set_and_run_solver_test({"use-solve" : "eme", "logall" : True})
        self._set_and_run_solver_test({"use-solve" : "eme", "threads" : 10, "logall" : True})
        self._set_and_run_solver_test({"use-solve" : "varfdtd", "threads" : 10, "logall" : True})
        self._set_and_run_solver_test({"use-solve" : "fde", "logall" : True})
    
    def test_use_solve_var_fdtd(self):
        """Test 02: test 'use-solve' varFDTD."""
        print("\nTesting varFDTD use-solve")
        
        self.solver_name = "varFDTD"
        self.run = False
        self._set_and_run_solver_test({"use-solve" : True, "logall" : True})
        self._set_and_run_solver_test({"use-solve" : "varfdtd", "logall" : True})
        self._set_and_run_solver_test({"use-solve" : "varfdtd", "threads" : 33, "logall" : True})
        self._set_and_run_solver_test({"use-solve" : "eme", "logall" : True})
        self._set_and_run_solver_test({"use-solve" : "fde", "threads" : 4, "logall" : True})
    
    def test_use_solve_fde(self):
        """Test 03: test 'use-solve' FDE."""
        print("\nTesting FDE use-solve")
        
        self.solver_name = "FDE"
        self.run = False
        self._set_and_run_solver_test({"use-solve" : True, "logall" : True})
        self._set_and_run_solver_test({"use-solve" : "fde", "logall" : True})
        self._set_and_run_solver_test({"use-solve" : "fde", "threads" : 4, "logall" : True})
        self._set_and_run_solver_test({"use-solve" : "varfdtd", "logall" : True})
        self._set_and_run_solver_test({"use-solve" : "eme", "threads" : 5, "logall" : True})
    
    def test_use_solve_with_disabled_command(self):
        """Test 04: test 'use-solve' with disabled command."""
        print("\nTesting run command under use-solve")
        
        self.solver_name = "EME"
        self.run = True
        self._set_and_run_solver_test({"use-solve" : True, "logall" : True})
