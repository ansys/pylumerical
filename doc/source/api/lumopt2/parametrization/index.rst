lumopt2.parametrization
=======================

The parametrization module contains classes and functions that defines how geometry is represented and modified during optimization.

.. grid:: 2 2 3 3

    .. grid-item-card:: parametrization.parametrization
        :link: parametrization
        :link-type: doc

        Parametrization based on arbitrary pre-existing Lumerical object properties.

    .. grid-item-card:: parametrization.topology
        :link: topology
        :link-type: doc

        Parametrization based on topology optimization with refractive index density pixels.

    .. grid-item-card:: parametrization.closed_curve
        :link: closed_curve
        :link-type: doc

        Parametrization based on moving vertices for a closed curve.

.. grid:: 2 2 3 3

    .. grid-item-card:: parametrization.combined_parametrization
        :link: combined_parametrization
        :link-type: doc

        Combine multiple parametrizations into one.

    .. grid-item-card:: parametrization.base_parametrization
        :link: base_parametrization
        :link-type: doc

        Abstract base class for all parametrization types.

    .. grid-item-card:: parametrization.d_eps_calculator
        :link: d_eps_calculator
        :link-type: doc

        Sparse dEps/dP Jacobian calculator in FDTD.

.. toctree::
   :hidden:

   parametrization
   topology
   closed_curve
   combined_parametrization
   base_parametrization
   d_eps_calculator
