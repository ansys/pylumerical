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

"""Test lumapi 'lumTypes' function.

- test 01: Test lumapi 'lumTypes' function with a list argument
- test 02: Test lumapi 'lumTypes' function with a non-list argument
"""

import numpy as np

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestLumTypes:
    """Test the lumapi 'lumTypes' function."""

    def test_lumapi_lumtypes_function_with_list_argument(self):
        """Test 01: Test lumapi 'lumTypes' function with a list argument."""
        mapping = [[0, 2, 0, 1], [0, 0, 2, 1], [1, 0.5, 0.5, 1]]

        np_mapping = np.array(mapping)

        converted = lumapi.lumTypes([mapping, np_mapping])

        assert converted == ["cell array", "matrix"]

    def test_lumapi_lumtypes_function_with_non_list_argument(self):
        """Test 02: Test lumapi 'lumTypes' function with a non-list argument."""
        dct = {"a": 1, "b": 2, "c": 3}

        converted = lumapi.lumTypes(dct)

        assert converted is None
