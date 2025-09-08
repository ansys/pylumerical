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

"""Test INTERCONNECT Monte Carlo Example.
- Test 01: test monte carlo example
"""

import pytest
import os
import shutil
import numpy
from set_resources import SetResources

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestInterconnectMonteCarloExample():
    """Test INTERCONNECT Monte Carlo Example."""

    def test_monte_carlo_example(self):
        """Test 01: test monte carlo example."""
        self.resources = SetResources()
        resources = self.resources.setup("INTERCONNECT")
        self.project_temp_file = resources[0]
        self.file_name = resources[1]

        self.intc = lumapi.INTERCONNECT(project = self.project_temp_file, hide = True)

        self.intc.addsweep(2)
        mc_name = "MC_script"
        self.intc.setsweep("Monte Carlo analysis", "name", mc_name)

        sweep_setup = {
            "number of trials": 8,
            "enable seed": True,
            "seed": 1.0,
            "Variation": "Both",
            "type": "Parameters",
        }

        for k, v in sweep_setup.items():
            self.intc.setsweep(mc_name, k, v)

        sweep_parameters = [
            { 
                "Name": "cpl_2",
                "Parameter": "::Root Element::WC2::coupling coefficient 1",
                "Value": self.intc.getnamed("WC2", "coupling coefficient 1"),
                "Distribution": {
                    "type": "gaussian",
                    "variation": 0.02
                }
            },

            {
                "Name": "cpl_3",
                "Parameter": "::Root Element::WC3::coupling coefficient 1",
                "Value": self.intc.getnamed("WC3", "coupling coefficient 1"),
                "Distribution": {
                    "type": "uniform",
                    "variation": 0.04
                }
            },

            {
                "Name": "wgd_model",
                "Model": "WGD::group index 1",
                "Value": self.intc.getnamed("SW1", "group index 1"),
                "Process": {
                    "type": "uniform",
                    "variation": 1.02
                },
                "Mismatch": {
                    "type": "gaussian",
                    "variation": 0.1
                }
            },

            {
                "Name": "wgd_corr",
                "Parameters": "SW1_group_index_1,SW2_group_index_1,SW3_group_index_1",
                "Value": 0.95
            }
        ]

        sweep_results = [
            {
                "Name": "fsr",
                "Result": "::Root Element::Optical Network Analyzer::input 2/mode 1/peak/free spectral range",
                "Estimation": True,
                "Min": 1.0e11,
                "Max": 2.0e11
            },

            {
                "Name": "bd",
                "Result": "::Root Element::Optical Network Analyzer::input 1/mode 1/peak/bandwidth",
                "Estimation": False
            },

            {
                "Name": "gain",
                "Result": "::Root Element::Optical Network Analyzer::input 1/mode 1/peak/gain",
                "Estimation": False
            }
        ]

        for parameter in sweep_parameters:
            self.intc.addsweepparameter(mc_name, parameter)

        for result in sweep_results:
            self.intc.addsweepresult(mc_name, result)

        self.intc.runsweep(mc_name)

        fsr = self.intc.getsweepresult(mc_name, "analysis/results/histogram/fsr")
        
        assert numpy.array_equal(fsr["count"], [4, 1, 1, 2])
        assert numpy.array_equal(fsr["fsr"][0][0], [1.001e+11, 1.035e11, 1.069e11, 1.103e11])

        pdf = self.intc.getsweepresult(mc_name, "analysis/results/pdf/fsr")
        
        assert numpy.allclose(pdf["count"], numpy.load("%s_pdf_count.npy" % self.file_name), atol = 1e-12)
        assert numpy.allclose(pdf["fsr"][0][0], numpy.load("%s_pdf_fsr.npy" % self.file_name), atol = 1e-12)

        self.intc.close()

        self.resources.teardown()
