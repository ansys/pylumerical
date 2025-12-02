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

"""Test lumapi 'Lumerical' children objects 'open' and 'close' methods.

- test 01: Test lumapi 'open' and 'close' FDTD with no arguments
- test 02: Test lumapi 'open' and 'close' FDTD with a project filename argument
- test 03: Test lumapi 'open' and 'close' FDTD with a script filename argument
- test 04: Test lumapi 'open' and 'close' FDTD with an encrypted script filename argument
- test 05: Test lumapi 'open' and 'close' DEVICE with server arguments
- test 06: Test lumapi 'open' DEVICE with invalid server arguments raises LumApiError
- test 07: Test lumapi 'open' DEVICE with invalid remote arguments raises LumApiError
- test 08: Test lumapi 'open' and 'close' MODE
- test 09: Test lumapi 'open' and 'close' INTERCONNECT
- test 10: Test lumapi object raises 'Invalid product name' LumApiError
"""

import os
from pathlib import Path

import pytest

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)

test_path = Path(__file__).parent.absolute()
os.chdir(test_path)


class TestLumericalOpenClose:
    """Test the lumapi 'open' and 'close' functions."""

    def test_open_close_without_arg(self):
        """Test 01: Test lumapi 'open' and 'close' FDTD with no arguments."""
        fdtd = lumapi.FDTD()

        assert isinstance(fdtd, lumapi.FDTD) == 1

        fdtd.close()

    def test_open_close_with_project_filename_arg(self):
        """Test 02: Test lumapi 'open' and 'close' FDTD with a project filename argument."""
        project_file = "fdtd_test.fsp"

        fdtd = lumapi.FDTD(project=project_file, hide=True)

        assert isinstance(fdtd, lumapi.FDTD) == 1

        current_project_file = fdtd.currentfilename()

        assert project_file in current_project_file

        fdtd.close()

    def test_open_close_with_script_filename_arg(self):
        """Test 03: Test lumapi 'open' and 'close' FDTD with a script filename argument."""
        script_file = "fdtd_test.lsf"

        fdtd = lumapi.FDTD(filename=script_file, hide=True)

        assert isinstance(fdtd, lumapi.FDTD) == 1

        obj = fdtd.getObjectById("::model::rectangle")

        assert obj.name == "rectangle"

        fdtd.close()

    def test_open_close_with_encrypted_script_filename_arg(self):
        """Test 04: Test lumapi 'open' and 'close' FDTD with an encrypted script filename argument."""
        script_file = "fdtd_test.lsfx"

        fdtd = lumapi.FDTD(script=script_file, hide=True)

        assert isinstance(fdtd, lumapi.FDTD) == 1

        obj = fdtd.getObjectById("::model::rectangle")

        assert obj.name == "rectangle"

        fdtd.close()

    def test_open_close_device_with_server_args(self):
        """Test 05: Test lumapi 'open' and 'close' DEVICE with server arguments."""
        server_args = {"use-solve": True, "threads": "2"}

        device = lumapi.DEVICE(hide=True, serverArgs=server_args)

        assert isinstance(device, lumapi.DEVICE) == 1

        device.close()

    def test_open_device_invalid_server_args_error(self):
        """Test 06: Test lumapi 'open' DEVICE with invalid server arguments raises LumApiError."""
        server_args = [{"use-solve": True, "threads": "2"}]

        with pytest.raises(lumapi.LumApiError) as ex_info:
            _ = lumapi.DEVICE(hide=True, serverArgs=server_args)

        assert "Server arguments must be in dict format" in str(ex_info.value)

    def test_open_device_invalid_remote_args_error(self):
        """Test 07: Test lumapi 'open' DEVICE with invalid remote arguments raises LumApiError."""
        remote_args = {"hostname": "123.123.123.123", "port": 8989}

        with pytest.raises(lumapi.LumApiError) as ex_info:
            _ = lumapi.DEVICE(hide=True, remoteArgs=remote_args)

        assert "appOpen error: Interop-client: Unable to open the SSL key file" in str(ex_info.value)

    def test_open_close_mode(self):
        """Test 08: Test lumapi 'open' and 'close' MODE."""
        mode = lumapi.MODE(hide=True)

        assert isinstance(mode, lumapi.MODE) == 1

        mode.close()

    def test_open_close_interconnect(self):
        """Test 09: Test lumapi 'open' and 'close' INTERCONNECT."""
        interconnect = lumapi.INTERCONNECT(hide=True)

        assert isinstance(interconnect, lumapi.INTERCONNECT) == 1

        interconnect.close()

    def test_open_invalid_product_name_error(self):
        """Test 10: Test lumapi object raises 'Invalid product name' LumApiError."""
        with pytest.raises(lumapi.LumApiError) as ex_info:
            _ = lumapi.Lumerical("LUMERICAL", filename=None, key=None, hide=False, serverArgs={}, remoteArgs={})

        assert "Invalid product name" in str(ex_info.value)
