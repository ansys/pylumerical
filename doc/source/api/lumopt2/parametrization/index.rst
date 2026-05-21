lumopt2.parametrization
=======================

The parametrization module defines how it represents the design geometry and how
design parameters map to permittivity distributions. It supports shape, topology,
and closed-curve optimization.

.. grid:: 2 2 3 3

    .. grid-item-card:: parametrization.base_parametrization
        :link: base_parametrization
        :link-type: doc

        Abstract base class for all parametrization types.

    .. grid-item-card:: parametrization.parametrization
        :link: parametrization
        :link-type: doc

        Flexible function-based parametrization.

    .. grid-item-card:: parametrization.topology
        :link: topology
        :link-type: doc

        Density-based topology optimization.

.. grid:: 2 2 3 3

    .. grid-item-card:: parametrization.closed_curve
        :link: closed_curve
        :link-type: doc

        Piecewise curve-based geometry boundaries.

    .. grid-item-card:: parametrization.combined_parametrization
        :link: combined_parametrization
        :link-type: doc

        Combine multiple parametrizations into one.

    .. grid-item-card:: parametrization.d_eps_calculator
        :link: d_eps_calculator
        :link-type: doc

        Sparse dEps/dP Jacobian computation.

.. toctree::
   :hidden:

   base_parametrization
   parametrization
   topology
   closed_curve
   combined_parametrization
   d_eps_calculator
