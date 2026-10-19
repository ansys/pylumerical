lumopt2.fom
===========

The figure of merit module defines the objective functions for optimization.

.. automodule:: lumopt2.fom
   :no-members:

.. grid:: 2 2 3 3

    .. grid-item-card:: fom.fom
        :link: fom
        :link-type: doc

        Factory function to create the correct FoM subclass based on the simulation result.

    .. grid-item-card:: fom.field_fom
        :link: field_fom
        :link-type: doc

        FoM calculator for field region results.

    .. grid-item-card:: fom.port_fom
        :link: port_fom
        :link-type: doc

        FoM calculator for port results.

.. grid:: 2 2 3 3

    .. grid-item-card:: fom.base_fom
        :link: base_fom
        :link-type: doc

        Base class providing shared FoM infrastructure.

    .. grid-item-card:: fom.simulation_results
        :link: simulation_results
        :link-type: doc

        Containers for simulation results from field region and ports.

.. toctree::
   :hidden:

   fom
   field_fom
   port_fom
   base_fom
   simulation_results
