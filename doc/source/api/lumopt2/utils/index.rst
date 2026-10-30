lumopt2.utils
=============

The utilities module provides helper functions for visualization, logging, and other auxiliary optimization utilities.

Visualization and Logging
--------------------------

These classes provide utilities via a callback system to log or visualize results.

.. grid:: 2 2 3 3

    .. grid-item-card:: utils.file_logger
        :link: file_logger
        :link-type: doc

        Plain-text and JSON result logger callbacks.

    .. grid-item-card:: utils.graphical_visualizer
        :link: graphical_visualizer
        :link-type: doc

        Matplotlib visualization callback.

    .. grid-item-card:: utils.callbacks
        :link: callbacks
        :link-type: doc

        Optimization callback base class and list.

.. grid:: 2 2 3 3

    .. grid-item-card:: utils.panels
        :link: panels
        :link-type: doc

        Reusable panel widgets for the visualizer.

    .. grid-item-card:: utils.shape_gradient_plot
        :link: shape_gradient_plot
        :link-type: doc

        Plot shape gradients on polygon boundaries.

    .. grid-item-card:: utils.logging_config
        :link: logging_config
        :link-type: doc

        Detailed console and file logging configuration.

.. grid:: 2 2 3 3

    .. grid-item-card:: utils.emit_logging
        :link: emit_logging
        :link-type: doc

        Machine-readable EMIT log level and data URI helpers.

Optimization utilities
--------------------------

These classes provide auxiliary utilities for optimization such as job management, profiling, and configurations.

.. grid:: 2 2 3 3

    .. grid-item-card:: utils.common
        :link: common
        :link-type: doc

        Common utility classes and functions.

    .. grid-item-card:: utils.config_map
        :link: config_map
        :link-type: doc

        Simulation result configuration mapping.

    .. grid-item-card:: utils.sparse_helpers
        :link: sparse_helpers
        :link-type: doc

        Sparse-dense index conversion functions.

.. grid:: 2 2 3 3

    .. grid-item-card:: utils.runner
        :link: runner
        :link-type: doc

        Job management infrastructure.

    .. grid-item-card:: utils.fd_grad
        :link: fd_grad
        :link-type: doc

        Finite difference gradient utilities.

    .. grid-item-card:: utils.profiler
        :link: profiler
        :link-type: doc

        Wall-clock profiling for optimization phases.

.. grid:: 2 2 3 3

    .. grid-item-card:: utils.slurm_config
        :link: slurm_config
        :link-type: doc

        Slurm cluster configuration and resource resolution.

    .. grid-item-card:: utils.pure_func_checker
        :link: pure_func_checker
        :link-type: doc

        Static analysis helpers for validating pure, picklable functions.

.. grid:: 2 2 3 3

    .. grid-item-card:: utils.gds_import
        :link: gds_import
        :link-type: doc

        Import polygons from GDS files.

    .. grid-item-card:: utils.burst_serdes
        :link: burst_serdes
        :link-type: doc

        Serialize an optimization script to run on a burst resource.

    .. grid-item-card:: utils.resource_estimator
        :link: resource_estimator
        :link-type: doc

        Estimate thread, memory, and concurrency needs for dEps/dP jobs.

.. toctree::
   :hidden:

   file_logger
   graphical_visualizer
   callbacks
   panels
   shape_gradient_plot
   logging_config
   emit_logging
   common
   config_map
   sparse_helpers
   runner
   fd_grad
   profiler
   slurm_config
   pure_func_checker
   custom_serializers
   gds_import
   burst_serdes
   resource_estimator
