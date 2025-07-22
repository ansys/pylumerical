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
Test lumapi 'Matrix', 'Rectilinear', and 'UnstructuredDatasetTranslator' objects 

 - test 01: Test 'MatrixDatasetTranslator' object
 - test 02: Test 'RectilinearDatasetTranslator' object
 - test 03: Test 'UnstructuredDatasetTranslator' object
"""

from unit_test_setup import *


@pytest.fixture(scope="module")
def module_setup():

    print('\n--> Setup')

    global fdtd

    fdtd = lumapi.FDTD(hide=True)

    yield

    print('\n--> Teardown')

    fdtd.close()


def test_01__MatrixDatasetTranslator(module_setup):

    fdtd.eval(f'matrix_dataset = matrixdataset;')
    fdtd.eval(f'matrix_dataset.addattribute( "scalarAttrib", randmatrix(1) );')
    fdtd.eval(f'matrix_dataset.addattribute( "vectorAttrib", randmatrix(3) );')

    matrix_dataset = fdtd.getv("matrix_dataset")

    mdt = lumapi.MatrixDatasetTranslator()

    mdt_struct = mdt.createStructMemberPreTranslators(matrix_dataset)

    assert list(mdt_struct.keys()) == ['scalarAttrib', 'vectorAttrib']

    fdtd.putv("matrix_dataset_2", matrix_dataset)


def test_02__RectilinearDatasetTranslator(module_setup):

    fdtd.eval(f'rectilinear_dataset = rectilineardataset( 1:1:4, 1:1:5, 1:1:6 );')
    fdtd.eval(
        f'rectilinear_dataset.addattribute( "scalarAttrib", randmatrix( 4, 5, 6 ) );')
    fdtd.eval(
        f'rectilinear_dataset.addattribute( "vectorAttrib", randmatrix( 4, 5, 6, 3) );')

    rectilinear_dataset = fdtd.getv("rectilinear_dataset")

    rdt = lumapi.RectilinearDatasetTranslator()

    rdt_struct = rdt.createStructMemberPreTranslators(rectilinear_dataset)

    assert list(rdt_struct.keys()) == ['scalarAttrib', 'vectorAttrib']

    fdtd.putv("rectilinear_dataset_2", rectilinear_dataset)


def test_03__UnstructuredDatasetTranslator(module_setup):

    fdtd.eval(f'npts = 13;')
    fdtd.eval(f'ncell = npts - 1;')
    fdtd.eval(f'x = linspace( 0, 1, npts );')
    fdtd.eval(f'y = linspace( 1, 2, npts );')
    fdtd.eval(f'z = linspace( 2, 3, npts );')
    fdtd.eval(f'C = zeros( npts - 1, 2 );')
    fdtd.eval(f'C( :, 1 ) = 1 : ( npts - 1 );')
    fdtd.eval(f'C( :, 2 ) = 2 : npts;')

    fdtd.eval(f'unstructured_dataset = unstructureddataset( x, y, z, C );')
    fdtd.eval(
        f'unstructured_dataset.addattribute( "scalarAttrib", randmatrix( npts ) );')
    fdtd.eval(
        f'unstructured_dataset.addattribute( "vectorAttrib", randmatrix( npts, 3 ) );')
    fdtd.eval(
        f'unstructured_dataset.addattribute( "scalarCell",   randmatrix( ncell ) );')
    fdtd.eval(
        f'unstructured_dataset.addattribute( "vectorCell",   randmatrix( ncell, 3 ) );')

    unstructured_dataset = fdtd.getv("unstructured_dataset")

    udt = lumapi.UnstructuredDatasetTranslator()

    udt_struct = udt.createStructMemberPreTranslators(unstructured_dataset)

    assert list(udt_struct.keys()).sort() == [
        'scalarAttrib', 'vectorAttrib', 'scalarCell', 'vectorCell'].sort()

    fdtd.putv("unstructured_dataset_2", unstructured_dataset)
