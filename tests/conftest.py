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
"""Define configurations to be shared across test files."""

import pytest

import ansys.api.lumerical.lumapi as lumapi


@pytest.fixture(scope="module")
def setup_interconnect():
    """Set up and tear down interconnect."""
    print("\n--> Setup")
    intc = lumapi.open("interconnect", hide=True)
    yield intc
    print("\n--> Teardown")
    intc.close()


@pytest.fixture(scope="module")
def setup_fdtd():
    """Set up and tear down FDTD."""
    print("\n--> Setup")
    fdtd = lumapi.FDTD(hide=True)
    yield fdtd
    print("\n--> Teardown")
    fdtd.close()


@pytest.fixture(scope="module")
def setup_fdtd_extras():
    """Set up and tear down FDTD with additional groups."""
    print("\n--> Setup")
    fdtd = lumapi.FDTD(hide=True)
    fdtd.addassemblygroup({"name": "assembly_grp"})
    fdtd.addcircle()
    fdtd.addtogroup("assembly_grp")
    yield fdtd
    print("\n--> Teardown")
    fdtd.close()
