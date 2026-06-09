.. _ref_user_guide:

User guide
========================
Use Python to analyze data, automate complex workflows, optimizations, and produce publication-quality plots. PyLumerical provides a method to seamlessly use Python to interact with Ansys Lumerical products.

This user guide provides important informational resources on key concepts of PyLumerical.

.. _simulation-automation:

Simulation automation
----------------------

The guides below discusses using lumapi to automate Lumerical simulations with Python.

.. grid:: 2 2 3 3

   .. grid-item-card:: Session management
      :link: session_management
      :link-type: doc

      Learn how to open, close and interact with Lumerical products through sessions.

   .. grid-item-card:: Script commands as methods
      :link: script_commands_as_methods
      :link-type: doc

      Learn how to interact with Lumerical products using script commands.

   .. grid-item-card:: Working with simulation objects
      :link: working_with_simulation_objects
      :link-type: doc

      Learning how to create and manipulate simulation objects.

.. grid:: 2 2 2 2

   .. grid-item-card:: Passing data
      :link: passing_data
      :link-type: doc

      Learning how data types are transferred between Lumerical and Python.

   .. grid-item-card:: Accessing simulation results
      :link: accessing_simulation_results
      :link-type: doc

      Learn how to access simulation results and work with Lumerical datasets.

Photonic inverse design
------------------------

The guide below discusses usage of lumopt2 for inverse design of photonic devices.

.. grid:: 1 1 1 1

   .. grid-item-card:: Introduction to photonic inverse design with lumopt2
      :link: photonic_inverse_design_with_lumopt2
      :link-type: doc

      Learn how to use the lumopt2 module for photonic inverse design.

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Simulation Automation

   session_management
   script_commands_as_methods
   working_with_simulation_objects
   passing_data
   accessing_simulation_results

.. toctree::
   :hidden:
   :maxdepth: 3
   :caption: Introduction to photonic inverse design

   photonic_inverse_design_with_lumopt2
   Getting started example: Simple metalens <lumopt2/getting_started_simple_metalens>
   Getting started example: L-Bend <lumopt2/getting_started_l_bend>


.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Photonic inverse design usage guide

   lumopt2/optimization_session