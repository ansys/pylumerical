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

"""Set up the imports for PyLumerical."""

import importlib.abc
import importlib.util
from pathlib import Path
import sys
import warnings

import ansys.api.lumerical
import ansys.api.lumerical.lumapi as _ansys_lumapi_module

# Make common names from lumapi available in the top-level namespace
from ansys.api.lumerical.lumapi import DEVICE, FDTD, INTERCONNECT, MODE, InteropPaths, SimObject, SimObjectId, SimObjectResults

from . import autodiscovery

_INSTALL_NOT_FOUND_MESSAGE = (
    "Lumerical installation not found. Set the LUMERICAL_HOME environment variable "
    "or call InteropPaths.setLumericalInstallPath() to configure the path manually."
)

__version__ = "0.1.dev0"
"""Lumerical API version."""


def _normalize_path(path):
    """Normalize a path for robust comparisons."""
    normalized_path = str(Path(path).resolve())
    if sys.platform.startswith("win"):
        return normalized_path.casefold()
    return normalized_path


def _resolve_lumerical_install_dir():
    """Resolve and configure the Lumerical installation directory."""
    install_dir = _ansys_lumapi_module.InteropPaths.LUMERICALINSTALLDIR
    if len(install_dir) == 0:
        install_dir = autodiscovery.locate_lumerical_install()
        if install_dir is not None:
            _ansys_lumapi_module.InteropPaths.setLumericalInstallPath(install_dir)
        else:
            warnings.warn(_INSTALL_NOT_FOUND_MESSAGE, stacklevel=2)
    return install_dir


def _get_bundled_lumopt2_package_dir(lumerical_install_dir):
    """Get bundled ``lumopt2`` package path from a Lumerical installation."""
    api_python_path = autodiscovery.get_lumerical_api_python_path(lumerical_install_dir)
    if api_python_path is None:
        return None

    lumopt2_package_dir = Path(api_python_path, "lumopt2")
    if lumopt2_package_dir.is_dir() and Path(lumopt2_package_dir, "__init__.py").is_file():
        return str(lumopt2_package_dir.resolve())

    return None


def _validate_lumopt2_origin(bundled_lumopt2_package_dir):
    """Ensure a preloaded ``lumopt2`` module comes from bundled package path."""
    existing_lumopt2_module = sys.modules.get("lumopt2")
    if existing_lumopt2_module is None:
        return

    existing_path = getattr(existing_lumopt2_module, "__file__", None)
    if existing_path is None:
        return

    normalized_existing_path = _normalize_path(existing_path)
    normalized_bundled_path = _normalize_path(bundled_lumopt2_package_dir)
    if not normalized_existing_path.startswith(normalized_bundled_path):
        raise RuntimeError(
            "A different 'lumopt2' module is already loaded "
            f"({existing_path}). PyLumerical requires the bundled module under {bundled_lumopt2_package_dir}. "
            "Remove custom lumopt2 path overrides and import ansys.lumerical.core first."
        )


def _bind_lumapi_alias():
    """Ensure top-level ``lumapi`` resolves to ``ansys.api.lumerical.lumapi``."""
    existing_lumapi_module = sys.modules.get("lumapi")
    if existing_lumapi_module is None:
        sys.modules["lumapi"] = _ansys_lumapi_module
        return

    if existing_lumapi_module is not _ansys_lumapi_module:
        existing_path = getattr(existing_lumapi_module, "__file__", "<unknown>")
        expected_path = getattr(_ansys_lumapi_module, "__file__", "<unknown>")
        raise RuntimeError(
            "A different 'lumapi' module is already loaded "
            f"({existing_path}). PyLumerical requires {expected_path}. "
            "Import ansys.lumerical.core before importing lumapi or lumopt2."
        )


class _Lumopt2DependencyGuard(importlib.abc.MetaPathFinder):
    """Load bundled ``lumopt2`` and raise clear errors when unsupported."""

    _REQUIRED_DEPS = ("autograd", "scipy")
    _INSTALL_HINT = 'Install them with: pip install "ansys-lumerical-core[lumopt2]"'

    def __init__(self, bundled_lumopt2_package_dir):
        self._bundled_lumopt2_package_dir = Path(bundled_lumopt2_package_dir).resolve()
        self._bundled_api_python_dir = self._bundled_lumopt2_package_dir.parent

    def _resolve_module_file(self, fullname):
        if fullname == "lumopt2":
            init_file = Path(self._bundled_lumopt2_package_dir, "__init__.py")
            return init_file if init_file.is_file() else None

        relative_parts = fullname.split(".")[1:]
        relative_path = Path(*relative_parts)
        package_init = Path(self._bundled_lumopt2_package_dir, relative_path, "__init__.py")
        if package_init.is_file():
            return package_init

        module_file = Path(self._bundled_lumopt2_package_dir, relative_path).with_suffix(".py")
        if module_file.is_file():
            return module_file

        return None

    def find_spec(self, fullname, path, target=None):
        """Load bundled lumopt2 modules and enforce dependency checks."""
        if fullname != "lumopt2" and not fullname.startswith("lumopt2."):
            return None

        module_file = self._resolve_module_file(fullname)
        if module_file is None:
            raise ModuleNotFoundError(
                f"Bundled module '{fullname}' was not found under {self._bundled_api_python_dir}. "
                "This Lumerical installation may not include lumopt2."
            )

        missing = [dep for dep in self._REQUIRED_DEPS if importlib.util.find_spec(dep) is None]
        if missing:
            raise ImportError(f"lumopt2 requires {', '.join(missing)}. {self._INSTALL_HINT}")

        if module_file.name == "__init__.py":
            return importlib.util.spec_from_file_location(
                fullname,
                str(module_file),
                submodule_search_locations=[str(module_file.parent)],
            )
        return importlib.util.spec_from_file_location(fullname, str(module_file))


def _install_lumopt2_dependency_guard(bundled_lumopt2_package_dir):
    """Register a finder that exposes bundled ``lumopt2`` only."""
    normalized_bundled_path = _normalize_path(bundled_lumopt2_package_dir)
    for index, finder in enumerate(sys.meta_path):
        if isinstance(finder, _Lumopt2DependencyGuard):
            existing_bundled_path = _normalize_path(str(finder._bundled_lumopt2_package_dir))
            if existing_bundled_path == normalized_bundled_path:
                return
            sys.meta_path.pop(index)
            break
    sys.meta_path.insert(0, _Lumopt2DependencyGuard(bundled_lumopt2_package_dir))


def _bootstrap_lumerical_environment():
    """Bootstrap Lumerical interop paths and module aliases."""
    install_dir = _resolve_lumerical_install_dir()
    if install_dir is not None:
        bundled_lumopt2_package_dir = _get_bundled_lumopt2_package_dir(install_dir)
        if bundled_lumopt2_package_dir is not None:
            _validate_lumopt2_origin(bundled_lumopt2_package_dir)
            _install_lumopt2_dependency_guard(bundled_lumopt2_package_dir)
    _bind_lumapi_alias()


_bootstrap_lumerical_environment()
