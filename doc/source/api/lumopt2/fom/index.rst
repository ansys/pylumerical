Figure of Merit
===============

The figure of merit (FOM) module defines the objective functions used during optimization. It provides
simulation result containers, concrete FOM classes, and a factory function to create the appropriate
FOM type from simulation results.

.. automodule:: lumopt2.fom
   :no-members:

.. grid:: 2 2 3 3

    .. grid-item-card:: fom.fom
        :link: fom
        :link-type: doc

        Factory function to create the appropriate FOM subclass.

    .. grid-item-card:: fom.base_fom
        :link: base_fom
        :link-type: doc

        Base class providing shared FOM infrastructure.

    .. grid-item-card:: fom.field_fom
        :link: field_fom
        :link-type: doc

        FOM calculator for field-based (DFT monitor) simulations.

    .. grid-item-card:: fom.port_fom
        :link: port_fom
        :link-type: doc

        FOM calculator for port-based (waveguide mode) simulations.

    .. grid-item-card:: fom.simulation_results
        :link: simulation_results
        :link-type: doc

        Containers for simulation results from field and port monitors.

.. toctree::
   :hidden:

   fom
   base_fom
   field_fom
   port_fom
   simulation_results
