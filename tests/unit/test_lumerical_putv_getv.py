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

"""Test lumapi Lumerical object 'putv' and 'getv' functions.

- test 01: Test 'Lumerical' object 'putv' and 'getv' an int
- test 02: Test 'Lumerical' object 'putv' and 'getv' a float
- test 03: Test 'Lumerical' object 'putv' and 'getv' a string
- test 04: Test 'Lumerical' object 'putv' and 'getv' a matrix
- test 05: Test 'Lumerical' object 'putv' and 'getv' a numpy array
- test 06: Test 'Lumerical' object 'putv' and 'getv' a numpy 2D array
- test 07: Test 'Lumerical' object 'putv' and 'getv' a numpy complex array
- test 08: Test 'Lumerical' object 'putv' and 'getv' a numpy int
- test 09: Test 'Lumerical' object 'putv' and 'getv' a numpy float
- test 10: Test 'Lumerical' object 'putv' and 'getv' a list
- test 11: Test 'Lumerical' object 'putv' and 'getv' a dict
- test 12: Test 'Lumerical' object 'putv' and 'getv' a set
- test 13: Test 'Lumerical' object 'putv' and 'getv' a tuple
- test 14: Test 'Lumerical' object 'putv' and 'getv' None
- test 15: Test 'Lumerical' object 'putv' and 'getv' numpy nan
"""

import numpy as np
import pytest

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestLumericalPutvGetv:
    """Test the lumapi 'Lumerical' object 'putv' and 'getv' functions."""

    @pytest.fixture
    def test_int(self, setup_fdtd):
        """Test 01: Test 'Lumerical' object 'putv' and 'getv' an int."""
        int_name = "I"
        int_value = 3.141592653589

        setup_fdtd.putv(int_name, int_value)

        get_int_value = setup_fdtd.getv(int_name)

        assert get_int_value == int_value

    def test_float(self, setup_fdtd):
        """Test 02: Test 'Lumerical' object 'putv' and 'getv' a float."""
        float_name = "A"
        float_value = 3.141592653589

        setup_fdtd.putv(float_name, float_value)

        get_float_value = setup_fdtd.getv(float_name)

        assert get_float_value == float_value

    def test_string(self, setup_fdtd):
        """Test 03: Test 'Lumerical' object 'putv' and 'getv' a string."""
        string_name = "B"
        string_value = "lumerical string variable"

        setup_fdtd.putv(string_name, string_value)

        get_string_value = setup_fdtd.getv(string_name)

        assert get_string_value == string_value

    def test_matrix(self, setup_fdtd):
        """Test 04: Test 'Lumerical' object 'putv' and 'getv' a matrix."""
        matrix_name = "C"
        matrix_value = [[1, 3, 4], [2, 5, 6], [3, 1, 1]]

        setup_fdtd.putv(matrix_name, matrix_value)

        get_matrix_value = setup_fdtd.getv(matrix_name)

        assert get_matrix_value == matrix_value

    def test_numpy_array(self, setup_fdtd):
        """Test 05: Test 'Lumerical' object 'putv' and 'getv' a numpy array."""
        array_name = "D"
        array_value = np.array([1, 2, 3, 4, 5])

        setup_fdtd.putv(array_name, array_value)

        get_array_value = setup_fdtd.getv(array_name)

        assert get_array_value[0] == array_value[0]

    def test_numpy_2d_array(self, setup_fdtd):
        """Test 06: Test 'Lumerical' object 'putv' and 'getv' a numpy 2D array."""
        array_name = "D2"
        array_value = np.array([[0, 1, 2], [3, 4, 5]])

        setup_fdtd.putv(array_name, array_value)

        get_array_value = setup_fdtd.getv(array_name)

        assert get_array_value[1, 1] == array_value[1, 1]

    def test_numpy_complex_array(self, setup_fdtd):
        """Test 07: Test 'Lumerical' object 'putv' and 'getv' a numpy complex array."""
        array_name = "D3"
        array_value = np.array([[1 + 2j, 3 - 4j], [5j, 6 + 7j]])

        setup_fdtd.putv(array_name, array_value)

        get_array_value = setup_fdtd.getv(array_name)

        assert get_array_value[1, 1] == array_value[1, 1]

    def test_numpy_int(self, setup_fdtd):
        """Test 08: Test 'Lumerical' object 'putv' and 'getv' a numpy int."""
        int_name = "numpy_int"
        int_value = np.int64(10)

        setup_fdtd.putv(int_name, int_value)

        get_int_value = setup_fdtd.getv(int_name)

        assert get_int_value == int_value

    def test_numpy_float(self, setup_fdtd):
        """Test 09: Test 'Lumerical' object 'putv' and 'getv' a numpy float."""
        float_name = "numpy_float"
        float_value = np.float32(1.2)

        setup_fdtd.putv(float_name, float_value)

        get_float_value = setup_fdtd.getv(float_name)

        assert get_float_value == float_value

    def test_list(self, setup_fdtd):
        """Test 10: Test 'Lumerical' object 'putv' and 'getv' a list."""
        list_name = "E"
        list_value = [1, 2, 3, 4, 5]

        setup_fdtd.putv(list_name, list_value)

        get_list_value = setup_fdtd.getv(list_name)

        assert get_list_value == list_value

    def test_dict(self, setup_fdtd):
        """Test 11: Test 'Lumerical' object 'putv' and 'getv' a dict."""
        dict_name = "F"
        dict_value = {"a": 1, "b": 2, "c": 3}

        setup_fdtd.putv(dict_name, dict_value)

        get_dict_value = setup_fdtd.getv(dict_name)

        assert get_dict_value == dict_value

    def test_set(self, setup_fdtd):
        """Test 12: Test 'Lumerical' object 'putv' and 'getv' a set."""
        set_name = "S"
        set_value = {"a", "b", "c"}

        setup_fdtd.putv(set_name, set_value)

        get_set_value = setup_fdtd.getv(set_name)

        assert list(get_set_value) == list(set_value)

    def test_tuple(self, setup_fdtd):
        """Test 13: Test 'Lumerical' object 'putv' and 'getv' a tuple."""
        tuple_name = "T"
        tuple_value = ("a", "b", "c")

        setup_fdtd.putv(tuple_name, tuple_value)

        get_tuple_value = setup_fdtd.getv(tuple_name)

        assert list(get_tuple_value) == list(tuple_value)

    def test_none(self, setup_fdtd):
        """Test 14: Test 'Lumerical' object 'putv' and 'getv' None."""
        none_name = "none"
        none_value = None

        setup_fdtd.putv(none_name, none_value)

        get_none_value = setup_fdtd.getv(none_name)

        assert get_none_value == "None"

    def test_numpy_nan(self, setup_fdtd):
        """Test 15: Test 'Lumerical' object 'putv' and 'getv' numpy nan."""
        nan_name = "numpy_nan"
        nan_value = np.nan

        setup_fdtd.putv(nan_name, nan_value)

        get_nan_value = setup_fdtd.getv(nan_name)

        assert np.isnan(get_nan_value)
