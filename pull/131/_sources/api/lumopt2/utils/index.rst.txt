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

.. toctree::
   :hidden:

   file_logger
   graphical_visualizer
   callbacks
   panels
   common
   config_map
   sparse_helpers
   runner
   fd_grad
   profiler
