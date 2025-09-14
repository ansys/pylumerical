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

"""Test FDTD SimObject.

- Test 01: test SimObject construction
- Test 02: test SimObject construction with no object
- Test 03: test SimObject construction duplicate
- Test 04: test SimObject get attributes
- Test 05: test SimObject set attributes
- Test 06: test SimObject results
"""

import numpy
import pytest

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestSimObject:
    """Test SimObject."""

    def test_sim_object_construction(self, setup_fdtd_with_addfdtd):
        """Test 01: test SimObject construction."""
        fdtd = setup_fdtd_with_addfdtd
        obj = fdtd.getObjectById("::model::FDTD")
        attributes = dir(obj)

        assert "x" in attributes
        assert "y" in attributes
        assert "x span" in attributes
        assert "x_span" not in attributes
        assert "x min bc" in attributes
        assert "same settings on all boundaries" in attributes

        fdtd.deleteall()

    def test_sim_object_construction_no_object(self, setup_fdtd_with_addfdtd):
        """Test 02: test SimObject construction with no object."""
        fdtd = setup_fdtd_with_addfdtd

        with pytest.raises(lumapi.LumApiError) as ex_info:
            _ = fdtd.getObjectById("::model::FDT")

        assert "Object ::model::FDT not found" in str(ex_info.value)

        fdtd.deleteall()

    def test_sim_object_construction_duplicate(self, setup_fdtd):
        """Test 03: test SimObject construction duplicate."""
        fdtd = setup_fdtd
        fdtd.addrect()
        fdtd.set("x", 100e-6)

        def add_rectangle_warning():
            with pytest.warns(UserWarning, match="Multiple objects named '::model::rectangle'."):
                fdtd.addrect()

            return 1

        assert add_rectangle_warning() == 1

        fdtd.set("x", 10e-6)

        def get_object_by_id_warning(id, value):
            with pytest.warns(UserWarning, match="Multiple objects named '::model::rectangle'."):
                obj = fdtd.getObjectById(id)

                assert obj.x == value

            return 1

        assert get_object_by_id_warning("::model::rectangle#1", 100e-6) == 1
        assert get_object_by_id_warning("::model::rectangle#2", 10e-6) == 1

        fdtd.deleteall()

    def test_sim_object_get_attributes(self, setup_fdtd):
        """Test 04: test SimObject get attributes."""
        fdtd = setup_fdtd
        fdtd.addpoly()
        obj = fdtd.getObjectBySelection()
        fdtd.set("x", 1e-3)
        assert obj.x == 1e-3

        fdtd.set("z span", 2e-3)
        assert obj.z_span == 2e-3

        v = numpy.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
        fdtd.set("vertices", v)
        assert (obj.vertices == v).all()

        material = "GaAs - Palik"
        fdtd.set("material", material)
        assert obj.material == material

        fdtd.set("override mesh order from material database", 1)
        assert obj.override_mesh_order_from_material_database == 1

        fdtd.set("first axis", "y")
        assert obj.first_axis == "y"

        fdtd.deleteall()

    def test_sim_object_set_attributes(self, setup_fdtd):
        """Test 05: test SimObject set attributes."""
        fdtd = setup_fdtd
        fdtd.addgaussian()
        obj = fdtd.getObjectBySelection()
        obj.amplitude = 2.5
        assert obj.amplitude == 2.5

        obj.direction = "Backward"
        assert obj.direction == "Backward"

        obj.optimize_for_short_pulse = False
        assert not obj.optimize_for_short_pulse

        obj.override_global_source_settings = False
        assert not obj.override_global_source_settings

        with pytest.raises(lumapi.LumApiError) as ex_info:
            obj.bandwidth = 1

        assert "in setnamed, the requested property 'bandwidth' is inactive" in str(ex_info.value)

        fdtd.deleteall()

    def test_sim_object_results(self, setup_fdtd):
        """Test 06: test SimObject results."""
        fdtd = setup_fdtd
        fdtd.addfdtd()
        obj = fdtd.getObjectBySelection()
        results = dir(obj.results)
        assert "x" in results
        assert "y" in results
        assert "z" in results
        assert "status" in results

        x = obj.results.x

        assert isinstance(x, numpy.ndarray)
        assert len(x.shape) == 2

        with pytest.raises(AttributeError) as ex_info:
            _ = obj.results.xx
        assert "'SimObjectResults' object has no attribute 'xx'" in str(ex_info.value)

        with pytest.raises(lumapi.LumApiError) as ex_info:
            obj.results.y = 1
        assert "Attribute 'y' can not be set" in str(ex_info.value)

        fdtd.deleteall()
