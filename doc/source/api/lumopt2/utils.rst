Utilities
=========

The utilities module provides helper functions and classes for logging, configuration mapping,
finite-difference gradient validation, job execution, sparse matrix operations, and visualization.

.. autosummary::
    :toctree: _autosummary

    lumopt2.utils.common.Box
    lumopt2.utils.common.PNorm
    lumopt2.utils.common.gen_logger
    lumopt2.utils.config_map.ConfigMap
    lumopt2.utils.fd_grad.finite_difference_gradient
    lumopt2.utils.fd_grad.fd_sweep_perturbation
    lumopt2.utils.fd_grad.validate_gradient
    lumopt2.utils.runner.BaseRunner
    lumopt2.utils.runner.LocalRunner
    lumopt2.utils.runner.SlurmRunner
    lumopt2.utils.runner.Job
    lumopt2.utils.sparse_helpers.dense_to_sparse_indices
    lumopt2.utils.sparse_helpers.sparse_to_dense_indices
    lumopt2.utils.sparse_helpers.sparse_to_sparse
    lumopt2.utils.visualizer.OptimizationVisualizer
