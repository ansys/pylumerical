# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Test for starting an FDTD session and verifying variable manipulation using the Lumerical API."""

import ansys.lumerical.core as lumapi  # Import the lumapi module


def test_FDTD_start_session():
    """
    Test the starting of an FDTD session and variable manipulation.

    This test performs the following steps:
    1. Starts an FDTD session with the `hide` parameter set to True.
    2. Adds a variable with a specified name and value to the FDTD session.
    3. Modifies the variable by adding an offset value using the `eval` method.
    4. Reads back the modified variable value.
    5. Asserts that the modified value is equal to the expected value (original value + offset).
    The test ensures that variables can be correctly set, modified, and retrieved within an FDTD session.
    """
    # Start an FDTD session
    with lumapi.FDTD(hide=True) as fdtd:
        # Add a variable
        variable_name = "test_variable"
        variable_value = 42
        fdtd.putv(variable_name, variable_value)

        offset_value = 3
        fdtd.eval(f"{variable_name} =  {offset_value} + {variable_value};")

        # Read back the variable value
        read_value = fdtd.getv(variable_name)

        # Check if the set value and read value are the same
        assert variable_value + offset_value == read_value
