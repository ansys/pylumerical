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

"""Test the lumapi 'GetSetHelper' object.

- test 01: Test 'GetSetHelper' object 'get' method
- test 02: Test 'GetSetHelper' object 'set' method
- test 03: Test 'GetSetHelper' raises 'property ... has no ... sub-property' AttributeError
"""

import pytest

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


@pytest.fixture(scope="module")
def module_setup():
    """PyTest module setup / tearadown."""
    print("\n--> Setup")

    global intc

    intc = lumapi.open("interconnect", hide=True)

    yield

    print("\n--> Teardown")

    intc.close()


def test_01__getsethelper_get(module_setup):
    """Test 01: Test 'GetSetHelper' object 'get' method."""
    intc.addelement("Waveguide Coupler")
    intc.addelement("Waveguide Coupler")
    intc.selectall()
    intc.createcompound()

    intc.addproperty("COMPOUND_1", "C 1.details", "Standard", "String")

    details = "two couplers"
    intc.select("COMPOUND_1")
    intc.set("C 1.details", details)

    obj = intc.getObjectBySelection()

    assert type(obj.C_1) is lumapi.GetSetHelper

    assert obj.C_1.details == details

    assert obj["C 1"]["details"] == details


def test_02__getsethelper_set(module_setup):
    """Test 02: Test 'GetSetHelper' object 'set' method."""
    obj = intc.getObjectById("::Root Element::COMPOUND_1")

    details = "2 waveguide couplers"
    obj.C_1.details = details

    obj = intc.getObjectBySelection()

    assert obj.C_1.details == details

    details = "2 couplers"
    obj["C 1"]["details"] = details

    obj = intc.getObjectBySelection()

    assert obj.C_1["details"] == details


def test_03__getsethelper_raises_property_has_no_sub_property_attributeerror(module_setup):
    """Test 03: Test 'GetSetHelper' raises 'property ... has no ... sub-property' AttributeError."""
    obj = intc.getObjectById("::Root Element::COMPOUND_1")

    with pytest.raises(AttributeError) as ex_info:
        _ = obj.C_1.xx

    assert "'C 1' property has no 'xx' sub-property" in str(ex_info.value)

    with pytest.raises(AttributeError) as ex_info:
        _ = obj["C 1"]["xx"]

    assert "'C 1' property has no 'xx' sub-property" in str(ex_info.value)

    with pytest.raises(AttributeError) as ex_info:
        obj["C 1"]["xx"] = "qwerty"

    assert "'C 1' property has no 'xx' sub-property" in str(ex_info.value)
