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

"""Test lumapi 'Matrix', 'Rectilinear', and 'UnstructuredDatasetTranslator' objects.

- test 01: Test 'MatrixDatasetTranslator' object
- test 02: Test 'RectilinearDatasetTranslator' object
- test 03: Test 'UnstructuredDatasetTranslator' object
"""

import ansys.api.lumerical.lumapi as lumapi
import ansys.lumerical.core.autodiscovery as autodiscovery

base_install_path = autodiscovery.locate_lumerical_install()
lumapi.InteropPaths.setLumericalInstallPath(base_install_path)


class TestDatasetTranslator:
    """Test the lumapi 'MatrixDatasetTranslator', 'RectilinearDatasetTranslator', and 'UnstructuredDatasetTranslator' objects."""

    def test_matrix_dataset_translator(self, setup_fdtd):
        """Test 01: Test 'MatrixDatasetTranslator' object."""
        setup_fdtd.eval("matrix_dataset = matrixdataset;")
        setup_fdtd.eval('matrix_dataset.addattribute( "scalarAttrib", randmatrix(1) );')
        setup_fdtd.eval('matrix_dataset.addattribute( "vectorAttrib", randmatrix(3) );')

        matrix_dataset = setup_fdtd.getv("matrix_dataset")

        mdt = lumapi.MatrixDatasetTranslator()

        mdt_struct = mdt.createStructMemberPreTranslators(matrix_dataset)

        assert list(mdt_struct.keys()) == ["scalarAttrib", "vectorAttrib"]

        setup_fdtd.putv("matrix_dataset_2", matrix_dataset)

    def test_rectilinear_dataset_translator(self, setup_fdtd):
        """Test 02: Test 'RectilinearDatasetTranslator' object."""
        setup_fdtd.eval("rectilinear_dataset = rectilineardataset( 1:1:4, 1:1:5, 1:1:6 );")
        setup_fdtd.eval('rectilinear_dataset.addattribute( "scalarAttrib", randmatrix( 4, 5, 6 ) );')
        setup_fdtd.eval('rectilinear_dataset.addattribute( "vectorAttrib", randmatrix( 4, 5, 6, 3) );')

        rectilinear_dataset = setup_fdtd.getv("rectilinear_dataset")

        rdt = lumapi.RectilinearDatasetTranslator()

        rdt_struct = rdt.createStructMemberPreTranslators(rectilinear_dataset)

        assert list(rdt_struct.keys()) == ["scalarAttrib", "vectorAttrib"]

        setup_fdtd.putv("rectilinear_dataset_2", rectilinear_dataset)

    def test_unstructured_dataset_translator(self, setup_fdtd):
        """Test 03: Test 'UnstructuredDatasetTranslator' object."""
        setup_fdtd.eval("npts = 13;")
        setup_fdtd.eval("ncell = npts - 1;")
        setup_fdtd.eval("x = linspace( 0, 1, npts );")
        setup_fdtd.eval("y = linspace( 1, 2, npts );")
        setup_fdtd.eval("z = linspace( 2, 3, npts );")
        setup_fdtd.eval("C = zeros( npts - 1, 2 );")
        setup_fdtd.eval("C( :, 1 ) = 1 : ( npts - 1 );")
        setup_fdtd.eval("C( :, 2 ) = 2 : npts;")

        setup_fdtd.eval("unstructured_dataset = unstructureddataset( x, y, z, C );")
        setup_fdtd.eval('unstructured_dataset.addattribute( "scalarAttrib", randmatrix( npts ) );')
        setup_fdtd.eval('unstructured_dataset.addattribute( "vectorAttrib", randmatrix( npts, 3 ) );')
        setup_fdtd.eval('unstructured_dataset.addattribute( "scalarCell",   randmatrix( ncell ) );')
        setup_fdtd.eval('unstructured_dataset.addattribute( "vectorCell",   randmatrix( ncell, 3 ) );')

        unstructured_dataset = setup_fdtd.getv("unstructured_dataset")

        udt = lumapi.UnstructuredDatasetTranslator()

        udt_struct = udt.createStructMemberPreTranslators(unstructured_dataset)

        assert list(udt_struct.keys()).sort() == ["scalarAttrib", "vectorAttrib", "scalarCell", "vectorCell"].sort()

        setup_fdtd.putv("unstructured_dataset_2", unstructured_dataset)
