Examples
=========

You can use the examples below to get started with PyLumerical and learn its basic functionalities.

For in-depth discussion of PyLumerical concepts, see the :doc:`User guide <user_guide/index>`.

.. grid:: 2 2 4 4

   .. grid-item-card:: Session management
      :link: examples/Sessions_and_Objects/basic_session_management
      :link-type: doc

      This example demonstrates how to initialize a local Lumerical session using PyLumerical.

   .. grid-item-card:: Basic FDTD simulation - Lumerical style commands
      :link: examples/Sessions_and_Objects/fdtd_example1_lsf
      :link-type: doc

      This example demonstrates how to set up a basic FDTD simulation with a Gaussian source and frequency-domain monitor.
      The example uses PyLumerical with workflows and syntax similar to the Lumerical Scripting Language.


   .. grid-item-card:: Basic FDTD simulation - Python style commands
      :link: examples/Sessions_and_Objects/fdtd_example1_pythonic
      :link-type: doc

      This example demonstrates how to set up a basic FDTD simulation with a Gaussian source and frequency-domain monitor.
      This example uses PyLumerical with workflows and syntax that is more native to Python.

   .. grid-item-card:: FDE MODE Simulation
      :link: examples/Sessions_and_Objects/waveguide_FDE
      :link-type: doc

      This example demonstrates how to set up a basic simulation with Ansys Lumerical MODE™ using the FDE solver.



.. toctree::
   :hidden:

   examples/Sessions_and_Objects/basic_session_management
   examples/Sessions_and_Objects/fdtd_example1_lsf
   examples/Sessions_and_Objects/fdtd_example1_pythonic
   examples/Sessions_and_Objects/waveguide_FDE