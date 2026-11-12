lumopt2
=======

The Lumerical photonic inverse design module lumopt2 provides a framework for the inverse design of photonic devices using Ansys Lumerical FDTD™. The following pages contains API documentation for the lumopt2 module.

.. note::

    lumopt2 is only available in Ansys Lumerical FDTD™ version 2026 R1.2 and later.

Common lumopt2 API
------------------

These classes are commonly used in the lumopt2 workflow, and you can directly initialize them from the top-level lumopt2 module.

.. tab-set::

   .. tab-item:: Optimization project

      Classes and functions for setting up the optimization project.

      .. rubric:: Classes

      .. autosummary::
         :nosignatures:

         ~lumopt2.core.optimization.Optimization
         ~lumopt2.core.optimization.OptimizationResult
         ~lumopt2.core.project.Project
         ~lumopt2.core.project_config.ProjectConfig
         ~lumopt2.core.fdtd_session.FdtdSession
         ~lumopt2.core.fdtd_session.SimulationStatus
         ~lumopt2.core.fdtd_session.SimulationError

   .. tab-item:: Results and FoM

      Classes and functions for handling simulation results and figures of merit.

      .. rubric:: Classes

      .. autosummary::
         :nosignatures:

         ~lumopt2.fom.simulation_results.PortResults
         ~lumopt2.fom.simulation_results.FieldResults
         ~lumopt2.fom.simulation_results.FarfieldResults
         ~lumopt2.fom.farfield_fom.FarfieldFom

      .. rubric:: Functions

      .. autosummary::
         :nosignatures:

         ~lumopt2.fom.fom.Fom
         ~lumopt2.utils.common.PNorm
         ~lumopt2.utils.common.BoundedMatch

   .. tab-item:: Parametrization

      Classes and functions for parametrizing the simulation geometry.

      .. rubric:: Classes

      .. autosummary::
         :nosignatures:

         ~lumopt2.parametrization.parametrization.Parametrization
         ~lumopt2.parametrization.closed_curve.ClosedCurve
         ~lumopt2.parametrization.closed_curve.ClosedCurveLinearSegment
         ~lumopt2.parametrization.closed_curve.ClosedCurveCubicSegment
         ~lumopt2.parametrization.layout_shape.LayoutShape
         ~lumopt2.parametrization.polygon.Polygon
         ~lumopt2.parametrization.combined_parametrization.CombinedParametrization
         ~lumopt2.parametrization.closed_curve.Segment
         ~lumopt2.parametrization.closed_curve.EqualSplit
         ~lumopt2.parametrization.closed_curve.Parametrize
         ~lumopt2.parametrization.closed_curve.ParamVertex
         ~lumopt2.utils.common.Box

   .. tab-item:: Optimizers

      Classes and functions for setting tools to calculate the gradient.

      .. rubric:: Classes

      .. autosummary::
         :nosignatures:

         ~lumopt2.optimizer.scipy_optimizer.ScipyOptimizer
         ~lumopt2.optimizer.gradient_ascent.GradientAscentOptimizer
         ~lumopt2.optimizer.base_optimizer.ParameterScaler

      .. rubric:: Functions

      .. autosummary::
         :nosignatures:

         ~lumopt2.optimizer.base_optimizer.validate_bounds
         ~lumopt2.optimizer.base_optimizer.extract_fom
         ~lumopt2.optimizer.base_optimizer.extract_fom_and_gradient
         ~lumopt2.utils.fd_grad.finite_difference_gradient
         ~lumopt2.utils.fd_grad.validate_gradient
         ~lumopt2.utils.fd_grad.fd_sweep_perturbation
         ~lumopt2.utils.fd_grad.visualize_d_eps

   .. tab-item:: Resources

      Classes and functions for managing computational resources to run optimization.

      .. rubric:: Classes

      .. autosummary::
         :nosignatures:

         ~lumopt2.utils.runner.LocalRunner
         ~lumopt2.utils.runner.SlurmRunner
         ~lumopt2.utils.runner.Job
         ~lumopt2.utils.slurm_config.SlurmConfig

      .. rubric:: Functions

      .. autosummary::
         :nosignatures:

         ~lumopt2.utils.burst_serdes.run_on_burst

   .. tab-item:: Visualization

      Classes and functions for visualizing optimization results.

      .. rubric:: Classes

      .. autosummary::
         :nosignatures:

         ~lumopt2.utils.callbacks.BaseCallback
         ~lumopt2.utils.callbacks.CallbackList
         ~lumopt2.utils.file_logger.FileLogger
         ~lumopt2.utils.graphical_visualizer.GraphicalVisualizer
         ~lumopt2.utils.panels.Panel
         ~lumopt2.utils.panels.PanelState
         ~lumopt2.utils.panels.FomPanel
         ~lumopt2.utils.panels.GeometryPanel
         ~lumopt2.utils.panels.GradientNormPanel
         ~lumopt2.utils.panels.MonitorPanel
         ~lumopt2.utils.panels.ConstraintViolationPanel
         ~lumopt2.utils.panels.ManufacturingMetricsPanel
         ~lumopt2.utils.panels.ShapeGradientPanel
         ~lumopt2.utils.callbacks.ManufacturingMetricsLogger
         ~lumopt2.utils.callbacks.ConstraintLogger

      .. rubric:: Functions

      .. autosummary::
         :nosignatures:

         ~lumopt2.utils.shape_gradient_plot.plot_shape_gradient

   .. tab-item:: Shape optimization

      Classes and functions for shape optimization of layout polygons with manufacturing constraints.

      .. rubric:: Classes

      .. autosummary::
         :nosignatures:

         ~lumopt2.shape_optimization.Transmission
         ~lumopt2.shape_optimization.DesignRules
         ~lumopt2.constraints.base.BaseConstraint
         ~lumopt2.constraints.manufacturing.MinAreaConstraint
         ~lumopt2.constraints.manufacturing.MinAngleConstraint
         ~lumopt2.constraints.manufacturing.MinDistanceConstraint
         ~lumopt2.constraints.manufacturing.MinEdgeLengthConstraint

      .. rubric:: Functions

      .. autosummary::
         :nosignatures:

         ~lumopt2.shape_optimization.optimize_shape

   .. tab-item:: Other

      Classes and functions for logging, profiling, and other utilities.

      .. rubric:: Classes

      .. autosummary::
         :nosignatures:

         ~lumopt2.utils.profiler.Profiler
         ~lumopt2.utils.logging_config.DetailedLogging

      .. rubric:: Functions

      .. autosummary::
         :nosignatures:

         ~lumopt2.setup_default_logging

All lumopt2 modules
-------------------

.. grid:: 2 2 3 3

    .. grid-item-card:: lumopt2.core
        :link: core/index
        :link-type: doc

        Modules for project configuration, optimization configuration, and FDTD session management.

    .. grid-item-card:: lumopt2.fom
        :link: fom/index
        :link-type: doc

        Modules to capture simulation results and define figures of merit from them for optimization.

    .. grid-item-card:: lumopt2.parametrization
        :link: parametrization/index
        :link-type: doc

        Modules to parametrize the simulation.

.. grid:: 2 2 3 3

    .. grid-item-card:: lumopt2.constraints
        :link: constraints/index
        :link-type: doc

        Modules for design rules.

.. grid:: 2 2 3 3

    .. grid-item-card:: lumopt2.gradient
        :link: gradient/index
        :link-type: doc

        Modules to form gradients from simulation fields.

    .. grid-item-card:: lumopt2.shape_optimization
        :link: shape_optimization
        :link-type: doc

        High-level workflow for shape optimization.

.. grid:: 2 2 3 3

    .. grid-item-card:: lumopt2.optimizer
        :link: optimizer/index
        :link-type: doc

        Modules to set up and perform the optimization algorithm.

    .. grid-item-card:: lumopt2.utils
        :link: utils/index
        :link-type: doc

        Utility modules.

.. toctree::
    :hidden:

    core/index
    fom/index
    optimizer/index
    parametrization/index
    constraints/index
    gradient/index
    shape_optimization
    utils/index

..