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

"""Test FDTD Simulation Object Property Access Syntax.
- Test 01: test single level property access
- Test 02: test parent children object access with geometries
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

'''
@pytest.fixture(scope = "module")
def setup_fdtd():
    """Set up and tear down FDTD."""
    print("\n--> Setup")
    fdtd = lumapi.FDTD(hide = True)
    yield fdtd
    print("\n--> Teardown")
    fdtd.close()
'''

class TestSimulationObjectPropertyAccessSyntax():
    """Test Simulation Object Property Access Syntax."""
    
    def test_single_level_property_access(self, setup_fdtd):
        """Test 01: test single level property access."""
        fdtd = setup_fdtd
        fdtd.addrect()
        fdtd.setnamed("::model::rectangle", "x span", 10.1e-6)
        expected = fdtd.getnamed("::model::rectangle", "x span")
        actual = fdtd.getObjectById("::model::rectangle")["x span"]
        
        assert actual == expected
        
        fdtd.deleteall()
    
    def test_parent_children_object_access_with_geometries(self, setup_fdtd):
        """Test 02: test parent children object access with geometries."""
        fdtd = setup_fdtd
        fdtd.addstructuregroup()
        fdtd.setnamed("structure group", "name", "sg0")
        
        for j in range(1, 5):
            fdtd.addstructuregroup()
            fdtd.setnamed("structure group", "name", "sg" + str(j))
            fdtd.select("sg" + str(j - 1))
            fdtd.addtogroup("sg" + str(j))

        obj = fdtd.getObjectById("::model")
        obj.getChildren()
        
        assert fdtd.getObjectById("::model::sg4::sg3::sg2").getParent().getParent()["name"] == "sg4"
        assert fdtd.getObjectById("::model::sg4::sg3::sg2").getChildren()[0].getChildren()[0]["name"] == "sg0"
        
        fdtd.deleteall()
      
    def test_ordered_property_initialization(self, setup_fdtd):
        """Test 03: test ordered property initialization."""
        fdtd = setup_fdtd
        props = collections.OrderedDict()
        props["first axis"] = "x"
        props["rotation 1"] = 90
        ring = fdtd.addring(properties = props)
        
        assert ring["rotation 1"] == 90
        
        fdtd.deleteall()
       
    def test_disabled_property_initialization_fails(self, setup_fdtd):
        """Test 04: test disabled property initialization fails."""
        fdtd = setup_fdtd
        props = collections.OrderedDict()
        props["rotation 1"] = 10
        
        excepted = False
        try:
            fdtd.addring(properties = props)
        except AttributeError:
            excepted = True
        assert excepted
        
        fdtd.deleteall()
        
    def test_constructor_initialization_props(self, setup_fdtd):
        """Test 05: test constructor initialization properties."""
        fdtd = setup_fdtd
        props = collections.OrderedDict()
        props["x"] = 100
        props["y"] = 200
        props["z"] = 300
        props["first axis"] = "x"
        props["second axis"] = "y"
        props["third axis"] = "z"
        props["rotation 1"] = 45
        props["rotation 2"] = 90
        props["rotation 3"] = 120
        props["x span"] = 1e-6
        props["y span"] = 2e-6
        props["z span"] = 3e-6
        
        rect = fdtd.addrect(properties = props)
        
        assert rect["x"] == 100
        assert rect["y"] == 200
        assert rect["z"] == 300
        assert rect["first axis"] == "x"
        assert rect["second axis"] == "y"
        assert rect["third axis"] == "z"
        assert rect["rotation 1"] == 45
        assert rect["rotation 2"] == 90
        assert rect["rotation 3"] == 120
        assert rect["x span"] == 1e-6
        assert rect["y span"] == 2e-6
        assert rect["z span"] == 3e-6
        assert rect["type"] == "Rectangle"

        fdtd.deleteall()

    def test_constructor_initialization_kwargs(self, setup_fdtd):
        """Test 06: test constructor initialization kwargs."""
        fdtd = setup_fdtd
        rect = fdtd.addrect(x = 100, y = 200, z = 300, 
                            x_span = 1e-6, y_span = 2e-6, z_span = 3e-6)
        
        assert rect.x == 100
        assert rect.y == 200
        assert rect.z == 300
        assert rect.x_span == 1e-6
        assert rect.y_span == 2e-6
        assert rect.z_span == 3e-6
        assert rect.type == "Rectangle"

        fdtd.deleteall()
        
    def test_partial_path_access(self, setup_fdtd):
        """Test 07: test partial path access."""
        fdtd = setup_fdtd
        fdtd.addrect(name = "rect", x = 100, y = 200, z = 300, 
                     x_span = 1e-6, y_span = 2e-6, z_span = 3e-6)
        rect = fdtd.getObjectById("rect")

        assert rect.x == 100
        assert rect.y == 200
        assert rect.z == 300
        assert rect.x_span == 1e-6
        assert rect.y_span == 2e-6
        assert rect.z_span == 3e-6
        assert rect.type == "Rectangle"
        
        fdtd.deleteall()
