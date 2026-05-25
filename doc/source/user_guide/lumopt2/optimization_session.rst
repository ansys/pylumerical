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

The project object, :py:class:`~pylumerical.lumopt2.project.Project`, defines the optimization problem

Base simulation
~~~~~~~~~~~~~~~~

Parametrization
~~~~~~~~~~~~~~~~

Figure of merit
~~~~~~~~~~~~~~~~

FDTD Session
~~~~~~~~~~~~~

Runner
~~~~~~

Optimizer
-----------

Callbacks
----------

Result configuration
---------------------

Result output
---------------