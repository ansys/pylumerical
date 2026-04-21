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

"""Test bootstrap helpers for bundled ``lumopt2`` support."""

import importlib.util
import sys
import types
from pathlib import Path

import pytest

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core as lumcore
import ansys.lumerical.core.autodiscovery as autodiscovery


def _meta_path_without_lumopt2_guards():
    """Return ``sys.meta_path`` without bundled lumopt2 guard instances."""
    return [finder for finder in sys.meta_path if not isinstance(finder, lumcore._Lumopt2DependencyGuard)]


class TestBootstrapLumopt2:
    """Test import bootstrap helpers for ``lumopt2`` compatibility."""

    def test_get_lumerical_api_python_path_when_available(self, tmp_path):
        """Return ``api/python`` when it exists under the install directory."""
        install_dir = tmp_path / "v261"
        api_python_dir = install_dir / "api" / "python"
        api_python_dir.mkdir(parents=True)

        returned_path = autodiscovery.get_lumerical_api_python_path(install_dir)

        assert Path(returned_path) == api_python_dir.resolve()

    def test_get_lumerical_api_python_path_when_missing(self, tmp_path):
        """Return ``None`` when ``api/python`` does not exist."""
        install_dir = tmp_path / "v261"
        install_dir.mkdir()

        assert autodiscovery.get_lumerical_api_python_path(install_dir) is None

    def test_get_lumerical_api_python_path_when_none(self):
        """Return ``None`` when the install directory is ``None``."""
        assert autodiscovery.get_lumerical_api_python_path(None) is None

    def test_get_bundled_lumopt2_package_dir_when_available(self, tmp_path):
        """Return bundled ``lumopt2`` package path when present."""
        install_dir = tmp_path / "v261"
        bundled_lumopt2_dir = install_dir / "api" / "python" / "lumopt2"
        bundled_lumopt2_dir.mkdir(parents=True)
        (bundled_lumopt2_dir / "__init__.py").write_text("x = 1\n", encoding="utf-8")

        assert Path(lumcore._get_bundled_lumopt2_package_dir(str(install_dir))) == bundled_lumopt2_dir.resolve()

    def test_get_bundled_lumopt2_package_dir_when_missing(self, tmp_path):
        """Return ``None`` when bundled ``lumopt2`` package is absent."""
        install_dir = tmp_path / "v261"
        (install_dir / "api" / "python").mkdir(parents=True)

        assert lumcore._get_bundled_lumopt2_package_dir(str(install_dir)) is None

    def test_resolve_install_dir_uses_autodiscovery(self, monkeypatch, tmp_path):
        """Use autodiscovery and set the interop install path when unset."""
        discovered_install_dir = str(tmp_path / "v261")

        monkeypatch.setattr(lumapi.InteropPaths, "LUMERICALINSTALLDIR", "")
        monkeypatch.setattr(autodiscovery, "locate_lumerical_install", lambda: discovered_install_dir)

        def _fake_set_install_path(install_dir):
            lumapi.InteropPaths.LUMERICALINSTALLDIR = install_dir

        monkeypatch.setattr(
            lumapi.InteropPaths,
            "setLumericalInstallPath",
            staticmethod(_fake_set_install_path),
        )

        assert lumcore._resolve_lumerical_install_dir() == discovered_install_dir
        assert lumapi.InteropPaths.LUMERICALINSTALLDIR == discovered_install_dir

    def test_resolve_install_dir_warns_when_missing(self, monkeypatch):
        """Warn when no install directory can be discovered."""
        monkeypatch.setattr(lumapi.InteropPaths, "LUMERICALINSTALLDIR", "")
        monkeypatch.setattr(autodiscovery, "locate_lumerical_install", lambda: None)

        with pytest.warns(UserWarning, match="Lumerical installation not found"):
            assert lumcore._resolve_lumerical_install_dir() is None

    def test_bind_lumapi_alias_when_missing(self, monkeypatch):
        """Create top-level ``lumapi`` alias when missing."""
        monkeypatch.delitem(sys.modules, "lumapi", raising=False)

        lumcore._bind_lumapi_alias()

        assert sys.modules["lumapi"] is lumapi

    def test_bind_lumapi_alias_fail_fast_on_conflict(self, monkeypatch):
        """Raise when a different ``lumapi`` module is already loaded."""
        conflicting_module = types.ModuleType("lumapi")
        conflicting_module.__file__ = "C:/fake/path/lumapi.py"
        monkeypatch.setitem(sys.modules, "lumapi", conflicting_module)

        with pytest.raises(RuntimeError, match="A different 'lumapi' module is already loaded"):
            lumcore._bind_lumapi_alias()

    def test_bind_lumapi_alias_is_noop_when_already_bound(self, monkeypatch):
        """Do nothing when top-level ``lumapi`` already points to the expected module."""
        monkeypatch.setitem(sys.modules, "lumapi", lumapi)

        lumcore._bind_lumapi_alias()

        assert sys.modules["lumapi"] is lumapi

    def test_validate_lumopt2_origin_fail_fast_on_conflict(self, monkeypatch, tmp_path):
        """Raise when ``lumopt2`` was imported from a non-bundled location."""
        conflicting_module = types.ModuleType("lumopt2")
        conflicting_module.__file__ = "C:/fake/path/lumopt2/__init__.py"
        monkeypatch.setitem(sys.modules, "lumopt2", conflicting_module)

        bundled_lumopt2_dir = tmp_path / "v261" / "api" / "python" / "lumopt2"
        bundled_lumopt2_dir.mkdir(parents=True)
        (bundled_lumopt2_dir / "__init__.py").write_text("x = 1\n", encoding="utf-8")

        with pytest.raises(RuntimeError, match="A different 'lumopt2' module is already loaded"):
            lumcore._validate_lumopt2_origin(str(bundled_lumopt2_dir))

    def test_validate_lumopt2_origin_allows_bundled_module(self, monkeypatch, tmp_path):
        """Allow ``lumopt2`` when imported from bundled ``api/python``."""
        bundled_lumopt2_dir = tmp_path / "v261" / "api" / "python" / "lumopt2"
        bundled_lumopt2_dir.mkdir(parents=True)
        module_file = bundled_lumopt2_dir / "__init__.py"
        module_file.write_text("x = 1\n", encoding="utf-8")

        bundled_module = types.ModuleType("lumopt2")
        bundled_module.__file__ = str(module_file.resolve())
        monkeypatch.setitem(sys.modules, "lumopt2", bundled_module)

        lumcore._validate_lumopt2_origin(str(bundled_lumopt2_dir))

    def test_dependency_guard_ignores_other_modules(self, tmp_path):
        """Guard ignores imports that are not lumopt2."""
        bundled_lumopt2_dir = tmp_path / "v261" / "api" / "python" / "lumopt2"
        bundled_lumopt2_dir.mkdir(parents=True)
        (bundled_lumopt2_dir / "__init__.py").write_text("x = 1\n", encoding="utf-8")
        guard = lumcore._Lumopt2DependencyGuard(str(bundled_lumopt2_dir))
        assert guard.find_spec("numpy", None, None) is None

    def test_dependency_guard_raises_when_bundled_module_missing(self, tmp_path):
        """Guard raises when bundled lumopt2 is absent."""
        bundled_lumopt2_dir = tmp_path / "v261" / "api" / "python" / "lumopt2"
        bundled_lumopt2_dir.mkdir(parents=True)
        guard = lumcore._Lumopt2DependencyGuard(str(bundled_lumopt2_dir))

        with pytest.raises(ModuleNotFoundError, match="may not include lumopt2"):
            guard.find_spec("lumopt2", None, None)

    def test_dependency_guard_raises_on_missing_deps(self, monkeypatch, tmp_path):
        """Guard raises ImportError with install hint when deps are missing."""
        bundled_lumopt2_dir = tmp_path / "v261" / "api" / "python" / "lumopt2"
        bundled_lumopt2_dir.mkdir(parents=True)
        (bundled_lumopt2_dir / "__init__.py").write_text("x = 1\n", encoding="utf-8")
        guard = lumcore._Lumopt2DependencyGuard(str(bundled_lumopt2_dir))

        monkeypatch.setattr(importlib.util, "find_spec", lambda name: None)

        with pytest.raises(ImportError, match=r'ansys-lumerical-core\[lumopt2\]'):
            guard.find_spec("lumopt2", None, None)

    def test_dependency_guard_returns_package_and_module_specs(self, monkeypatch, tmp_path):
        """Guard returns package and module specs when bundled lumopt2 exists."""
        bundled_lumopt2_dir = tmp_path / "v261" / "api" / "python" / "lumopt2"
        bundled_lumopt2_dir.mkdir(parents=True)
        package_init = bundled_lumopt2_dir / "__init__.py"
        package_init.write_text("x = 1\n", encoding="utf-8")
        module_file = bundled_lumopt2_dir / "core.py"
        module_file.write_text("y = 1\n", encoding="utf-8")

        guard = lumcore._Lumopt2DependencyGuard(str(bundled_lumopt2_dir))
        monkeypatch.setattr(importlib.util, "find_spec", lambda name: object())

        package_spec = guard.find_spec("lumopt2", None, None)
        module_spec = guard.find_spec("lumopt2.core", None, None)

        assert package_spec.origin == str(package_init)
        assert module_spec.origin == str(module_file)

    def test_bootstrap_full_flow(self, monkeypatch, tmp_path):
        """Bootstrap configures install path, lumapi alias, and bundled finder."""
        install_dir = tmp_path / "v261"
        bundled_lumopt2_dir = install_dir / "api" / "python" / "lumopt2"
        bundled_lumopt2_dir.mkdir(parents=True)
        (bundled_lumopt2_dir / "__init__.py").write_text("x = 1\n", encoding="utf-8")

        monkeypatch.setattr(lumapi.InteropPaths, "LUMERICALINSTALLDIR", "")
        monkeypatch.setattr(autodiscovery, "locate_lumerical_install", lambda: str(install_dir))

        def _fake_set_install_path(path):
            lumapi.InteropPaths.LUMERICALINSTALLDIR = path

        monkeypatch.setattr(lumapi.InteropPaths, "setLumericalInstallPath", staticmethod(_fake_set_install_path))
        monkeypatch.delitem(sys.modules, "lumapi", raising=False)
        original_sys_path = list(sys.path)
        monkeypatch.setattr(sys, "path", list(original_sys_path), raising=False)
        monkeypatch.setattr(sys, "meta_path", _meta_path_without_lumopt2_guards(), raising=False)

        lumcore._bootstrap_lumerical_environment()

        assert lumapi.InteropPaths.LUMERICALINSTALLDIR == str(install_dir)
        assert sys.modules.get("lumapi") is lumapi
        assert sys.path == original_sys_path
        assert any(isinstance(finder, lumcore._Lumopt2DependencyGuard) for finder in sys.meta_path)

    def test_bootstrap_without_api_python_dir(self, monkeypatch, tmp_path):
        """Bootstrap succeeds when install directory lacks ``api/python/lumopt2``."""
        install_dir = tmp_path / "v261"
        install_dir.mkdir()

        monkeypatch.setattr(lumapi.InteropPaths, "LUMERICALINSTALLDIR", str(install_dir))
        monkeypatch.delitem(sys.modules, "lumapi", raising=False)
        monkeypatch.delitem(sys.modules, "lumopt2", raising=False)
        monkeypatch.setattr(sys, "meta_path", _meta_path_without_lumopt2_guards(), raising=False)

        lumcore._bootstrap_lumerical_environment()

        assert sys.modules.get("lumapi") is lumapi
        assert not any(isinstance(finder, lumcore._Lumopt2DependencyGuard) for finder in sys.meta_path)

    def test_bootstrap_without_api_python_and_lumopt2_loaded(self, monkeypatch, tmp_path):
        """Bootstrap doesn't crash when api/python is missing and lumopt2 is preloaded."""
        install_dir = tmp_path / "v261"
        install_dir.mkdir()

        conflicting = types.ModuleType("lumopt2")
        conflicting.__file__ = "C:/fake/path/lumopt2/__init__.py"
        monkeypatch.setattr(lumapi.InteropPaths, "LUMERICALINSTALLDIR", str(install_dir))
        monkeypatch.setitem(sys.modules, "lumopt2", conflicting)
        monkeypatch.delitem(sys.modules, "lumapi", raising=False)
        monkeypatch.setattr(sys, "meta_path", _meta_path_without_lumopt2_guards(), raising=False)

        lumcore._bootstrap_lumerical_environment()

        assert sys.modules.get("lumapi") is lumapi
