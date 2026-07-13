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

.. rubric:: Step 1 - Import and simulation parameters

Import PyLumerical and define various simulation parameters.

.. dropdown:: Show parameter definition
   :icon: gear
   :chevron: right-down

   .. literalinclude:: ../_static/simulation_examples/getting_started_nanoholes/getting_started_nanoholes.py
      :language: python
      :start-after: # --- Parameters ---
      :end-before: # --- Parameters end ---


.. rubric:: Step 2 - Build simulation

Set up the simulation, including the region, geometry, materials, source, and monitors.

.. dropdown:: Show simulation setup
   :icon: tools
   :chevron: right-down
   :open:

   .. literalinclude:: ../_static/simulation_examples/getting_started_nanoholes/getting_started_nanoholes.py
      :language: python
      :start-after: # --- Simulation setup ---
      :end-before: # --- Simulation setup end --

.. rubric:: Step 3 - Run and plot results

Run the simulation and plot the transmission and reflection spectra.

.. dropdown:: Show simulation run and plotting
   :icon: graph
   :chevron: right-down

   .. literalinclude:: ../_static/simulation_examples/getting_started_nanoholes/getting_started_nanoholes.py
      :language: python
      :start-after: # --- Run ---
      :end-before: # --- Run end --

The figure below shows the transmission and reflection spectrum of the array.

.. image:: ../_static/simulation_examples/getting_started_nanoholes/final_result.png
   :alt: Transmission spectrum
   :align: center


.. rubric:: Full script

.. dropdown:: Show full script for copy and paste
   :icon: download
   :chevron: right-down

   .. literalinclude:: ../_static/simulation_examples/getting_started_nanoholes/getting_started_nanoholes.py
      :language: python


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
