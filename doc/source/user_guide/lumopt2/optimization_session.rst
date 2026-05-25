Setting up the optimization session
====================================

The optimization session is the main interface to run inverse design problems. It combines critical components include the base simulation, parametrization, figure of merit, and visualizer settings.

This article describes the overall optimization workflow in lumopt2 through the optimization session, and includes links to detailed guides for each of the component.

Overview
--------

The overall workflow for running an inverse design problem is shown in the diagram below, with subsequent subsections describing in further detail each of the components.

.. grid:: 1 1 12 12
   :gutter: 0
   :class-container: flow-hub-row

   .. grid-item::
      :columns: 12 12 2 2

      .. card:: Base simulation
         :link: #base-simulation
         :link-type: url

         ``.fsp``, ``.lsf``, ``.py``

      .. card:: Parametrization
         :link: #parametrization
         :link-type: url

         ``lumopt2.Parametrization`` ``lumopt2.ClosedCurve`` ``lumopt2.Topology``

      .. card:: Figure of merit
         :link: #figure-of-merit
         :link-type: url

         ``lumopt2.Fom``

      .. card:: FDTD Session
         :link: #fdtd-session
         :link-type: url

         ``lumopt2.FdtdSession``

      .. card:: Runner
         :link: #runner
         :link-type: url

         ``lumopt2.LocalRunner``

   .. grid-item::
      :columns: 12 12 1 1
      :class: flow-bracket-top

   .. grid-item::
      :columns: 12 12 3 3

      .. card:: Project
         :link: #project
         :link-type: url

         ``lumopt2.Project``

      .. card:: Optimizer
         :link: #optimizer
         :link-type: url

         ``lumopt2.ScipyOptimizer``

      .. card:: Callbacks
         :link: #callbacks
         :link-type: url

         ``lumopt2.GraphicalVisualizer``

      .. card:: Result configuration
         :link: #result-configuration
         :link-type: url

         ``Optimization.store_all_simulations`` ``Optimization.log_profiling_summary``

   .. grid-item::
      :columns: 12 12 1 1
      :class: flow-bracket-right

   .. grid-item::
      :columns: 12 12 2 2

      .. card:: Optimization
         :class-card: flow-card-static

         ``lumopt2.Optimization``

   .. grid-item::
      :columns: 12 12 1 1
      :class: flow-arrow-right

   .. grid-item::
      :columns: 12 12 2 2

      .. card:: Run & Results
         :class-card: flow-card-static

         ``Optimization.run()``

Project
--------

The project object, :py:class:`~lumopt2.project.Project`, defines the optimization problem by combining the following elements:
- Base simulation (``Project.setup``): the simulation file to run the optimization in.
- Parametrization (``Project.parametrization``): how geometric parameters are translated into parameters for optimization.
- Figure of merit (``Project.fom``): the objective function to evaluate for the optimization.
- FDTD session (``Project.fdtd_session``): a handler for the session running Ansys Lumerical FDTD™
- Runner (``Project.runner``): a handler to set up the computational resources for running the optimization.

Base simulation
~~~~~~~~~~~~~~~~

The base simulation file defines the FDTD project to optimize, including the necessary geometry, sources, and monitors.
You can set up the base simulation file using an existing ``.fsp`` project file, a ``.lsf`` Lumerical script file, or a Python function.

Further information, such as the requirements on simulation object, is in the base simulation article.

.. grid:: 1 1 3 3

   .. grid-item-card:: Base simulation
      :link: base_simulation
      :link-type: doc

      Setting up the FDTD simulation for optimization.

Parametrization
~~~~~~~~~~~~~~~~

The parametrization defines how geometric parameters in the simulation maps to optimization parameters in lumopt2.

The lumopt2 module currently supports three different types of parametrization strategies:
- Parametric optimization: maps arbitrary Lumerical object properties as parameters, created through :py:class:`lumopt2.parametrization.Parametrization`.
- Closed curve optimization: defines a closed curve using Bezier control points, typically used for photonic integrated circuit applications, created through :py:class:`lumopt2.parametrization.ClosedCurve`.
- Topology optimization: defines a design region and generates a free-form geometry based on index values and a binarization step, created through :py:class:`lumopt2.parametrization.Topology`.

Further information for each parametrization strategy is in the parametrization article.

.. grid:: 1 1 3 3

   .. grid-item-card:: Parametrization
      :link: parametrization
      :link-type: doc

      Parametric, closed curve, and topology parametrization.

Figure of merit
~~~~~~~~~~~~~~~~

The figure of merit defines the objective function that the optimization evaluates at each iteration.
You can define a figure of merit based on simulation results from specific simulation objects, using the :py:func:`lumopt2.fom.Fom` function.

lumopt2 supports field intensity results from `field region <https://optics.ansys.com/hc/en-us/articles/36967414684947-Field-Region-Simulation-object>`__ objects, and results from `port <https://optics.ansys.com/hc/en-us/articles/360034382554-Ports-FDTD-Simulation-Object>`__ objects.

For further information on setting up the figure of merit from simulation results, see the figure of merit article.

.. grid:: 1 1 3 3

   .. grid-item-card:: Figure of merit
      :link: figure_of_merit
      :link-type: doc

      Defining figure of merit from simulation results.


FDTD session
~~~~~~~~~~~~~

The FDTD session is a handler class that defines a connection to the Ansys Lumerical FDTD™ software.

The session created using :py:class:`lumopt2.core.FdtdSession`, and automatically handled by the lumopt2 module. You only need to configure whether to show the FDTD GUI during the optimization process.

The GUI window is disabled by default, you can define a session with the GUI enabled using the following code.

.. code:: python

   fdtd_session = lmpt.FdtdSession(show_fdtd_cad = True)

Runner
~~~~~~

The runner is responsible for managing the computational resources for running the optimization.

lumopt2 currently supports local runners for CPU and GPU optimization, defined through :py:class:`lumopt2.utils.runner.LocalRunner`.
This runner uses the first GPU or CPU resource set up in FDTD, depending on the definition.

To set up a local runner, use the following code.

.. code:: python

   runner_gpu = lmpt.LocalRunner(resource = 'GPU') # GPU Runner
   runner_cpu = lmpt.LocalRunner(resource = 'CPU') # CPU Runner

For further information on resource configuration and GPU simulation, please visit the following Knowledge Base pages.

.. grid:: 2 2 4 4

   .. grid-item-card:: Resource configuration
      :link: https://optics.ansys.com/hc/en-us/articles/360058790674-Resource-configuration-elements-and-controls
      :link-type: url

      Learn how to set up resources in Lumerical.

   .. grid-item-card:: GPU simulation
      :link: https://optics.ansys.com/hc/en-us/articles/17518942465811-Getting-started-with-running-FDTD-on-GPU
      :link-type: url

      Getting started with running FDTD simulations on GPU.

Optimizer
-----------

Callbacks
----------

Result configuration
---------------------