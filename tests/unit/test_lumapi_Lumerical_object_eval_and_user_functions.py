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

"""Test lumapi 'Lumerical' object 'eval' and user functions.

- test 01: Test 'Lumerical' object has no user functions by default
- test 02: Test 'Lumerical' object 'eval' method with a user function
- test 03: Test 'Lumerical' object '_addUserFunctions' method
- test 04: Test 'Lumerical' object '_syncUserFunctions' method
- test 05: Test 'Lumerical' object '_deleteUserFunctions' method
"""

import pytest

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


@pytest.fixture(scope="module")
def module_setup():
    """PyTest module setup / tearadown."""
    print("\n--> Setup")

    global fdtd

    fdtd = lumapi.FDTD(hide=True)

    yield

    print("\n--> Teardown")

    fdtd.close()


class TestLumericalEval:

    def test_lumerical_object_has_no_user_functions(self, module_setup):
        """Test 01: Test 'Lumerical' object has no user functions by default."""
        global fdtd

        assert fdtd.userFunctions == set()


    def test_lumerical_object_eval_user_function(self, module_setup):
        """Test 02: Test 'Lumerical' object 'eval' method with a user function."""
        global fdtd

        fdtd.eval("function add_function(a, b){ return a + b; }")
        fdtd.eval("res = add_function(1, 2);")

        assert fdtd.userFunctions == set()


    def test_lumerical_object_add_user_functions(self, module_setup):
        """Test 03: Test 'Lumerical' object '_addUserFunctions' method."""
        global fdtd

        fdtd._addUserFunctions()

        userfunction_list = list(fdtd.userFunctions)

        assert userfunction_list[0] == "add_function"

        res = fdtd.getv("res")

        assert res == 3


    def test_lumerical_object_sync_user_functions(self, module_setup):
        """Test 04: Test 'Lumerical' object '_syncUserFunctions' method."""
        global fdtd

        fdtd.eval("function multiply_function(a, b){ return a * b; }")

        fdtd._syncUserFunctions()

        assert fdtd.userFunctions == {"add_function", "multiply_function"}


    def test_lumerical_object_delete_user_functions(self, module_setup):
        """Test 05: Test 'Lumerical' object '_deleteUserFunctions' method."""
        global fdtd

        fdtd._deleteUserFunctions()

        assert fdtd.userFunctions == set()
