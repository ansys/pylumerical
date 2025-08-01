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

"""Test lumapi 'Lumerical' object raises different 'LumApiError'.

- test 01: Test 'Lumerical' object 'eval' method raises 'Failed to evaluate code' LumApiError
- test 02: Test 'Lumerical' object 'getv' method raises 'Failed to get variable' LumApiError
- test 03: Test 'Lumerical' object 'putv' method raises "'SimObject' object has no attribute" LumApiError
- test 04: Test 'Lumerical' object 'getObjectById' method raises 'Object ... not found' LumApiError
- test 05: Test 'Lumerical' object 'getObjectBySelection' method raises 'in getid, no items are currently selected' LumApiError
"""

import pytest

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestLumApiError:
    """Test the lumapi 'Lumerical' object raises different 'LumApiError'."""

    def test_eval_fails(self, setup_fdtd):
        """Test 01: Test 'Lumerical' object 'eval' method raises 'Failed to evaluate code' LumApiError."""
        with pytest.raises(lumapi.LumApiError) as ex_info:
            setup_fdtd.eval("qwerty")

        assert "Failed to evaluate code" in str(ex_info.value)

    def test_getv_fails(self, setup_fdtd):
        """Test 02: Test 'Lumerical' object 'getv' method raises 'Failed to get variable' LumApiError."""
        with pytest.raises(lumapi.LumApiError) as ex_info:
            _ = setup_fdtd.getv("qwerty")

        assert "Failed to get variable" in str(ex_info.value)

    def test_putv_attr_error(self, setup_fdtd):
        """Test 03: Test 'Lumerical' object 'putv' method raises "'SimObject' object has no attribute" LumApiError."""
        setup_fdtd.addfdtd()

        obj = setup_fdtd.getObjectById("::model::FDTD")

        with pytest.raises(AttributeError) as ex_info:
            setup_fdtd.putv("obj", obj)

        assert "'SimObject' object has no attribute" in str(ex_info.value)

    def test_obj_not_found_error(self, setup_fdtd):
        """Test 04: Test 'Lumerical' object 'getObjectById' method raises 'Object ... not found' LumApiError."""
        setup_fdtd.addrect({"name": "rect1"})

        with pytest.raises(lumapi.LumApiError) as ex_info:
            _ = setup_fdtd.getObjectById("::model::rect_2")

        assert "Object ::model::rect_2 not found" in str(ex_info.value)

    def test_no_items_selected_error(self, setup_fdtd):
        """Test 05: Test 'Lumerical' object 'getObjectBySelection' method raises 'in getid, no items are currently selected' LumApiError."""
        setup_fdtd.unselectall()

        with pytest.raises(lumapi.LumApiError) as ex_info:
            _ = setup_fdtd.getObjectBySelection()

        assert "in getid, no items are currently selected" in str(ex_info.value)
