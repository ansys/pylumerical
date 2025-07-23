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

"""Test lumapi 'open' and 'close' functions.

- test 01: Test lumapi 'open' and 'close' FDTD
- test 02: Test lumapi 'open' and 'close' DEVICE
- test 03: Test lumapi 'open' and 'close' MODE
- test 04: Test lumapi 'open' and 'close' INTERCOINNECT
- test 05: Test lumapi 'open' unexpected app raises 'product not available' LumApiError
"""

from unit_test_setup import lumapi, pytest


def test_01__lumapi_open_close_fdtd():
    """Test 01: Test lumapi 'open' and 'close' FDTD."""
    fdtd = lumapi.open("fdtd", hide=True)

    assert isinstance(fdtd, lumapi.Lumerical) == 1

    assert isinstance(fdtd, lumapi.FDTD) == 1

    lumapi.close(fdtd)


def test_02__lumapi_open_close_device():
    """Test 02: Test lumapi 'open' and 'close' DEVICE."""
    device = lumapi.open("device", hide=True)

    handle = device.handle

    assert isinstance(device, lumapi.DEVICE) == 1

    assert isinstance(handle, lumapi.LumApiSession) == 1

    lumapi.close(device)


def test_03__lumapi_open_close_mode():
    """Test 03: Test lumapi 'open' and 'close' MODE."""
    mode = lumapi.open("mode", hide=True)

    assert isinstance(mode, lumapi.MODE) == 1

    lumapi.close(mode)


def test_04__lumapi_open_close_interconnect():
    """Test 04: Test lumapi 'open' and 'close' INTERCOINNECT."""
    interconnect = lumapi.open("interconnect", hide=True)

    assert isinstance(interconnect, lumapi.INTERCONNECT) == 1

    lumapi.close(interconnect)


def test_05__lumapi_open_unexpected_app_raises_product_not_available_lumapierror():
    """Test 05: Test lumapi 'open' unexpected app raises 'product not available' LumApiError."""
    product = "UNEXPECTED"

    with pytest.raises(lumapi.LumApiError) as ex_info:
        _ = lumapi.open(product, hide=True)

    assert "Product [" + product + "] is not available" in str(ex_info.value)
