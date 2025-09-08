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

"""Test FDTD Nanowire Example.
- Test 01: test the nanowire example
"""

import pytest
import time
import numpy
import platform
from set_resources import SetResources

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestFdtdNanowireExample():
    """Test FDTD Nanowire Example class."""

    def _run(self, profile_monitor_wavelength = 1e-6):
        """run."""
        self.fdtd.newproject()
        self.fdtd.addcircle()
        self.fdtd.addfdtd()
        self.fdtd.addmesh()
        self.fdtd.addtfsf()
        self.fdtd.addobject("cross_section")
        self.fdtd.set("name", "scat")
        self.fdtd.addobject("cross_section")
        self.fdtd.set("name", "total")
        self.fdtd.addtime()
        self.fdtd.set("name", "time")
        self.fdtd.addprofile()
        self.fdtd.set("name", "profile")

        configuration = (
            ("source", (
                    ("polarization angle", 0.),
                    ("injection axis", "y"),
                    ("x", 0.),
                    ("y", 0.),
                    ("x span", 100.0e-9),
                    ("y span", 100.0e-9),
                    ("wavelength start", 300.0e-9),
                    ("wavelength stop", 400.0e-9))),

            ("mesh", (
                    ("dx", 0.5e-9),
                    ("dy", 0.4e-9),
                    ("x", 0.),
                    ("y", 0.),
                    ("x span", 110.0e-9),
                    ("y span", 110.0e-9))),

            ("FDTD", (
                    ("simulation time", 200e-15), # in seconds
                    ("dimension", "2D"),
                    ("x", 0.0e-9),
                    ("y", 0.),
                    ("z", 0.),
                    ("x span", 800.0e-9),
                    ("y span", 800.0e-9),
                    ("auto scale pml parameters", False),
                    ("mesh refinement", "conformal variant 1"))),

            ("circle", (
                    ("x", 0.0e-9),
                    ("y", 0.0e-9),
                    ("z", 0.0e-9),
                    ("radius", 25.0e-9), # in meters
                    ("material", "Ag (Silver) - Palik (0-2um)"))),

            ("scat", (
                    ("x", 0.),
                    ("y", 0.),
                    ("z", 0.),
                    ("x span", 110.0e-9),
                    ("y span", 110.0e-9))),

            ("total", (
                    ("x", 0.),
                    ("y", 0.),
                    ("z", 0.),
                    ("x span", 90.0e-9),
                    ("y span", 90.0e-9))),

            ("time", (
                    ("x", 28.0e-9),
                    ("y", 26.0e-9))),

            ("profile", (
                    ("x", 0.),
                    ("y", 0.),
                    ("x span", 90e-9),
                    ("y span", 90e-9),
                    ("override global monitor settings", True),
                    ("use source limits", False),
                    ("frequency points", 1),
                    ("wavelength center", float(profile_monitor_wavelength)),
                    ("wavelength span", 0.))),
        )

        for obj, parameters in configuration:
           for k, v in parameters:
               self.fdtd.setnamed(obj, k, v)

        self.fdtd.setnamed("profile", "wavelength center", float(profile_monitor_wavelength))
        
        '''Setting the global frequency resolution.'''
        self.fdtd.setglobalmonitor("frequency points", 100) 
        
        self.fdtd.save(self.project_temp_file)
        self.fdtd.run()
        
        scat_sigma = self.fdtd.getresult("scat", "sigma")
        total_sigma = self.fdtd.getresult("total", "sigma")
        profile_e = self.fdtd.getresult("profile", "E")

        return scat_sigma, total_sigma, profile_e

    def test_nanowire_example(self ):
        """Test 01: test the nanowire example."""
        self.resources = SetResources()
        resources = self.resources.setup("FDTD")
        self.project_temp_file = resources[0]
        self.file_name = resources[1]

        self.fdtd = lumapi.FDTD(hide = True)
      
        start_time = time.time()
        
        sigma_scat, sigma_abs, _ = self._run()

        lam_sim = sigma_scat['lambda'][:,0]
        sigma_scat = sigma_scat['sigma']
        sigma_abs  = sigma_abs['sigma']
        sigma_ext = -sigma_abs + sigma_scat

        '''Load cross section theory from text file.'''
        nw_theory = numpy.genfromtxt("%s_theory.csv" % self.file_name, delimiter = ",")

        lam_theory = nw_theory[:, 0] * 1.e-9
        
        '''Flipping data.'''
        r23 = nw_theory[:, 1:4] * 2 * 23 * 1e-9
        r24 = nw_theory[:, 4:7] * 2 * 24 * 1e-9
        r25 = nw_theory[:, 7:10] * 2 * 25 * 1e-9
        r26 = nw_theory[:, 10:13] * 2 * 26 * 1e-9
        r27 = nw_theory[:, 13:16] * 2 * 27 * 1e-9

        for i in range(0, 3):
            r23[:, i] = numpy.interp(lam_sim, lam_theory, r23[:, i])
            r24[:, i] = numpy.interp(lam_sim, lam_theory, r24[:, i])
            r25[:, i] = numpy.interp(lam_sim, lam_theory, r25[:, i])
            r26[:, i] = numpy.interp(lam_sim, lam_theory, r26[:, i])
            r27[:, i] = numpy.interp(lam_sim, lam_theory, r27[:, i])

        '''Compare FDTD to theory.'''
        rms = lambda x, y : numpy.sqrt(numpy.mean(abs(x - y)))
        assert rms(r25[:, 0], sigma_ext)  < 4.0e-5
        assert rms(r25[:, 1], -sigma_abs) < 4.0e-5
        assert rms(r25[:, 2], sigma_scat) < 4.0e-5

        '''Run the simulation again using the resonance wavelength.'''
        _, _, profile_e = self._run(profile_monitor_wavelength = lam_sim[numpy.argmax(sigma_scat)])
        ref_profile = numpy.load("%s_field_profile.npy" % self.file_name)
        test_profile = profile_e["E"][:, :, 0, 0, 1]
        rel_diff = numpy.max(numpy.abs(test_profile - ref_profile)) / numpy.max(numpy.abs(ref_profile))
        rel_tol = 2e-2
        message = "Largest deviation {:.5f} is larger than rel. tolerance {:.5f}".format(rel_diff, rel_tol)

        assert rel_diff < rel_tol, message
        
        end_time = time.time()
        duration = end_time - start_time
        err_msg = "Test failed due to timeout"

        if platform.system() == "Windows":
            assert duration < 140, err_msg
        else:
            assert duration < 160, err_msg

        self.fdtd.close()

        self.resources.teardown()
