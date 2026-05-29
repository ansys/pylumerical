lumopt2 Lumerical photonic inverse design module introduction
==============================================================

As photonic components become increasingly complex, traditional design cycles involving manually varying a small set of parameters become less effective in finding the optimal device design. While parameter sweeps and traditional optimization techniques allows for further exploration of the design space, the time required exponentially increases as the number of design parameters increase. Towards that end, specialized methods are required to anticipate strong candidates which allows for faster convergence towards a satisfactory design.

The Lumerical photonic inverse design module is a Python module included within Lumerical FDTD is built for efficient optimization of photonic components. Leveraging the adjoint method, you can calculate the gradient with respect to all parameters with only two FDTD simulations, enabling you to quickly adjust your design to achieve specified figures of merit.

With only simple Python scripting, you can set up an optimization session based on an FDTD simulation, map simulation parameters to optimization parameters, and run the inverse design with a variety of resources.

Installation
-------------

Using with PyLumerical
~~~~~~~~~~~~~~~~~~~~~~

lumopt2 is provided as a part of the Lumerical FDTD installation. Therefore, you must have Lumerical FDTD installed to use lumopt2.
PyLumerical is set up such that if there it detects a Lumerical installation with the module, you can directly import lumopt2.

To use lumopt2, first create a Python virtual environment and install PyLumerical.

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
   Manual ``sys.path`` overrides for ``lumopt2`` are unsupported.

.. tip::
   For consistent module binding, import ``ansys.lumerical.core`` before importing ``lumapi`` or ``lumopt2`` directly.

Using with the in-product script editor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also use lumopt2 directly with the script editor in Lumerical products.

To do so, simply open any Python script from the editor, and import the module directly and run the script.

.. code-block:: python

   import lumopt2 as lmpt

.. note::

   The import syntax between PyLumerical and the in-product script editor slightly differs, as the in-product script editor uses a bundled Python environment.

Getting started
----------------

Follow the example below to quick get started with basic functionalities of lumopt2.

.. grid:: 2 2 3 3

    .. grid-item-card:: 3x3 array of pillars
        :link: lumopt2/getting_started_3x3_pillar
        :link-type: doc

        Learn the basics of lumopt2 through a simple example for optimizing a 3x3 array of pillars.

Follow these examples for more in-depth introductions catered to specific workflows.

.. grid:: 2 2 3 3

    .. grid-item-card:: L-Bend
        :link: lumopt2/getting_started_l_bend
        :link-type: doc

        Learn about the workflow for photonic integrated circuits through an L-bend example.


Usage guide
-----------

The diagram below illustrates the general workflow for using lumopt2. For further information on the critical components, click on the corresponding card.

.. grid:: 5 5 5 5
   :gutter: 0
   :class-container: flow-hub-row

   .. grid-item::
      :columns: 12 12 5 5

      .. card:: Optimization session
         :link: lumopt2/optimization_session
         :link-type: doc

         Combining components into a Project and Optimization workflow — optimizer, runner, and execution configuration.

   .. grid-item::
      :columns: 12 12 1 1
      :class: flow-chevron-right

   .. grid-item::
      :columns: 12 12 2 2

      .. card:: Run optimization
         :class-card: flow-card-static

         ``Optimization.run()``

   .. grid-item::
      :columns: 12 12 1 1
      :class: flow-chevron-right

   .. grid-item::
      :columns: 12 12 3 3

      .. card:: Optimization results
         :class-card: flow-card-static

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

         Setting up the FDTD simulation for optimization.

      .. grid-item-card:: Parametrization
         :link: lumopt2/parametrization
         :link-type: doc

         Parametric and closed curve approaches.

      .. grid-item-card:: Figure of merit
         :link: lumopt2/figure_of_merit
         :link-type: doc

         Defining simulation results and objective functions.

.. toctree::
   :hidden:
   :maxdepth: 2

   lumopt2/getting_started_3x3_pillar
   lumopt2/getting_started_l_bend
   lumopt2/optimization_session
   lumopt2/base_simulation
   lumopt2/parametrization
   lumopt2/figure_of_merit
   lumopt2/callbacks




