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

"""Test DEVICE Simulation Object Property Access Syntax.

- Test 01: test single level property access
- Test 02: test nested property access
- Test 03: test parent children object access with materials
- Test 04: test parent children object access with geometries
- Test 05: test parent children object access with solver objects
- Test 06: test ordered property initialization
- Test 07: test constructor initialization properties
- Test 08: test constructor initialization kwargs
- Test 09: test partial path access
- Test 10: test disabled property initialization fails
"""

import collections

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestSimulationObjectPropertyAccessSyntax:
    """Test Simulation Object Property Access Syntax."""

    def test_single_level_property_access(self, setup_device):
        """Test 01: test single level property access."""
        device = setup_device
        device.addrect()
        device.setnamed("::model::geometry::rectangle", "x span", 10.1e-6)
        expected = device.getnamed("::model::geometry::rectangle", "x span")
        actual = device.getObjectById("::model::geometry::rectangle")["x span"]

        assert actual == expected

        device.deleteall()

    def test_nested_property_access(self, setup_device):
        """Test 02: test nested property access."""
        device = setup_device
        alloy_name = "AlInP (Aluminium Indium Phosphide)"
        device.addmodelmaterial()
        device.addmaterialproperties("CT", alloy_name)
        device.setnamed(
            "::model::materials::New Material::AlInP (Aluminium Indium Phosphide)", "electronic.gamma.mup.high field.monotonic.beta.bowing", 3.14e-6
        )
        expected = device.getnamed(
            "::model::materials::New Material::AlInP (Aluminium Indium Phosphide)", "electronic.gamma.mup.high field.monotonic.beta.bowing"
        )
        actual = device.getObjectById("::model::materials::New Material::AlInP (Aluminium Indium Phosphide)")
        actual = actual["electronic"]["gamma"]["mup"]["high field"]["monotonic"]["beta"]["bowing"]

        assert actual == expected

        device.deleteall()

    def test_parent_children_object_access_with_materials(self, setup_device):
        """Test 03: test parent children object access with materials."""
        device = setup_device
        device.addmodelmaterial()
        device.setnamed("New Material", "name", "electrothermal material")
        device.addmaterialproperties("CT", "Air")
        device.select("::model::materials::electrothermal material")
        device.addmaterialproperties("HT", "InAlAs (Indium Aluminium Arsenide)")

        assert (
            device.getObjectById(
                ("::model::materials::electrothermal material" + "::InAlAs (Indium Aluminium Arsenide)" + "::AlAs (Aluminium Arsenide)")
            ).getParent()["name"]
            == "InAlAs (Indium Aluminium Arsenide)"
        )
        assert device.getObjectById("::model::materials::electrothermal material").getParent()["name"] == "materials"

        children_names = [
            c["name"]
            for c in device.getObjectById(("::model::materials::electrothermal material" + "::InAlAs (Indium Aluminium Arsenide)")).getChildren()
        ]

        assert "InAs (Indium Arsenide)" in children_names and "AlAs (Aluminium Arsenide)" in children_names

        device.addmodelmaterial()
        device.setnamed("New Material", "name", "optical material")
        device.addmaterialproperties("EM", "Vacuum")

        assert device.getObjectById("::model::materials::optical material::Vacuum").getParent()["name"] == "optical material"
        assert device.getObjectById("::model::materials::optical material").getChildren()[0]["name"] == "Vacuum"

        device.deleteall()

    def test_parent_children_object_access_with_geometries(self, setup_device):
        """Test 04: test parent children object access with geometries."""
        device = setup_device
        device.addstructuregroup()
        device.setnamed("structure group", "name", "sg0")
        for j in range(1, 5):
            device.addstructuregroup()
            device.setnamed("structure group", "name", "sg" + str(j))
            device.select("sg" + str(j - 1))
            device.addtogroup("sg" + str(j))

        obj = device.getObjectById("::model::geometry")
        obj.getChildren()

        assert device.getObjectById("::model::geometry::sg4::sg3::sg2").getParent().getParent()["name"] == "sg4"
        assert device.getObjectById("::model::geometry::sg4::sg3::sg2").getChildren()[0].getChildren()[0]["name"] == "sg0"

        device.deleteall()

    def test_parent_children_object_access_with_solver_objects(self, setup_device):
        """Test 05: test parent children object access with solver objects."""
        device = setup_device
        device.addchargesolver()
        device.setnamed("::model::CHARGE", "temperature dependence", "coupled")
        device.addtemperaturebc()
        device.addelectricalcontact()
        device.addgroup()
        device.setnamed("::model::CHARGE::new group", "name", "container group")
        device.addtemperaturemonitor()
        device.addtogroup("container group")
        children_names = [c["name"] for c in device.getObjectById("::model::CHARGE::boundary conditions").getChildren()]

        assert "temperature" in children_names and "electrical" in children_names
        assert device.getObjectById("::model::CHARGE::boundary conditions::electrical").getParent()["name"] == "boundary conditions"
        assert device.getObjectById("::model::CHARGE::boundary conditions").getParent()["name"] == "CHARGE"
        assert device.getObjectById("::model::CHARGE::container group").getParent()["name"] == "CHARGE"
        assert device.getObjectById("::model::CHARGE::container group").getChildren()[0]["name"] == "monitor"
        assert device.getObjectById("::model::CHARGE::container group::monitor").getParent()["name"] == "container group"

        device.deleteall()

    def test_ordered_property_initialization(self, setup_device):
        """Test 06: test ordered property initialization."""
        device = setup_device

        props = collections.OrderedDict()
        props["first axis"] = "x"
        props["rotation 1"] = 90
        ring = device.addring(properties=props)

        assert ring["rotation 1"] == 90

        device.deleteall()

    def test_constructor_initialization_props(self, setup_device):
        """Test 07: test constructor initialization properties."""
        device = setup_device

        prop = collections.OrderedDict()
        prop["name"] = "material"
        device.addmodelmaterial(properties=prop)

        props = collections.OrderedDict()
        props["x"] = 100e-6
        props["y"] = 200e-6
        props["z"] = 300e-6
        props["first axis"] = "x"
        props["second axis"] = "y"
        props["third axis"] = "z"
        props["rotation 1"] = 45
        props["rotation 2"] = 90
        props["rotation 3"] = 120
        props["x span"] = 1e-6
        props["y span"] = 2e-6
        props["z span"] = 3e-6
        props["material"] = "material"
        rect = device.addrect(properties=props)

        assert rect["x"] == 100e-6
        assert rect["y"] == 200e-6
        assert rect["z"] == 300e-6
        assert rect["first axis"] == "x"
        assert rect["second axis"] == "y"
        assert rect["third axis"] == "z"
        assert rect["rotation 1"] == 45
        assert rect["rotation 2"] == 90
        assert rect["rotation 3"] == 120
        assert rect["x span"] == 1e-6
        assert rect["y span"] == 2e-6
        assert rect["z span"] == 3e-6
        assert rect["material"] == "material"
        assert rect["type"] == "Rectangle"

        device.deleteall()

    def test_constructor_initialization_kwargs(self, setup_device):
        """Test 08: test constructor initialization kwargs."""
        device = setup_device
        device.addmodelmaterial(name="material")

        rect = device.addrect(x=100e-6, y=200e-6, z=300e-6, x_span=1e-6, y_span=2e-6, z_span=3e-6, material="material")

        assert rect.x == 100e-6
        assert rect.y == 200e-6
        assert rect.z == 300e-6
        assert rect.x_span == 1e-6
        assert rect.y_span == 2e-6
        assert rect.z_span == 3e-6
        assert rect.material == "material"
        assert rect.type == "Rectangle"

        device.deleteall()

    def test_partial_path_access(self, setup_device):
        """Test 09: test partial path access."""
        device = setup_device
        device.addrect(name="rect", x=100e-6, y=200e-6, z=300e-6, x_span=1e-6, y_span=2e-6, z_span=3e-6)
        rect = device.getObjectById("rect")

        assert rect.x == 100e-6
        assert rect.y == 200e-6
        assert rect.z == 300e-6
        assert rect.x_span == 1e-6
        assert rect.y_span == 2e-6
        assert rect.z_span == 3e-6
        assert rect.type == "Rectangle"

        device.deleteall()

    def test_disabled_property_initialization_fails(self, setup_device):
        """Test 10: test disabled property initialization fails."""
        device = setup_device

        props = collections.OrderedDict()
        props["rotation 1"] = 10

        excepted = False
        try:
            device.addring(properties=props)
        except AttributeError:
            excepted = True
        assert excepted

        device.deleteall()
