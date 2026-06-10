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

The article below discusses usage of lumopt2 for inverse design of photonic devices, along with a few getting started examples.

.. grid:: 1 1 1 1

   .. grid-item-card:: Introduction to photonic inverse design with lumopt2
      :link: photonic_inverse_design_with_lumopt2
      :link-type: doc

      Learn how to install and use the lumopt2 module for photonic inverse design.

.. grid:: 1 2 2 2

   .. grid-item-card:: Getting started with lumopt2: Simple metalens example
      :link: lumopt2/getting_started_simple_metalens
      :link-type: doc

      Get a quick introduction to using lumopt2 through a simple metalens optimization example.

   .. grid-item-card:: Getting started with lumopt2: L-bend example
      :link: lumopt2/getting_started_l_bend
      :link-type: doc

      Learn how to optimize components for integrated photonic circuits through a simple L-bend example.

Start with the article below to learn the details of ``lumopt2``.

.. grid:: 1 1 1 1

   .. grid-item-card:: Optimization session
      :link: lumopt2/optimization_session
      :link-type: doc

      Learn about the optimization session, which is the core of the photonic inverse design workflow with ``lumopt2``.

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
   :caption: Photonic inverse design

   photonic_inverse_design_with_lumopt2
   Getting started: Simple metalens example <lumopt2/getting_started_simple_metalens>
   Getting started: L-Bend example <lumopt2/getting_started_l_bend>
   lumopt2/optimization_session
