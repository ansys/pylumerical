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

"""Autodiscover the Lumerical installation directory."""

from pathlib import Path
import platform
import re


def locate_lumerical_install():
    r"""
    Locate the installation directory and interop library directory for Lumerical software.

    This function attempts to identify the most recent installation path of Lumerical
    software and its associated Python interop library directory based on the operating
    system and predefined directory structures.

    Returns
    -------
        lumerical_install_dir (str or None): The path to the Lumerical installation directory,
          or None if not found.

    Raises
    ------
        RuntimeError: If the operating system is not Windows or Linux.

    Notes
    -----
        - On Windows, the function searches under "C:\Program Files\Lumerical\" and
          "C:\Program Files\Ansys Inc\Lumerical".
        - On Linux, the function searches under "/opt/lumerical/" and "~/Ansys/ansys_inc/Lumerical".

    Examples
    --------
        Example 1: Use autodiscovery to locate a Lumerical installation in a default location.

        >>> import ansys.lumerical.core as lumapi
        >>> # use lumapi ...

        Example 2: Provide a custom installation path before importing the module.

        >>> import ansys.api.lumerical.lumapi
        >>> ansys.api.lumerical.lumapi.InteropPaths.setLumericalInstallPath(r"C:\Program Files\Lumerical\v252\")
        >>> import ansys.lumerical.core as lumapi
        >>> # use lumapi ...

        Example 3: Provide a custom installation path after importing the module.

        >>> import ansys.lumerical.core as lumapi
        Warning: Lumerical installation not found. Please use InteropPaths.setLumericalInstallPath to set the interop library location.
        >>> lumapi.InteropPaths.setLumericalInstallPath(r"C:\Program Files\Lumerical\v252\")
        >>> # use lumapi ...
    """
    lumerical_install_dir = None

    # TODO(dylanm-ansys): add registry checks on Windows (https://tfs.ansys.com:8443/tfs/ANSYS_Optics/Lumerical/_workitems/edit/45439)

    if platform.system() == "Windows":
        guess_base_and_suffix = [["C:\\Program Files\\Lumerical\\", ""], ["C:\\Program Files\\Ansys Inc\\", "Lumerical"]]
    elif platform.system() == "Linux":
        guess_base_and_suffix = [["/opt/lumerical/", ""], ["~/Ansys/ansys_inc/", "Lumerical"]]
    else:
        raise RuntimeError("Unsupported operating system. Only Windows and Linux are supported.")

    # support 22R1+
    latest_ver_year = 21
    latest_ver_release = 2

    for guess_base, suffix in guess_base_and_suffix:
        if Path(guess_base).exists():
            for dir in Path(guess_base).iterdir():
                if Path(dir, suffix).is_dir():
                    match = re.match(r"v(\d{2})(\d)", dir.name)
                    if match:
                        ver_year = int(match.group(1))
                        ver_maj = int(match.group(2))
                        if ver_year > latest_ver_year or (ver_year == latest_ver_year and ver_maj > latest_ver_release):
                            latest_ver_year = ver_year
                            latest_ver_release = ver_maj
                            # check to make sure the api/python path is there (avoids some false positives from uninstalls)
                            if Path(dir, suffix, "api/python/").exists():
                                lumerical_install_dir = str(Path(dir, suffix))

    return lumerical_install_dir
