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

"""Test DEVICE SimObject Properties.

- Test 01: test composition fraction property
- Test 02: test optical material property construction
- Test 03: test thermal material property construction
"""

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestSimObjectProperties:
    """Test SimObject Properties."""

    def test_composition_fraction_property(self, setup_device):
        """Test 01: test composition fraction property."""
        device = setup_device
        device.addrect()
        device.set("name", "Rect")
        obj = device.getObjectById("::model::geometry::Rect")
        attributes = dir(obj)

        assert not any(["." in name for name in attributes])

        device.deleteall()

    def test_optical_material_property_construction(self, setup_device):
        """Test 02: test optical material property construction."""
        device = setup_device
        device.addmodelmaterial()
        device.set("name", "Test")
        device.addemmaterialproperty("Dielectric")
        device.set("name", "Optical")
        obj = device.getObjectById("::model::materials::Test::Optical")
        attributes = dir(obj)

        assert "refractive index" in attributes

        device.deleteall()

    def test_thermal_material_property_construction(self, setup_device):
        """Test 03: test thermal material property construction."""
        device = setup_device
        device.addmodelmaterial()
        device.set("name", "Test")
        device.addhtmaterialproperty("Solid")
        device.set("name", "Thermal")
        obj = device.getObjectById("::model::materials::Test::Thermal")
        attributes = dir(obj)

        assert not any(["." in name for name in attributes])

        device.deleteall()
