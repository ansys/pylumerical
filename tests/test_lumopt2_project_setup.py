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

"""Smoke test for lumopt2 project setup: boot Lumerical and build a minimal optimization project."""

from collections import OrderedDict

import ansys.lumerical.core.lumopt2 as lmpt


def test_lumopt2_project_setup():
    """Set up a minimal lumopt2 optimization project and call generate() without running a simulation.

    This test boots a real Lumerical FDTD session and verifies:
    - FdtdSession opens successfully
    - Parametrization, FieldResults, and Fom objects construct correctly
    - Project wires all components together without errors
    - generate() loads the geometry into FDTD, verifies simulation components, and locks
      the mesh — without running any simulation
    """

    def setup_cylinder(fdtd):
        """Minimal FDTD simulation: one cylinder, one plane source, one power monitor."""
        fdtd.addfdtd(z_span=4e-6)
        fdtd.addcircle({"name": "cyl0", "radius": 75e-9, "z min": 0, "z max": 500e-9})
        source_props = OrderedDict([("override global source settings", True), ("wavelength start", 940e-9), ("wavelength stop", 940e-9)])
        fdtd.addgaussian(properties=source_props)
        fdtd.adddftmonitor(name="focus", x=0, y=0, z=1e-6)

    optimization_region = lmpt.Box(
        x_span=1e-6,
        y_span=1e-6,
        z_span=2e-6,
        dx=25e-9,
        dy=25e-9,
        dz=25e-9,
    )

    def param_func(params):
        return OrderedDict({"cyl0::radius": params[0]})

    parametrization = lmpt.Parametrization(
        func=param_func,
        bounds=[(50e-9, 150e-9)],
        optimization_region=optimization_region,
    )

    fom_result = lmpt.FieldResults(monitor_name="focus", metric="intensity", wavelengths=940e-9)
    fom = lmpt.Fom([fom_result])

    session = lmpt.FdtdSession(show_fdtd_cad=False)

    project = lmpt.Project(
        setup=setup_cylinder, parametrization=parametrization, fom=fom, fdtd_session=session, runner=lmpt.LocalRunner(resource="CPU")
    )

    project.generate()

    assert project.generated is True

    session.fdtd.close()
