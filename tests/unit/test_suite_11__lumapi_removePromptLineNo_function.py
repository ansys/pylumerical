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
Test lumapi 'removePromptLineNo' function 

 - test 01: Test lumapi 'removePromptLineNo' with a simple string
 - test 02: Test lumapi 'removePromptLineNo' with a string with columns
 - test 03: Test lumapi 'removePromptLineNo' with a string with columns and 'prompt line'
"""

from unit_test_setup import *


def test_01__lumapi_removePromptLineNo_simple_string():

    strval = "remove prompt line number helper function"

    message = lumapi.removePromptLineNo(strval)

    assert message == strval


def test_02__lumapi_removePromptLineNo_string_with_columns():

    strval = "123:456:789"

    message = lumapi.removePromptLineNo(strval)

    assert message == "123:456:789"


def test_03__lumapi_removePromptLineNo_string_with_columns_and_prompt_line():

    strval = "123: prompt line :789"

    message = lumapi.removePromptLineNo(strval)

    assert message == "123:789"
