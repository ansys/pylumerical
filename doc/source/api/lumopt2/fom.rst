Figure of merit
===============

The figure of merit (FOM) module defines the objective functions used during optimization. It provides
simulation result containers, base and concrete FOM classes, and a factory function to create the
appropriate FOM type from simulation results.

.. autosummary::
    :toctree: _autosummary

    lumopt2.fom.fom.Fom
    lumopt2.fom.base_fom.BaseFom
    lumopt2.fom.field_fom.FieldFom
    lumopt2.fom.port_fom.PortFom
    lumopt2.fom.simulation_results.BaseResults
    lumopt2.fom.simulation_results.FieldResults
    lumopt2.fom.simulation_results.PortResults
