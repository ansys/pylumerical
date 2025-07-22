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
Test lumapi verifyConnection function 

 - test 01: Test 'verifyConnection' function
 - test 02: Test 'verifyConnection' function raises 'Error validating the connection' LumApiError
 - test 03: Test 'verifyConnection' function raises 'Error validating the connection' LumApiError
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


def test_01__verifyConnection(module_setup):

    handle = fdtd.handle

    assert lumapi.verifyConnection(handle) == True


def test_02__verifyConnection_raises_error_validating_the_connection_LumApiError(module_setup):

    handle = fdtd.handle

    fdtd.close()

    with pytest.raises(lumapi.LumApiError) as ex_info:

        lumapi.verifyConnection(handle)

    assert "Error validating the connection" in str(ex_info.value)


def test_03__verifyConnection_raises_error_validating_the_connection_LumApiError(module_setup):

    fdtd = lumapi.open('fdtd', hide=True)

    fdtd.addrect()

    obj = fdtd.getObjectBySelection()

    fdtd.close()

    with pytest.raises(lumapi.LumApiError) as ex_info:

        obj = fdtd.getObjectBySelection()

    assert "Error validating the connection" in str(ex_info.value)
