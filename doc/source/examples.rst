Examples
=========

You can use the examples below to get started with PyLumerical and learn its basic functionalities.

For in-depth discussion of PyLumerical concepts, see the :doc:`User guide <user_guide/index>`.

.. grid:: 2 2 3 3

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

.. grid:: 2 2 3 3

   .. grid-item-card:: Basic MODE simulation - FDE Waveguide
      :link: examples/Single_Solver_Workflows/waveguide_FDE
      :link-type: doc

      This example demonstrates how to set up a basic MODE simulation to calculate the supported modes of a waveguide.

   .. grid-item-card:: Using Structure and Analysis Groups - Photonic Crystal Bandstructure
      :link: examples/Single_Solver_Workflows/photonic_crystal_bandstructure
      :link-type: doc

      This example uses built-in Lumerical Structure and Analysis Groups to calculate the resonant frequencies of photonic
      crystals using FDTD. Lumerical's built-in sweep tool is used to calculate the full bandstructure.

.. toctree::
   :hidden:

   examples/Sessions_and_Objects/basic_session_management
   examples/Sessions_and_Objects/fdtd_example1_lsf
   examples/Sessions_and_Objects/fdtd_example1_pythonic
   examples/Single_Solver_Workflows/photonic_crystal_bandstructure
   examples/Single_Solver_Workflows/waveguide_FDE