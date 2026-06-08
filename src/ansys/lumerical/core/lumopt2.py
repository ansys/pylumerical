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

"""Compatibility alias for importing bundled ``lumopt2`` from PyLumerical namespace."""

from importlib import import_module
import sys

try:
    _lumopt2_module = import_module("lumopt2")
except ModuleNotFoundError as exc:
    # Only rewrap when ``lumopt2`` itself is missing. Leave errors about other
    # modules (e.g. a missing transitive dependency of lumopt2) untouched so the
    # original ``name`` and traceback stay visible.
    if exc.name != "lumopt2":
        raise
    raise ModuleNotFoundError(
        "Could not import bundled 'lumopt2' as 'ansys.lumerical.core.lumopt2'. "
        "This alias requires a Lumerical installation whose 'api/python' directory "
        "contains a 'lumopt2' package. Ensure autodiscovery can locate the install "
        "(for example by setting the LUMERICAL_HOME environment variable) and that "
        "the installed Lumerical version bundles lumopt2.",
        name="lumopt2",
    ) from exc
sys.modules[__name__] = _lumopt2_module
