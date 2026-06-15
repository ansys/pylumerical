# Copyright (C) 2025 - 2026 ANSYS, Inc. and/or its affiliates.
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

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestLumericalEval:
    """Test the lumapi 'Lumerical' object 'eval' and user functions."""

    def test_no_user_functions(self, setup_fdtd):
        """Test 01: Test 'Lumerical' object has no user functions by default."""
        assert setup_fdtd.userFunctions == set()

    def test_eval_user_function(self, setup_fdtd):
        """Test 02: Test 'Lumerical' object 'eval' method with a user function."""
        setup_fdtd.eval("function add_function(a, b){ return a + b; }")
        setup_fdtd.eval("res = add_function(1, 2);")

        assert setup_fdtd.userFunctions == set()

    def test_add_user_functions(self, setup_fdtd):
        """Test 03: Test 'Lumerical' object '_addUserFunctions' method."""
        setup_fdtd._addUserFunctions()

        userfunction_list = list(setup_fdtd.userFunctions)

        assert userfunction_list[0] == "add_function"

        res = setup_fdtd.getv("res")

        assert res == 3

    def test_sync_user_functions(self, setup_fdtd):
        """Test 04: Test 'Lumerical' object '_syncUserFunctions' method."""
        setup_fdtd.eval("function multiply_function(a, b){ return a * b; }")

        setup_fdtd._syncUserFunctions()

        assert setup_fdtd.userFunctions == {"add_function", "multiply_function"}

    def test_delete_user_functions(self, setup_fdtd):
        """Test 05: Test 'Lumerical' object '_deleteUserFunctions' method."""
        setup_fdtd._deleteUserFunctions()

        assert setup_fdtd.userFunctions == set()
