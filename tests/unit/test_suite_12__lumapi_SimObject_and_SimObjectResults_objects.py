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

"""Test lumapi 'SimObject' and 'SimObjectResults' objects.

- test 01: Test 'Lumerical' object 'getAllSelectedObjects' returns as 'SimObject' list
- test 02: Test 'Lumerical' object 'getObjectById_SimObject
- test 03: Test 'Lumerical' object 'getObjectBySelection_SimObject
- test 04: Test 'SimObjectResults' object raises 'SimObjectResults has no attribute' AttributeError
- test 05: Test 'SimObject' object raises 'attribute can not be set' LumApiError
- test 06: Test 'SimObject' object 'getParent' and 'getChildren' methods
"""

import numpy as np
import pytest

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


@pytest.fixture(scope="module")
def module_setup():
    """PyTest module setup / tearadown."""
    print("\n--> Setup")

    global fdtd

    fdtd = lumapi.FDTD(hide=True)

    fdtd.addfdtd()

    yield

    print("\n--> Teardown")

    fdtd.close()


def test_01__lumerical_getallselectedobjects_simobject_list(module_setup):
    """Test 01: Test 'Lumerical' object 'getAllSelectedObjects' returns as 'SimObject' list."""
    obj_lst = fdtd.getAllSelectedObjects()

    assert len(obj_lst) == 1

    obj = obj_lst[0]

    attributes = dir(obj)

    assert "x" in attributes
    assert "y" in attributes
    assert "x span" in attributes
    assert "x_span" not in attributes
    assert "x min bc" in attributes
    assert "same settings on all boundaries" in attributes


def test_02__lumerical_getobjectbyid_simobject(module_setup):
    """Test 02: Test 'Lumerical' object 'getObjectById_SimObject."""
    obj = fdtd.getObjectById("::model::FDTD")

    attributes = dir(obj)

    assert "x" in attributes
    assert "y" in attributes
    assert "x span" in attributes
    assert "x_span" not in attributes
    assert "x min bc" in attributes
    assert "same settings on all boundaries" in attributes


def test_03__lumerical_getobjectbyselection_simobject(module_setup):
    """Test 03: Test 'Lumerical' object 'getObjectBySelection_SimObject."""
    obj = fdtd.getObjectBySelection()

    results = dir(obj.results)

    assert "x" in results
    assert "y" in results
    assert "z" in results
    assert "status" in results

    x = obj.results.x

    assert isinstance(x, np.ndarray)
    assert len(x.shape) == 2


def test_04__simobjectresults_raises_simobjectresults_has_no_attribute_attributeerror(module_setup):
    """Test 04: Test 'SimObjectResults' object raises 'SimObjectResults has no attribute' AttributeError."""
    obj = fdtd.getObjectBySelection()

    with pytest.raises(AttributeError) as ex_info:
        _ = obj.results.xx

    assert "'SimObjectResults' object has no attribute 'xx'" in str(ex_info.value)


def test_05__simobject_raises_attribute_can_not_be_set_lumapierror(module_setup):
    """Test 05: Test 'SimObject' object raises 'attribute can not be set' LumApiError."""
    obj = fdtd.getObjectBySelection()

    with pytest.raises(lumapi.LumApiError) as ex_info:
        obj.results.y = 1

    assert "Attribute 'y' can not be set" in str(ex_info.value)


def test_06__simobject_getparent_and_getchildren(module_setup):
    """Test 06: Test 'SimObject' object 'getParent' and 'getChildren' methods."""
    fdtd.addstructuregroup({"name": "group1"})
    fdtd.addrect({"name": "rect1"})
    fdtd.select("rect1")
    fdtd.addtogroup("group1")
    fdtd.select("group1")

    obj = fdtd.getObjectBySelection()

    parent = obj.getParent()
    child_lst = obj.getChildren()

    assert len(child_lst) == 1

    child = child_lst[0]

    assert child.name == "rect1"

    assert parent.name == "model"
