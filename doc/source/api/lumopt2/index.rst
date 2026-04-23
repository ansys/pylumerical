LumOpt2
=======

LumOpt2 is a Python-driven inverse design framework for photonic devices. It uses adjoint-based optimization
with Ansys Lumerical FDTD to automate the design of photonic components by maximizing a user-defined figure of merit.

.. grid:: 2 2 3 3

    .. grid-item-card:: Core
        :link: core
        :link-type: doc

        Project configuration, FDTD session management, and optimization orchestration.

    .. grid-item-card:: Figure of merit
        :link: fom
        :link-type: doc

        Figure of merit definitions, simulation result containers, and the factory function to create FOMs.

    .. grid-item-card:: Optimizer
        :link: optimizer
        :link-type: doc

        Optimization algorithms, including the SciPy-based optimizer.

.. grid:: 2 2 3 3

    .. grid-item-card:: Parametrization
        :link: parametrization
        :link-type: doc

        Geometry parametrization methods for shape, topology, and closed-curve optimization.

    .. grid-item-card:: Utilities
        :link: utils
        :link-type: doc

        Helper functions and classes for logging, configuration, gradient validation, running jobs, and visualization.

.. toctree::
    :hidden:

    core
    fom
    optimizer
    parametrization
    utils
