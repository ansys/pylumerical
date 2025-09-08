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

"""Test INTERCONNECT Simulation Object Property Access Syntax.
- Test 01: test single level property access
- Test 02: test parent children object access with compound
- Test 03: test ordered property initialization
- Test 04: test disabled property initialization fails
- Test 05: test constructor initialization properties
- Test 06: test constructor initialization kwargs
- Test 07: test partial path access
"""

import pytest
import collections
import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestSimulationObjectPropertyAccessSyntax():
    """Test Simulation Object Property Access Syntax."""

    def test_single_level_property_access(self, setup_interconnect):
        """Test 01: test single level property access."""
        intc = setup_interconnect
        
        newElement = intc.addelement()
        newElement.name = "element"
        
        assert newElement["name"] == "element"
        
        intc.deleteall()

    def test_parent_children_object_access_with_compound(self, setup_interconnect):
        """Test 02: test parent children object access with compound."""
        intc = setup_interconnect
        
        outer = intc.addelement(name = "OuterParent")
        intc.groupscope("OuterParent")
        intc.addelement(name = "InnerParent")
        intc.addelement("Optical Amplifier", name = "In Outer")
        intc.groupscope("InnerParent")
        inner = intc.addelement("Optical Amplifier", name = "In Inner")
        intc.groupscope("::Root Element")
        children = outer.getChildren()
        parent = inner.getParent()
        
        assert children[0]["name"] == parent["name"]
        
        intc.deleteall()

    def test_ordered_property_initialization(self, setup_interconnect):
        """Test 03: test ordered property initialization."""
        intc = setup_interconnect
        
        props = collections.OrderedDict()
        props["run diagnostic"] = True
        props["diagnostic size"] = 500
        connector = intc.addelement("electrical connector", properties = props)
        
        assert connector["diagnostic size"] == 500
        
        intc.deleteall()

    def test_disabled_property_initialization_fails(self, setup_interconnect):
        """Test 04: test disabled property initialization fails."""
        intc = setup_interconnect
        
        excepted = False
        try:
            intc.addelement("electrical connector", diagnostic_size = 500)
        except AttributeError:
            excepted = True
        assert excepted
        
        intc.deleteall()

    def test_constructor_initialization_props(self, setup_interconnect):    
        """Test 05: test constructor initialization properties."""
        intc = setup_interconnect
        
        props = collections.OrderedDict()
        props["name"] = "CWLASER"
        props["annotate"] = False
        props["frequency"] = 190
        props["power"] = 1
        props["linewidth"] = 1
        props["phase"] = 2.5
        props["azimuth"] = 1.3
        props["ellipticity"] = 0.5
        props["automatic seed"] = False
        laser = intc.addelement("CW Laser", properties = props)

        for k in props.keys():
            assert laser[k] == props[k]
            
        intc.deleteall()

    def test_constructor_initialization_kwargs(self, setup_interconnect):
        """Test 06: test constructor initialization kwargs."""
        intc = setup_interconnect
        
        laser = intc.addelement("CW Laser", name = "CWLASER", annotate = False, frequency = 190, 
                                power = 1, linewidth = 1, phase = 2.5, azimuth = 1.3, 
                                ellipticity = 0.5, automatic_seed = False)

        assert laser.name == "CWLASER"
        assert laser.annotate == False
        assert laser.frequency == 190
        assert laser.power == 1
        assert laser.linewidth == 1
        assert laser.phase == 2.5
        assert laser.azimuth == 1.3
        assert laser.ellipticity == 0.5
        assert laser.automatic_seed == False
        
        intc.deleteall()

    def test_partial_path_access(self, setup_interconnect):
        """Test 07: test partial path access."""
        intc = setup_interconnect
        
        intc.addelement("Waveguide coupler", name = "coupler 1", x_position = 0, y_position = 0, 
                        coupling_coefficient_1 = 0.3)
        coupler = intc.getObjectById("coupler 1")

        assert coupler.name == "coupler 1"
        assert coupler.x_position == 0
        assert coupler.y_position == 0
        assert coupler.coupling_coefficient_1 == 0.3
        assert coupler.type == "Waveguide Coupler"
        
        intc.deleteall()
