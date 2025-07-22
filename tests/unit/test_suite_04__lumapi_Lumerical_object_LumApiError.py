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

""" 
Test lumapi 'Lumerical' object raises different 'LumApiError'

 - test 01: Test 'Lumerical' object 'eval' method raises 'Failed to evaluate code' LumApiError
 - test 02: Test 'Lumerical' object 'getv' method raises 'Failed to get variable' LumApiError
 - test 03: Test 'Lumerical' object 'putv' method raises "'SimObject' object has no attribute" LumApiError
 - test 04: Test 'Lumerical' object 'getObjectById' method raises 'Object ... not found' LumApiError
 - test 05: Test 'Lumerical' object 'getObjectBySelection' method raises 'in getid, no items are currently selected' LumApiError
"""

from unit_test_setup import *


@pytest.fixture(scope="module")
def module_setup():

    print('\n--> Setup')

    global fdtd

    fdtd = lumapi.FDTD(hide=True)

    yield

    print('\n--> Teardown')

    fdtd.close()


def test_01__Lumerical_eval_raises_failed_to_evaluate_code_LumApiError(module_setup):

    with pytest.raises(lumapi.LumApiError) as ex_info:

        fdtd.eval("qwerty")

    assert 'Failed to evaluate code' in str(ex_info.value)


def test_02__Lumerical_getv_raises_failed_to_get_variable_LumApiError(module_setup):

    with pytest.raises(lumapi.LumApiError) as ex_info:

        qwerty = fdtd.getv("qwerty")

    assert 'Failed to get variable' in str(ex_info.value)


def test_03__Lumerical_putv_raises_object_has_no_attribute_LumApiError(module_setup):

    fdtd.addfdtd()

    obj = fdtd.getObjectById('::model::FDTD')

    with pytest.raises(AttributeError) as ex_info:

        fdtd.putv("obj", obj)

    assert "'SimObject' object has no attribute" in str(ex_info.value)


def test_04__Lumerical_getObjectById_raises_object_not_found_LumApiError(module_setup):

    fdtd.addrect({"name": "rect1"})

    with pytest.raises(lumapi.LumApiError) as ex_info:

        obj = fdtd.getObjectById('::model::rect_2')

    assert "Object ::model::rect_2 not found" in str(ex_info.value)


def test_05__Lumerical_getObjectBySelection_raises_no_items_are_currently_selected_LumApiError(module_setup):

    fdtd.unselectall()

    with pytest.raises(lumapi.LumApiError) as ex_info:

        obj = fdtd.getObjectBySelection()

    assert 'in getid, no items are currently selected' in str(ex_info.value)
