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

"""Test the lumapi 'appCall' and 'appCallWithConstructor' objects.

- test 01: Test 'appCall' object with ordered dict properties
- test 02: Test 'appCall' object raises 'the requested object cannot be created' LumApiError
- test 03: Test 'appCallWithConstructor' object 'set' and 'get' methods
- test 04: Test 'appCallWithConstructor' object raises 'type added doesn't have property' AttributeError
- test 05: Test 'appCallWithConstructor' object raises 'use an ordered dict for properties' lumWarning
"""

from collections import OrderedDict

import pytest

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestAppCall:
    """Test the lumapi 'appCall' and 'appCallWithConstructor' objects."""

    def test_appcall_with_ordered_dict_properties(self, setup_fdtd):
        """Test 01: Test 'appCall' object with ordered dict properties."""
        prop_dict = OrderedDict(
            [
                ("name", "monitor"),
                ("override global monitor settings", True),
                ("x", 0.0),
                ("y", 0.4e-6),
                ("monitor type", "linear x"),
                ("frequency points", 10.0),
            ]
        )

        setup_fdtd.adddftmonitor(properties=prop_dict)

    def test_appcall_raises_obj_cannot_be_created(self, setup_fdtd):
        """Test 02: Test 'appCall' object raises 'the requested object cannot be created' LumApiError."""
        prop_dict = {
            "name": "monitor 2",
            "override global monitor settings": True,
            "x": 0.0,
            "y": 0.4e-6,
            "monitor type": "linear x",
            "frequency points": 10.0,
        }

        with pytest.raises(lumapi.LumApiError) as ex_info:
            setup_fdtd.adddftmonitor(prop_dict)

        assert "error during property initialization, the requested object cannot be created" in str(ex_info.value)

    def test_appcallwithconstructor_obj_set_and_get(self, setup_fdtd):
        """Test 03: Test 'appCallWithConstructor' object 'set' and 'get' methods."""
        name = "addtriangle"
        method = (lambda x: lambda fdtd, *args, **kwargs: lumapi.appCallWithConstructor(fdtd, x, args, **kwargs))(name)
        method.__name__ = str("my_addtriangle")

        setattr(setup_fdtd, "my_addtriangle", method)

        _ = getattr(setup_fdtd, "my_addtriangle")

        setup_fdtd.my_addtriangle(setup_fdtd)

        obj = setup_fdtd.getObjectById("::model::triangle")

        assert obj.name == "triangle"

    def test_appcallwithconstructor_raises_no_property_error(self, setup_fdtd):
        """Test 04: Test 'appCallWithConstructor' object raises 'type added doesn't have property' AttributeError."""
        prop_dict = OrderedDict(
            [
                ("name", "monitor"),
                ("override_global_monitor_settings", True),
                ("x", 0.0),
                ("y", 0.4e-6),
                ("monitor_type", "linear x"),
                ("frequency_points", 10.0),
            ]
        )

        with pytest.raises(AttributeError) as ex_info:
            setup_fdtd.adddftmonitor(properties=prop_dict)

        assert "Type added by 'adddftmonitor' doesn't have 'override_global_monitor_settings' property" in str(ex_info.value)

    def test_appcallwithconstructor_raises_use_an_ordered_dict_warning(self, setup_fdtd):
        """Test 05: Test 'appCallWithConstructor' object raises 'use an ordered dict for properties' lumWarning."""
        prop_dict = {
            "name": "monitor 2",
            "override global monitor settings": True,
            "x": 0.0,
            "y": 0.4e-6,
            "monitor type": "linear x",
            "frequency points": 10.0,
        }

        def lumapi_lum_warning():
            with pytest.warns(
                UserWarning,
                match=("It is recommended to use an ordered dict for properties," + "as regular dict elements can be re-ordered by Python"),
            ):
                setup_fdtd.adddftmonitor(properties=prop_dict)

            return 1

        assert lumapi_lum_warning() == 1
