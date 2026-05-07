Parametrization
===============

The parametrization module defines how the design geometry is represented and how
design parameters map to permittivity distributions. It supports shape optimization,
topology optimization, and closed-curve parametrizations.

.. autosummary::
    :toctree: _autosummary

    lumopt2.parametrization.base_parametrization.BaseParametrization
    lumopt2.parametrization.parametrization.Parametrization
    lumopt2.parametrization.topology.Topology
    lumopt2.parametrization.closed_curve.ClosedCurve
    lumopt2.parametrization.closed_curve.ClosedCurveSegment
    lumopt2.parametrization.closed_curve.ClosedCurveLinearSegment
    lumopt2.parametrization.closed_curve.ClosedCurveCubicSegment
    lumopt2.parametrization.closed_curve.ParamVertex
    lumopt2.parametrization.closed_curve.Segment
    lumopt2.parametrization.closed_curve.EqualSplit
    lumopt2.parametrization.closed_curve.Parametrize
    lumopt2.parametrization.d_eps_calculator.DEpsCalculator
