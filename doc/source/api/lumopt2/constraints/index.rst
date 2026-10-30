lumopt2.constraints
===================

The constraints module provides differentiable soft constraints and feasibility restoration for manufacturable designs.

.. automodule:: lumopt2.constraints
   :no-members:

.. grid:: 2 2 3 3

    .. grid-item-card:: constraints.base
        :link: base
        :link-type: doc

        Base class and evaluation container for constraints.

    .. grid-item-card:: constraints.aggregator
        :link: aggregator
        :link-type: doc

        Combine multiple constraints into one penalty.

    .. grid-item-card:: constraints.manufacturing
        :link: manufacturing
        :link-type: doc

        Minimum area, angle, distance, and edge length constraints.

.. grid:: 2 2 3 3

    .. grid-item-card:: constraints.restoration
        :link: restoration
        :link-type: doc

        Minimum-norm geometric correction onto the exact design rules.

.. toctree::
   :hidden:

   base
   aggregator
   manufacturing
   restoration
