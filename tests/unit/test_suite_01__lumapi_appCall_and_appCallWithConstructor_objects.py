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
Test the lumapi 'appCall' and 'appCallWithConstructor' objects 

 - test 01: Test 'appCall' object with ordered dict properties
 - test 02: Test 'appCall' object raises 'the requested object cannot be created' LumApiError
 - test 03: Test 'appCallWithConstructor' object 'set' and 'get' methods
 - test 04: Test 'appCallWithConstructor' object raises 'type added doesn't have property' AttributeError
 - test 05: Test 'appCallWithConstructor' object raises 'use an ordered dict for properties' lumWarning
"""

from unit_test_setup import *
from collections import OrderedDict


@pytest.fixture(scope="module")
def module_setup():

    print('\n--> Setup')

    global fdtd

    fdtd = lumapi.FDTD(hide=True)

    yield

    print('\n--> Teardown')

    fdtd.close()


def test_01__appCall_with_ordered_dict_properties(module_setup):

    prop_dict = OrderedDict([("name", "monitor"),
                             ("override global monitor settings", True),
                             ("x", 0.),
                             ("y", 0.4e-6),
                             ("monitor type", "linear x"),
                             ("frequency points", 10.0)])

    fdtd.adddftmonitor(properties=prop_dict)


def test_02__appCall_raises_object_cannot_be_created_LumApiError(module_setup):

    prop_dict = {"name": "monitor 2",
                 "override global monitor settings": True,
                 "x": 0.,
                 "y": 0.4e-6,
                 "monitor type": "linear x",
                 "frequency points": 10.0}

    with pytest.raises(lumapi.LumApiError) as ex_info:

        fdtd.adddftmonitor(prop_dict)

    assert 'error during property initialization, the requested object cannot be created' in str(
        ex_info.value)


def test_03__appCallWithConstructor_object_set_and_get(module_setup):

    name = 'addtriangle'
    method = (lambda x: lambda fdtd, *args,
              **kwargs: lumapi.appCallWithConstructor(fdtd, x, args, **kwargs))(name)
    method.__name__ = str('my_addtriangle')

    setattr(fdtd, 'my_addtriangle', method)

    my_method_attr = getattr(fdtd, 'my_addtriangle')

    fdtd.my_addtriangle(fdtd)

    obj = fdtd.getObjectById('::model::triangle')

    assert obj.name == "triangle"


def test_04__appCallWithConstructor_raises_does_not_have_property_AttributeError(module_setup):

    prop_dict = OrderedDict([("name", "monitor"),
                             ("override_global_monitor_settings", True),
                             ("x", 0.),
                             ("y", 0.4e-6),
                             ("monitor_type", "linear x"),
                             ("frequency_points", 10.0)])

    with pytest.raises(AttributeError) as ex_info:

        fdtd.adddftmonitor(properties=prop_dict)

    assert "Type added by 'adddftmonitor' doesn't have 'override_global_monitor_settings' property" in str(
        ex_info.value)


def test_05__appCallWithConstructor_raises_use_an_ordered_dict_lumWarning(module_setup):

    prop_dict = {"name": "monitor 2",
                 "override global monitor settings": True,
                 "x": 0.,
                 "y": 0.4e-6,
                 "monitor type": "linear x",
                 "frequency points": 10.0}

    def lumapi_lum_warning():

        with pytest.warns(UserWarning,
                          match=("It is recommended to use an ordered dict for properties," +
                                 "as regular dict elements can be re-ordered by Python")):

            fdtd.adddftmonitor(properties=prop_dict)

        return 1

    assert lumapi_lum_warning() == 1
