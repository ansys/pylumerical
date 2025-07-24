.. _ref_accessing_simulation_results:

Accessing simulation results
=============================

Simulation results are typically stored in datasets simulation or monitor objects Lumerical products. 
This article describes how you can access and process datasets and raw simulation data when using the PyLumerical.

For more information on how PyLumerical translates basic data types and best practices when transferring data, see the article on :doc:`Passing data <passing_data>`, for more information on Lumerical datasets, see the Lumerical Knowledge Base article `Introduction to lumerical datasets <https://optics.ansys.com/hc/en-us/articles/360034409554-Introduction-to-Lumerical-datasets>`__.

Accessing datasets
-------------------

Lumerical products package relevant results in datasets so that you can readily visualize and explore them.
You can use the `getresult <https://optics.ansys.com/hc/en-us/articles/360034409854>`__ method to retrieve these datasets into the Python workspace.

PyLumerical retrieves datasets as dictionaries, with keys associated with various `attributes and parameters <https://optics.ansys.com/hc/en-us/articles/360034409554-Introduction-to-Lumerical-datasets#toc_3>`__.

Dictionaries converted from datasets have a special metadata key ``Lumerical_dataset`` which contains identifier values, this key preserves their structure when performing a roundtrip back to the Lumerical environment. 
When passing a dictionary from Python to Lumerical, PyLumerical converts it into a generic structure, unless it has the metadata element.

Attributes and parameters are both stored as :class:`numpy.ndarray`. Parameters are 1-D arrays that acts as a list of parameters. 
For attributes, the dimension of the array depends on the type of dataset, the type of data, and the number of parameters.

+------------------------+---------------------------------------------------------------------+
| Dataset Type           | Attribute Dimensions                                                |
+========================+=====================================================================+
| Matrix Dataset         | Dimensions depend on type of attribute:                             |
|                        |                                                                     |
|                        | * Scalar attribute: [ |Np1| ; |Np2| ; ... ; |Npn| ]                 |
|                        | * Vector attribute: [ |Np1| ; |Np2| ; ... ; |Npn| ; 3 ]             |
|                        |                                                                     |
|                        | where |Npi| is the length of the |i|\th parameter.                  |
+------------------------+---------------------------------------------------------------------+
| Rectilinear Dataset    | Dimensions depend on type of attribute:                             |
|                        |                                                                     |
|                        | * Scalar attribute: [ |Nx| ; |Ny| ; |Nz| ; |Np1| ; |Np2| ; ... ;    |
|                        |   |Npn| ]                                                           |
|                        | * Vector attribute: [ |Nx| ; |Ny| ; |Nz| ; |Np1| ; |Np2| ; ... ;    |
|                        |   |Npn| ; 3 ]                                                       |
|                        | * Tensor attribute: [ |Nx| ; |Ny| ; |Nz| ; |Np1| ; |Np2| ; ... ;    |
|                        |   |Npn| ; 9 ]                                                       |
|                        |                                                                     |
|                        | where |Nk|, |k| = |x|, |y|, |z| are the lengths of the              |
|                        | coordinate vectors, and |Npi| is the length of the |i|\th           |
|                        | parameter. If the dataset is 2D or 1D, then there                   |
|                        | are singleton dimensions, so that one of |Nk| = 1.                  |               
+------------------------+---------------------------------------------------------------------+
| Unstructured Dataset   | Dimensions depend on type of attribute:                             |
|                        |                                                                     |
|                        | * Scalar attribute: [ |NN| ; |Np1| ; |Np2| ; ... ; |Npn| ; 1 ]      |
|                        | * Vector attribute: [ |NN| ; |Np1| ; |Np2| ; ... ; |Npn| ; 3 ]      |
|                        | * Tensor attribute: [ |NN| ; |Np1| ; |Np2| ; ... ; |Npn| ; 9 ]      |
|                        |                                                                     |
|                        | where |NN| is the number of elements in the unstructured grid.      |
|                        | An extra attribute for the grid connectivity array,                 |
|                        | ``connectivity``, is also a part of the dataset.                    |
+------------------------+---------------------------------------------------------------------+

.. |Np1| replace:: :math:`N_{p1}`
.. |Np2| replace:: :math:`N_{p2}`
.. |Npn| replace:: :math:`N_{pn}`
.. |Nx|  replace:: :math:`N_x`
.. |Ny|  replace:: :math:`N_y`
.. |Nz|  replace:: :math:`N_z`
.. |Nk|  replace:: :math:`N_k`
.. |k|   replace:: :math:`k`
.. |Npi| replace:: :math:`N_{p_i}`
.. |NN|  replace:: :math:`N_N`
.. |x|   replace:: :math:`x`
.. |y|   replace:: :math:`y`
.. |z|   replace:: :math:`z`
.. |i|   replace:: :math:`i`

.. note::
    You can remove singleton dimensions with the `pinch <https://optics.ansys.com/hc/en-us/articles/360034405674>`__ command in Lumerical or :func:`numpy.squeeze` in numpy.

**Example**

The following example uses an example file ‘fdtd_file.fsp’ created using the following script.

.. code-block:: python

    from collections import OrderedDict
    import ansys.lumerical.core as lumapi
    with lumapi.FDTD() as fdtd:
        fdtd.addfdtd(dimension="2D", x=0.0e-9, y=0.0e-9, x_span=3.0e-6, y_span=1.0e-6)
        fdtd.addgaussian(name = 'source', x=0., y=-0.4e-6, injection_axis="y", waist_radius_w0=0.2e-6, wavelength_start=0.5e-6, wavelength_stop=0.6e-6)
        fdtd.addring( x=0.0e-9, y=0.0e-9, z=0.0e-9, inner_radius=0.1e-6, outer_radius=0.2e-6, index=2.0)
        fdtd.addmesh(dx=10.0e-9, dy=10.0e-9, x=0., y=0., x_span=0.4e-6, y_span=0.4e-6)
        fdtd.addtime(name="time", x=0.0e-9, y=0.0e-9)
        fdtd.addprofile(name="profile", x=0., x_span=3.0e-6, y=0.) 

        # Dict ordering is not guaranteed, so if there properties dependant on other properties an ordered dict is necessary
        # In this case 'override global monitor settings' must be true before 'frequency points' can be set    
        props = OrderedDict([("name", "power"),
                            ("override global monitor settings", True),
                            ("x", 0.),("y", 0.4e-6),("monitor type", "linear x"),
                            ("frequency points", 10.0)])
                        
        fdtd.addpower(properties=props)  
        fdtd.save("fdtd_file.fsp")


The following script uses this file to obtain rectilinear datasets.

.. code-block:: python

    import ansys.lumerical.core as lumapi
    with lumapi.FDTD('fdtd_file.fsp') as fdtd:
        fdtd.run()   
        #Return 2 different types of rectilinear datasets
        T, time = fdtd.getresult("power", "T"), fdtd.getresult("time","E")
    
    print('Transmission result T is type', type(T),' with keys', str(T.keys()) )
    print('Time monitor result E is type', type(time),' with keys', str(time.keys()) )

Returns

.. code-block::

    Transmission result T is type <class 'dict'> with keys dict_keys(['lambda', 'f', 'T', 'Lumerical_dataset'])
    Time monitor result E is type <class 'dict'> with keys dict_keys(['t', 'x', 'y', 'z', 'E', 'Lumerical_dataset'])

The following script creates a p-n junction in Lumerical Multiphysics, and returns an unstructured dataset related to its doping.

.. code-block:: python

    from collections import OrderedDict
    import ansys.lumerical.core as lumapi
    with lumapi.DEVICE() as device:
        #Create Simulation region
        device.addsimulationregion(name = "SimRegion", dimension = "2D Y-Normal", x_span = 1.5e-6, z_span = 0.5e-6)
        device.addchargesolver(name = "CHARGE", simulation_region = "SimRegion")

        #Add materials
        device.addmodelmaterial(name = "Silicon")
        device.addmaterialproperties("CT","Si (Silicon)")

        #Add Geometry
        device.addrect(name = "junction", x_span = 2e-6, y_span = 1e-6, z_span = 0.5e-6, material = "Silicon")

        #Add Doping
        device.adddope(name ="n dope", x_min = -1e-6, x_max = 0, dopant_type = "n", concentration = 1e16)
        device.adddope(name ="p dope", x_min = 0, x_max = 1e-6, dopant_type = "p", concentration = 1e16)

        #Add Contacts
        prop_n_contact = OrderedDict([("name", "n_contact"), ("surface type", "simulation region"), ("x min", True)])
        device.addelectricalcontact(properties = prop_n_contact)

        prop_p_contact = OrderedDict([("name", "p_contact"), ("surface type", "simulation region"), ("x max", True)])
        device.addelectricalcontact(properties = prop_p_contact)

        #Save File
        device.save("UnstructuredDatasetTest.ldev")

        #mesh and get doping results
        device.mesh()
        unstructured_result = device.getresult("CHARGE","grid")

        print(f"unstructured_result is of type {type(unstructured_result)} and contains {unstructured_result.keys()}")

Returns

.. code-block::

    unstructured_result is of type <class 'dict'> and contains dict_keys(['area', 'ID', 'x', 'y', 'z', 'connectivity', 'N', 'Lumerical_dataset'])

Accessing raw data
------------------

Raw data from monitors are results in their raw, matrix form. You can also pass these results to the Python workspace using the `getdata <https://optics.ansys.com/hc/en-us/articles/360034409834>`__ command.

PyLumerical retrieves raw data from Lumerical products as :class:`numpy.ndarray` objects.

The length to each dimension of the returned array depends on whether the raw data was originally an attribute or parameter. 
These dimensions follow the dimensions for attributes and parameters described in the “Accessing dataset” section.

**Example**

The following example uses the FDTD project file “fdtd_file.fsp” created above and accesses raw data stored in the profile monitor.

.. code-block:: python

    import ansys.lumerical.core as lumapi
    with lumapi.FDTD('fdtd_file.fsp') as fdtd:
        fdtd.run()

        #Return raw E field data
        Ex = fdtd.getdata("profile","Ex")
        f = fdtd.getdata("profile","f")
        x = fdtd.getdata("profile","x")
        y = fdtd.getdata("profile","y")

    print('Frequency field profile data Ex is type', type(Ex),' with shape', str(Ex.shape))
    print('Frequency field profile data f is type', type(f), 'with shape', str(f.shape))
    print('Frequency field profile data x is type', type(x), 'with shape', str(x.shape))
    print('Frequency field profile data y is type', type(y), 'with shape', str(y.shape))

Returns

.. code-block::

    Frequency field profile data Ex is type with shape (99, 59, 1, 5)
    Frequency field profile data f is type with shape (5, 1)
    Frequency field profile data x is type with shape (99, 1)
    Frequency field profile data y is type with shape (59, 1)

