Optimization session
====================

The optimization session is the main interface for setting up and running a ``lumopt2`` optimization.
Its key input is the optimization :py:class:`~lumopt2.core.project.Project`, which defines the base simulation, parameterization, and figure of merit. You can also use the session inputs to choose the optimizer and specify what data is reported during and after the optimization.

This article describes the overall optimization workflow in ``lumopt2`` through the optimization session, and includes links to detailed guides for each of the component.

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

         ``lumopt2.Parametrization`` ``lumopt2.ClosedCurve``

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

         ``lumopt2.GraphicalVisualizer`` ``lumopt2.FileLogger``

      .. card:: Additional configurations
         :link: #additional-configurations
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
         :link: #running-the-optimization
         :link-type: url

         ``Optimization.run()``

Project
--------

The project object, :py:class:`~lumopt2.core.project.Project`, defines the optimization problem by combining the following elements:

- **Base simulation** (``Project.setup``): configures the simulation objects, such as sources and monitors, required to run the FDTD simulations.
- **Parametrization** (``Project.parametrization``): defines the optimization parameters in terms of how they modify the simulated structure.
- **Figure of merit** (``Project.fom``): defines the objective function to evaluate for the optimization.
- **FDTD session** (``Project.fdtd_session``): manages the session running FDTD simulations.
- **Runner** (``Project.runner``): sets up the computational resources for running the optimization.

Base simulation
~~~~~~~~~~~~~~~~

The base simulation file defines the FDTD project to optimize, including the necessary geometry, sources, and monitors.
You can set up the base simulation file using an existing ``.fsp`` project file, a ``.lsf`` Lumerical script file, or a Python function.

Further information, such as the requirements on simulation object, is in the base simulation article.

.. grid:: 1 1 4 4

    .. grid-item::

        .. card:: :octicon:`book` User guide - base simulation
            :link: base_simulation
            :link-type: doc

Parametrization
~~~~~~~~~~~~~~~~

The parametrization defines how geometric parameters in the simulation maps to optimization parameters in lumopt2.

The lumopt2 module currently supports two different types of parametrization strategies:

- Parametric optimization (:py:class:`~lumopt2.parametrization.parametrization.Parametrization`): maps arbitrary Lumerical object properties as parameters.
- Closed curve optimization (:py:class:`~lumopt2.parametrization.closed_curve.ClosedCurve`): defines a closed curve formed by linear and cubic segments, typically used for photonic integrated circuit applications..

Further information for each parametrization strategy is in the parametrization article.

.. grid:: 1 1 4 4

    .. grid-item::

        .. card:: :octicon:`book` User guide - parametrization
            :link: parametrization
            :link-type: doc

Figure of merit
~~~~~~~~~~~~~~~~

The figure of merit defines the objective function that the optimization evaluates at each iteration.
You can define a figure of merit based on simulation results from specific simulation objects, using the :py:func:`~lumopt2.fom.fom.Fom` function.
lumopt2 supports field intensity results from `field region <https://optics.ansys.com/hc/en-us/articles/36967414684947-Field-Region-Simulation-object>`__ objects, and results from `port <https://optics.ansys.com/hc/en-us/articles/360034382554-Ports-FDTD-Simulation-Object>`__ objects.

For further information on setting up the figure of merit from simulation results, see the figure of merit article.

.. grid:: 1 1 4 4

    .. grid-item::

        .. card:: :octicon:`book` User guide - figure of merit
            :link: figure_of_merit
            :link-type: doc


FDTD session
~~~~~~~~~~~~~

The FDTD session is a handler class that defines a connection to the Ansys Lumerical FDTD™ software.

The session created using :py:class:`~lumopt2.core.fdtd_session.FdtdSession` is automatically handled by the lumopt2 module.
The GUI window is disabled by default, you can define a session with the GUI enabled using the following code.

.. code:: python

   fdtd_session = lmpt.FdtdSession(show_fdtd_cad = True)

Runner
~~~~~~

The runner is responsible for managing the computational resources for running the optimization.

lumopt2 currently supports local runners for CPU and GPU optimization, defined through :py:class:`~lumopt2.utils.runner.LocalRunner`.
The runner uses the first GPU or CPU resource enabled in the FDTD resource manager list, depending on the specified type.

To set up a local runner, use the following code.

.. code:: python

   runner_gpu = lmpt.LocalRunner(resource = 'GPU') # GPU Runner
   runner_cpu = lmpt.LocalRunner(resource = 'CPU') # CPU Runner

For further information on resource configuration and GPU simulation, please visit the following Knowledge Base pages.

.. grid:: 1 1 4 4

    .. grid-item::

        .. card:: :octicon:`book` Lumerical KB - resource configuration
            :link: https://optics.ansys.com/hc/en-us/articles/360058790674-Resource-configuration-elements-and-controls
            :link-type: url

    .. grid-item::

        .. card:: :octicon:`book` Lumerical KB - GPU simulation
            :link: https://optics.ansys.com/hc/en-us/articles/17518942465811-Getting-started-with-running-FDTD-on-GPU
            :link-type: url

Optimizer
-----------

The optimizer defines the optimization algorithm for solving the inverse design problem.

In lumopt2, you can define an optimizer using the built-in :py:class:`~lumopt2.optimizer.scipy_optimizer` class.

You can use the following code to set up a basic optimizer with default settings.

.. code:: python

   optimizer = lmpt.ScipyOptimizer()

By default, the optimizer uses the gradient-based L-BFGS-B method. This method is well-suited for inverse design because of its excellent memory efficiency for high-dimensional problems, ability to naturally handle bounds, efficient usage of gradient information, and quick convergence for smooth objective functions.

In addition to the default, you can also choose from any of the optimization algorithm available in the `scipy.optimize.minimize` function. For any gradient-free methods, ``lumopt2`` automatically skips the adjoint simulation step.

.. tip::

   Certain optimizer parameters, such as ``ftol``, ``gtol``, and ``max_fval``, are exposed directly in the :py:class:`~lumopt2.optimizer.scipy_optimizer` class, which are passed onto the underlying optimizer if they are applicable.
   You can additional options ont in the default argument list using the ``options`` argument.

Callbacks
----------

Callbacks are functions that are executed at specific points during the optimization process. You can use callbacks for logging and visualization during the optimization.

``lumopt2`` includes a built-in graphical visualizer class, :py:class:`~lumopt2.utils.graphical_visualizer.GraphicalVisualizer`, which you can further customize with panels to plot results from specific monitors.

You can also set up logging using classes including :py:class:`~lumopt2.utils.file_logger.FileLogger`.

For further information on configuring callbacks and on when they are triggered, see the callbacks article.

.. grid:: 1 1 4 4

    .. grid-item::

        .. card:: :octicon:`book` User guide - callbacks
            :link: callbacks
            :link-type: doc

Additional configurations
-------------------------

There are two additional useful flags in the :py:class:`~lumopt2.core.optimization.Optimization` class configuration:

- ``Optimization.store_all_simulations``: stores all simulations on disk
- ``Optimization.log_profiling_summary``: toggles whether wall-clock profiling is a part of the standard log

.. _optimization-session-run:

Running the optimization
------------------------

After configuring the optimization session, run the optimization using

.. code:: python

   Optimization.run()

.. _optimization-session-results:

Optimization results
--------------------

The :py:class:`Optimization.run() <lumopt2.core.optimization.Optimization>` method returns a tuple, where the first element is the best optimization parameter set, and the second element is the best figure of merit value.

You can export the optimization results in your preferred method, or recreate an FDTD project file using the optimal parameters with the :py:class:`Project.save_project() <lumopt2.core.project.Project>` method for further processing and export for fabrication.

.. code-block:: python

   best_params, best_fom = result
   project.save_project("L_bend_optimization_final.fsp",params=best_params)

.. tip::

    See the Lumerical Knowledge Base article `Importing and exporting GDSII files <https://optics.ansys.com/hc/en-us/articles/1500006203341>`_ for more information on exporting a GDS file from the final project.

..

.. toctree::
   :hidden:
   :maxdepth: 2

   Project: Base simulation <base_simulation>
   Project: Parametrization <parametrization>
   Project: Figure of merit <figure_of_merit>
   Callbacks <callbacks>