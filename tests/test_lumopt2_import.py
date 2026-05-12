# Copyright (C) 2025 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Smoke test for lumopt2 import: verify the full import chain and pure data objects."""

import matplotlib

import ansys.lumerical.core.lumopt2 as lmpt


def test_lumopt2_import_and_basics():
    """Verify lumopt2 imports correctly and objects that are often used behaves correctly.

    This test covers:
    - Importing lumopt2 as a user would
    - Checking that lumopt2 has the expected objects important for a typical use case, does not check all objects
    - Ensures visualizer works properly, as matplotlib is only required on that part
    """
    # Version is populated from the bundled installation
    assert lmpt.__version__ is not None

    # Check that key public objects are accessible
    assert hasattr(lmpt, "Box")
    assert hasattr(lmpt, "Project")
    assert hasattr(lmpt, "FdtdSession")
    assert hasattr(lmpt, "Parametrization")
    assert hasattr(lmpt, "Fom")
    assert hasattr(lmpt, "OptimizationVisualizer")

    # OptimizationVisualizer construction triggers the lazy matplotlib import
    matplotlib.use("Agg")  # non-interactive backend for CI/CD
    viz = lmpt.OptimizationVisualizer()
    assert viz is not None
