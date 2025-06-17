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
Unit tests for the autodiscovery functionality.

This module tests the detection of Lumerical installation paths across different platforms,
including Windows registry simulation, guessed install paths, and unsupported OS handling.
"""

from pathlib import Path
import platform
import shutil
import sys
import tempfile

import pytest

from ansys.lumerical.core import autodiscovery


def test_locate_lumerical_install_windows_registry(monkeypatch):
    """Test autodiscovery using a simulated Windows registry entry."""
    if platform.system() != "Windows":
        pytest.skip("Windows-specific test")

    # Simulate winreg and registry key
    class DummyKey:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    def dummy_openkey(*args, **kwargs):
        return DummyKey()

    def dummy_queryvalueex(key, value):
        return (str(Path(tempfile.gettempdir()) / "Lumerical"), None)

    monkeypatch.setitem(
        sys.modules,
        "winreg",
        type("winreg", (), {"HKEY_LOCAL_MACHINE": None, "OpenKey": staticmethod(dummy_openkey), "QueryValueEx": staticmethod(dummy_queryvalueex)}),
    )
    Path(tempfile.gettempdir(), "Lumerical").mkdir(exist_ok=True)
    result = autodiscovery.locate_lumerical_install()
    assert result is not None
    shutil.rmtree(Path(tempfile.gettempdir()) / "Lumerical", ignore_errors=True)


def test_locate_lumerical_install_guess(tmp_path):
    """Test autodiscovery using a simulated guessed install path with a custom base path."""
    # Simulate a guessed install path for Linux
    base = tmp_path / "lumerical"
    version_dir = base / "v252"
    api_python = version_dir / "api" / "python"
    api_python.mkdir(parents=True)
    # Use the new base_paths argument to point autodiscovery to our temp structure
    base_paths = [[base, ""]]
    result = autodiscovery.locate_lumerical_install(base_paths=base_paths)
    assert result is not None
    # Platform-independent check for the last two path components
    assert Path(result).parts[-2:] == ("lumerical", "v252")


def test_locate_lumerical_install_unsupported_os(monkeypatch):
    """Test autodiscovery raises on unsupported OS."""
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    with pytest.raises(RuntimeError):
        autodiscovery.locate_lumerical_install()
