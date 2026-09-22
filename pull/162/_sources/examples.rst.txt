Examples
=========

You can use the examples below to get started with PyLumerical and learn its basic functionalities.

For discussion of PyLumerical concepts, see the :doc:`User guide <user_guide/index>`.

Simulation automation
----------------------

These examples demonstrates basic simulation automation using PyLumerical for various Lumerical products.

.. grid:: 2 2 3 3

   .. grid-item-card:: Session management
      :link: examples/Sessions_and_Objects/basic_session_management/basic_session_management
      :link-type: doc

      This example demonstrates how to initialize a local Lumerical session using PyLumerical.

   .. grid-item-card:: Basic FDTD simulation - Lumerical style commands
      :link: examples/Sessions_and_Objects/fdtd_example1_lsf/fdtd_example1_lsf
      :link-type: doc

      This example demonstrates how to set up a basic FDTD simulation with a Gaussian source and frequency-domain monitor.
      The example uses PyLumerical with workflows and syntax similar to the Lumerical Scripting Language.


   .. grid-item-card:: Basic FDTD simulation - Python style commands
      :link: examples/Sessions_and_Objects/fdtd_example1_pythonic/fdtd_example1_pythonic
      :link-type: doc

      This example demonstrates how to set up a basic FDTD simulation with a Gaussian source and frequency-domain monitor.
      This example uses PyLumerical with workflows and syntax that is more native to Python.

.. grid:: 2 2 3 3

   .. grid-item-card:: Basic MODE simulation - FDE Waveguide
      :link: examples/Single_Solver_Workflows/waveguide_FDE/waveguide_FDE
      :link-type: doc

      This example demonstrates how to set up a basic MODE simulation to calculate the supported modes of a waveguide.

   .. grid-item-card:: Basic HEAT simulation - Thermal Waveguide Tuner
      :link: examples/Single_Solver_Workflows/thermal_tuner_heat/thermal_tuner_heat
      :link-type: doc

      This example demonstrates how to set up and run a simple HEAT simulation to calculate the temperature profile for a thermal waveguide tuner.

   .. grid-item-card:: Using Structure and Analysis Groups - Photonic Crystal Bandstructure
      :link: examples/Single_Solver_Workflows/photonic_crystal_bandstructure/photonic_crystal_bandstructure
      :link-type: doc

      This example uses built-in Lumerical Structure and Analysis Groups to calculate the resonant frequencies of photonic
      crystals using FDTD. Lumerical's built-in sweep tool is used to calculate the full bandstructure.

.. grid:: 2 2 3 3

   .. grid-item-card:: Metalens (RCWA / FDTD)
      :link: examples/Multiple_Solver_Workflows/metalens_FDTD_with_projections/metalens_FDTD_with_projections
      :link-type: doc

      This example runs RCWA simulations to create a unit cell library and constructs a full metalens in FDTD.
      The full metalens is simulated using symmetric boundary conditions in FDTD. A top-down monitor collects the
      fields after the structures and far-field calculations are used to plot the focusing behavior.

   .. grid-item-card:: Basic INTERCONNECT simulation - Ring Resonator
      :link: examples/Single_Solver_Workflows/ring_resonator_interconnect/ring_resonator_interconnect
      :link-type: doc

      This example demonstrates how to set up a basic INTERCONNECT simulation to calculate the transmission spectrum of a ring resonator.

Photonic inverse design
------------------------

These examples focuses on the use of the ``lumopt2`` module for photonic inverse design.

.. grid:: 2 2 3 3

   .. grid-item-card:: Y-branch
      :link: examples/lumopt2/y_branch/pylumerical_y_branch
      :link-type: doc

      This example demonstrates the use of ``lumopt2`` for the inverse design of a Y-branch.
      It utilizes a custom function to enforce symmetric parametrization, and exports the final design to a GDSII file.

   .. grid-item-card:: Color Router
      :link: examples/lumopt2/color_router/color_router_pylumerical
      :link-type: doc

      This example uses ``lumopt2`` with multi-configuration for the inverse design of a color router lens.

.. toctree::
   :hidden:
   :caption: Simulation automation

   examples/Sessions_and_Objects/basic_session_management/basic_session_management
   examples/Sessions_and_Objects/fdtd_example1_lsf/fdtd_example1_lsf
   examples/Sessions_and_Objects/fdtd_example1_pythonic/fdtd_example1_pythonic
   examples/Multiple_Solver_Workflows/metalens_FDTD_with_projections/metalens_FDTD_with_projections
   examples/Single_Solver_Workflows/photonic_crystal_bandstructure/photonic_crystal_bandstructure
   examples/Single_Solver_Workflows/waveguide_FDE/waveguide_FDE
   examples/Single_Solver_Workflows/ring_resonator_interconnect/ring_resonator_interconnect
   examples/Single_Solver_Workflows/thermal_tuner_heat/thermal_tuner_heat
.. toctree::
   :hidden:
   :caption: Photonic inverse design

   examples/lumopt2/y_branch/pylumerical_y_branch
   examples/lumopt2/color_router/color_router_pylumerical