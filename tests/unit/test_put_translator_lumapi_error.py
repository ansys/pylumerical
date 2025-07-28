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

"""Test lumapi 'PutTranslator' object raises LumApiError.

- test 01: Test 'PutTranslator' object raises 'Unsupported data type' LumApiError
- test 02: Test 'PutTranslator' object raises 'wrong type for the property' LumApiError
"""

import pytest

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestPutTranslatorLumApiError:
    """Test the lumapi 'PutTranslator' object raises LumApiError."""

    def test_unsupported_datatype_error(self, setup_fdtd_extras):
        """Test 01: Test 'PutTranslator' object raises 'Unsupported data type' LumApiError."""
        with pytest.raises(lumapi.LumApiError) as excinfo:
            setup_fdtd_extras.setnamed("assembly_grp", "parameters", {"x", "y", "radius"})

        assert "Unsupported data type" in str(excinfo.value)

    def test_wrong_property_type_error(self, setup_fdtd_extras):
        """Test 02: Test 'PutTranslator' object raises 'wrong type for the property' LumApiError."""
        mapping = [[0, 2, 0, 1], [0, 0, 2, 1], [1, 0.5, 0.5, 1]]

        with pytest.raises(lumapi.LumApiError) as excinfo:
            setup_fdtd_extras.setnamed("assembly_grp", "mapping", mapping)

        assert ("in setnamed, the value supplied is the wrong type " + "for the property 'mapping'") in str(excinfo.value)
