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

"""Test lumapi 'PutTranslator' object raises LumApiError.

- test 01: Test 'PutTranslator' object raises 'Unsupported data type' LumApiError
- test 02: Test 'PutTranslator' object raises 'wrong type for the property' LumApiError
"""

import pytest

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)
# from unit_test_setup import lumapi, pytest


@pytest.fixture(scope="module")
def module_setup():
    """PyTest module setup / tearadown."""
    print("\n--> Setup")

    global fdtd

    fdtd = lumapi.FDTD(hide=True)

    fdtd.addassemblygroup({"name": "assembly_grp"})
    fdtd.addcircle()
    fdtd.addtogroup("assembly_grp")

    yield

    print("\n--> Teardown")

    fdtd.close()


def test_01__puttranslator_raises_unsupported_data_type_lumapierror(module_setup):
    """Test 01: Test 'PutTranslator' object raises 'Unsupported data type' LumApiError."""
    with pytest.raises(lumapi.LumApiError) as excinfo:
        fdtd.setnamed("assembly_grp", "parameters", {"x", "y", "radius"})

    assert "Unsupported data type" in str(excinfo.value)


def test_02__puttranslator_raises_wrong_type_for_the_property_lumapierror(module_setup):
    """Test 02: Test 'PutTranslator' object raises 'wrong type for the property' LumApiError."""
    mapping = [[0, 2, 0, 1], [0, 0, 2, 1], [1, 0.5, 0.5, 1]]

    with pytest.raises(lumapi.LumApiError) as excinfo:
        fdtd.setnamed("assembly_grp", "mapping", mapping)

    assert ("in setnamed, the value supplied is the wrong type " + "for the property 'mapping'") in str(excinfo.value)
