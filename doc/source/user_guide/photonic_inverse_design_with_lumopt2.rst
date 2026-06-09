lumopt2 module for photonic inverse design
==========================================

Inverse design is a computational design approach in which the desired functionality of a component or system is specified first, and optimization algorithms are then used to determine the structure or parameters that best produce that response.
Unlike traditional design workflows, which rely on iteratively adjusting a limited set of parameters and evaluating candidate geometries, inverse design enables systematic exploration of much larger design spaces.
This makes it especially valuable for complex photonic designs, where brute-force parameter sweeps become increasingly costly and less effective as the number of parameters grows.

The Ansys Lumerical solution for photonic inverse design, lumopt2, is named after the Python module of the same name included in the Ansys Lumerical installation.
The ``lumopt2`` module provides a simple and intuitive Python interface for configuring and running inverse design optimizations with Ansys Lumerical FDTD.

In just a few steps, you can define an optimization session with your custom parametrization and figure of merit, run the optimization, and analyze the results.

Installation
-------------

The ``lumopt2`` module is included with the Ansys Lumerical products and requires an existing Ansys Lumerical installation.

Using PyLumerical
~~~~~~~~~~~~~~~~~

PyLumerical is set up such that if there it detects a Lumerical installation with the module, you can directly import ``lumopt2``.

To use ``lumopt2``, first create a Python virtual environment and install PyLumerical.

.. tab-set::

   .. tab-item:: Linux

      .. code-block:: bash

         python -m venv .venv
         source .venv/bin/activate
         python -m pip install -U pip
         python -m pip install ansys-lumerical-core

   .. tab-item:: Windows Command Prompt

      .. code-block:: bash

         python -m venv .venv
         .venv\\Scripts\\activate.bat
         python -m pip install -U pip
         python -m pip install ansys-lumerical-core


   .. tab-item:: Windows Powershell

      .. code-block:: bash

         python -m venv .venv
         .venv\\Scripts\\Activate.ps1
         python -m pip install -U pip
         python -m pip install ansys-lumerical-core

Then, import the lumopt2 module and it is ready to use.

.. code-block:: python

   import ansys.lumerical.core.lumopt2 as lmpt

.. warning::
   Manual ``sys.path`` overrides for ``lumopt2`` are unsupported. The ``lumopt2`` module bundled with Ansys Lumerical products silently takes precedence over those added to ``sys.path``.

.. tip::
   To ensure that the correct bundled modules are imported, import ``ansys.lumerical.core`` before importing ``lumapi`` or ``lumopt2``.

Using the in-product script editor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also use ``lumopt2`` in Python scripts run from the Script Editor in Lumerical products. Import the module with a single line:

.. code-block:: python

   import lumopt2 as lmpt

.. note::

   The import syntax between PyLumerical and the in-product script editor slightly differs, as the in-product script editor uses a bundled Python environment.

Getting started
----------------

Follow the example below to quick get started with basic functionalities of lumopt2.

.. grid:: 2 2 3 3

    .. grid-item-card:: 3x3 array of pillars
        :link: lumopt2/getting_started_simple_metalens
        :link-type: doc

        Learn the basics of lumopt2 through a simple example of a metalens optimization.

Follow these examples for more in-depth introductions catered to specific workflows.

.. grid:: 2 2 3 3

    .. grid-item-card:: L-Bend
        :link: lumopt2/getting_started_l_bend
        :link-type: doc

        Learn how to optimize components for integrated photonic circuits through a simple L-bend example.


Usage guide
-----------

The diagram below illustrates the general workflow for using lumopt2. For further information, click on the corresponding card.

.. grid:: 5 5 5 5
   :gutter: 0
   :class-container: flow-hub-row

   .. grid-item::
      :columns: 12 12 5 5

      .. card:: Optimization session
         :link: lumopt2/optimization_session
         :link-type: doc

         Configure your optimization using your project definition, along with additional optimizer and callback settings.

   .. grid-item::
      :columns: 12 12 1 1
      :class: flow-chevron-right

   .. grid-item::
      :columns: 12 12 2 2

      .. card:: Run optimization
         :link: optimization-session-run
         :link-type: ref

   .. grid-item::
      :columns: 12 12 1 1
      :class: flow-chevron-right

   .. grid-item::
      :columns: 12 12 3 3

      .. card:: Optimization results
         :link: optimization-session-results
         :link-type: ref

.. grid:: 1 1 2 2
   :gutter: 0

   .. grid-item::
      :columns: 12 12 5 5
      :class: flow-chevron-up

.. card:: Project
   :class-card: flow-box

   .. grid:: 2 2 3 3
      :gutter: 5

      .. grid-item-card:: Base simulation
         :link: lumopt2/base_simulation
         :link-type: doc

         Define the base FDTD simulation for optimization.

      .. grid-item-card:: Parametrization
         :link: lumopt2/parametrization
         :link-type: doc

         Define the map between optimization and structure parameters.

      .. grid-item-card:: Figure of merit
         :link: lumopt2/figure_of_merit
         :link-type: doc

         Define the objective function based on specific simulation results.

.. toctree::
   :hidden:
   :maxdepth: 3

   Getting started example: Simple metalens <lumopt2/getting_started_simple_metalens>
   Getting started example: L-Bend <lumopt2/getting_started_l_bend>

.. toctree::
   :hidden:
   :maxdepth: 3

   lumopt2/optimization_session

..



