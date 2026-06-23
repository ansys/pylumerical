.. _ref_installation:

Installation and getting started
================================

Installation
-------------
|python|

.. |python| image:: https://img.shields.io/pypi/pyversions/ansys-lumerical-core?logo=pypi
   :target: https://pypi.org/project/ansys-lumerical-core/
   :alt: Python

You can install PyLumerical using pip.

First, create a virtual environment and activate it to avoid dependency conflicts and to keep your global Python environment clean.

.. tab-set::

   .. tab-item:: Linux

      .. code-block:: bash

         python -m venv .venv
         source .venv/bin/activate

   .. tab-item:: Windows Command Prompt

      .. code-block:: bash

         python -m venv .venv
         .venv\\Scripts\\activate.bat

   .. tab-item:: Windows Powershell

      .. code-block:: bash

         python -m venv .venv
         .venv\\Scripts\\Activate.ps1

Then, upgrade pip to the latest version, and install PyLumerical with the package name `ansys-lumerical-core`.

.. code:: bash

    python -m pip install -U pip
    python -m pip install ansys-lumerical-core

.. tip::
    Using a virtual environment isn't a requirement, but it's a best practice for Python development.
    PyLumerical is compatible with various Python IDEs including VS Code, Jupyter Notebook, and Cursor. After installation, you can use your preferred editor to start using PyLumerical.

Requirements
-------------

You must have an Ansys Lumerical GUI license along with Lumerical |supported_lum_release| or later on your computer to use PyLumerical. For more information, please visit the `licensing page <https://optics.ansys.com/hc/en-us/articles/360033862333-Lumerical-product-components-and-licensing-overview>`_ on the Ansys Optics website.

Upon importing PyLumerical, the :doc:`autodiscovery <../api/autodiscovery>` logic automatically locates the Lumerical installation path and configures interop.
If autodiscovery fails, set the ``LUMERICAL_HOME`` environment variable before import and start a new Python session.

To use the Lumerical photonic inverse design module lumopt2, you must have Ansys Lumerical FDTD™ version 2026 R1.2 or later installed on your computer. The autodiscovery logic automatically locates the lumopt2 module if it is available.

Importing modules
------------------

To use PyLumerical for simulation automation:

.. code-block:: python

   import ansys.lumerical.core as lumapi

.. tip::

   When imported this way, you can directly use your scripts written with the legacy ``lumapi`` Python module.

To use the ``lumopt2`` inverse design module, use the code below. For further information, see the :doc:`lumopt2 introduction page <../user_guide/photonic_inverse_design_with_lumopt2>`.

.. code-block:: python

   import ansys.lumerical.core.lumopt2 as lmpt

.. warning::

   - To ensure correct functionality, only import ``lumopt2`` through ``ansys.lumerical.core``.
   - Manual ``sys.path`` overrides for ``lumopt2`` are unsupported. The ``lumopt2`` module bundled with Ansys Lumerical products silently takes precedence over those added to ``sys.path``.

.. Turn off vale here due to captizalization issues being wrongly flagged by vale.

.. vale off

My first PyLumerical project
-----------------------------

.. vale on

The code snippet below provides a simple project of using PyLumerical to drive a Lumerical FDTD simulation with an array of nanoholes on a gold film atop a glass substrate.

.. code-block:: python

   # Import modules

   import numpy as np
   import ansys.lumerical.core as lumapi
   import matplotlib.pyplot as plt
   from collections import OrderedDict

   # Define parameters

   filename = "Nanohole_array.fsp"

   # Parameters related to the patterned film
   periodicity = 400e-9 # 400 nm periodic array
   film_thickness = 100e-9
   hole_radius = 100e-9 # radius of the nanoholes
   nx = ny = 3 # Number of nanoholes

   # Parameters for the substrate
   substrate_thickness = 1e-6
   substrate_span = 1.2e-6

   # FDTD region and mesh
   fdtd_z_span = 1e-6 # Ensure span is large enough to capture both T, R monitors
   transmission_z = 0.4e-6 # z position of top "T" monitor
   reflection_z = -0.2e-6 # z position of bottom "R" monitor
   dx = 0.01e-6 # mesh override resolution

   # Source and wavelengths
   source_z = 0.3e-6 # position of source
   wavelength_start = 0.4e-6
   wavelength_stop = 0.7e-6


   # Initialize session and build simulation objects. Set hide = True to hide the Lumerical GUI.

   with lumapi.FDTD(hide = False) as fdtd:

      # Add the substrate
      fdtd.addrect(name = "substrate", x_span = substrate_span, y_span = substrate_span, z_max = 0, z_min = substrate_thickness, material = "SiO2 (Glass) - Palik")

      # Add the gold film
      fdtd.addrect(name = "film", x_span = substrate_span, y_span = substrate_span, z_max = film_thickness, z_min = 0, material = "Au (Gold) - CRC")

      # Add the nanohole array in the gold layer
      # For this, we use the built-in rectangular photonic crystal object from the library
      pc_props = {"name":"nanoholes","material":"etch", "radius": hole_radius, "z": film_thickness/2, "z span": film_thickness,"nx": nx, "ny": ny, "ax": periodicity, "ay": periodicity }
      fdtd.addobject("rect_pc")
      fdtd.set(pc_props)

      # Set up the simulation region
      fdtd_geometry_props = {"x": 0, "x span" : periodicity, "y": 0, "y span" : periodicity, "z": 0, "z span" : fdtd_z_span}
      # Use symmetric boundary conditions in x and y and steep angle PML profile in z
      fdtd_boundary_props = {"allow symmetry on all boundaries": 1, "x min bc" : "anti-symmetric", "x max bc": "anti-symmetric", "y min bc" : "symmetric", "y max bc": "symmetric", "z min bc": "PML", "z max bc": "PML", "pml profile": 3}
      # Combine properties settings into one dictionary
      fdtd_props = OrderedDict({**fdtd_geometry_props, **fdtd_boundary_props})
      fdtd.addfdtd(properties = fdtd_props)

      # Add a mesh override region around the holes
      fdtd.addmesh(dx = dx, dy = dx, dz = dx, based_on_a_structure = 1, structure = "circle")

      # Add plane wave source
      fdtd.addplane(injection_axis = "z-axis", direction = "backward", x_span = substrate_span, y_span = substrate_span, z = source_z)
      fdtd.setglobalsource("wavelength start", wavelength_start)
      fdtd.setglobalsource("wavelength stop", wavelength_stop)

      # Set up frequency domain monitors to measure R and T
      # First, set global monitor properties
      # Source limits will be used by default to define min/max wavelength
      fdtd.setglobalmonitor("frequency points", 50)
      # Now add the monitors
      fdtd.adddftmonitor(name = "T_monitor", monitor_type = "2D Z-normal", x_span = substrate_span, y_span = substrate_span, z = transmission_z)
      fdtd.adddftmonitor(name = "R_monitor", monitor_type = "2D Z-normal", x_span = substrate_span, y_span = substrate_span, z = reflection_z)

      # zoom CAD view around simulation region
      fdtd.select("FDTD")
      fdtd.setview("extent")

      fdtd.save(filename)
      print("File saved to folder as: " + filename)

      # Open the file and run the simulation! Visualize the T/R spectrum.

   with lumapi.FDTD(filename, hide = True) as fdtd:
      print("Starting simulation now...")
      fdtd.run()
      print("Run completed.")

      # Retrieve results
      T = fdtd.getresult("T_monitor","T") # Returns lumerical dataset T vs lambda/f
      R = fdtd.getresult("R_monitor","T")

      # Visualize using matplotlib
      fig, ax = plt.subplots()
      ax.plot(T['lambda']*1e9, T['T'], label="Transmission")
      ax.plot(R['lambda']*1e9, -1*R['T'], label="Reflection") # light traveling along -z so T result is negative
      ax.set_xlabel("Wavelength [nm]")
      ax.set_ylabel("T/R")
      ax.legend()
      plt.show()



Further resources
-----------------

.. grid:: 2 2 3 3

    .. grid-item-card:: User guide
      :link: ../user_guide/index
      :link-type: doc

      Information on key concepts of PyLumerical.

    .. grid-item-card:: API reference
      :link: ../api/index
      :link-type: doc

      Reference for the PyLumerical API.

    .. grid-item-card:: Examples
      :link: ../examples
      :link-type: doc

      Gallery of examples using PyLumerical.

.. grid:: 1 1 1 1

   .. grid-item-card:: Lumerical scripting commands
      :link: https://optics.ansys.com/hc/en-us/articles/360037228834-Lumerical-scripting-language-By-category
      :link-type: url

      Reference for Lumerical scripting commands.


.. grid:: 1 1 1 1

   .. grid-item-card:: Photonic inverse design with lumopt2
      :link: ../user_guide/photonic_inverse_design_with_lumopt2
      :link-type: doc

      Introduction to using lumopt2 for photonic inverse design.

Recommended examples
----------------------

Recommended examples to further build your understanding of PyLumerical and its capabilities.

.. grid:: 2 2 3 3

   .. grid-item-card:: Basic FDTD simulation
      :link: ../examples/Sessions_and_Objects/fdtd_example1_pythonic/fdtd_example1_pythonic
      :link-type: doc

      Run an FDTD simulation using PyLumerical and plot the electric field.

   .. grid-item-card:: Basic MODE simulation
      :link: ../examples/Single_Solver_Workflows/waveguide_FDE/waveguide_FDE
      :link-type: doc

      Run a waveguide simulation in MODE.

   .. grid-item-card:: Basic INTERCONNECT simulation
      :link: ../examples/Single_Solver_Workflows/ring_resonator_interconnect/ring_resonator_interconnect
      :link-type: doc

      Run an an INTERCONNECT simulation for a ring resonator.
