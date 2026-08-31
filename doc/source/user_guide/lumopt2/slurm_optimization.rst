Running lumopt2 optimization on a cluster with Slurm
====================================================

You can run ``lumopt2`` optimizations on a compute cluster with the Slurm job scheduler using the :py:class:`~lumopt2.utils.runner.SlurmRunner` class.
This allows you to utilize high-performance computing resources for your optimization tasks.

Prior to creating optimization scripts for running on a cluster, ensure that your cluster is configured for Lumerical. For further information, see `Running lumerical on a local on-presmise cluster <https://optics.ansys.com/hc/en-us/articles/4408499754003-Running-Lumerical-on-a-Local-On-premise-Cluster>`_.

Overview
--------

When you run ``lumopt2`` on a cluster, the optimization process is set up to submit the most computationally intensive tasks to each of the cluster's compute nodes, whereas the submitting node, known as the head node, is responsible for the orchestration of the optimization problem.
The diagram below illustrates the steps done by the head node and the compute nodes during a ``lumopt2`` optimization.

.. image:: /_static/images/lumopt2_head_compute_division.png
    :align: center
    :width: 65%

Optimization scripts for Slurm - pure functions
-----------------------------------------------

To create an optimization for a slurm cluster, you can generally define the optimization problem in the same way as a local optimization, but with an additional requirements for functions that are executed on the compute nodes because the compute node won't have access to the same environment.
All functions that needs to execute on the compute node, **commonly the parameter definition function, the figure of merit objective function, and configuration functions**, must adhere to the following additional requirements:

1. The function must not be a lambda function.
2. The function can only use the following namespaces: ``lumopt2``, ``np`` for ``numpy``, and ``anp`` for ``autograd.numpy``.
3. The function must not contain reference any global variables or objects. All auxiliary functions and variables must be defined within the function scope.

``lumopt2`` examines functions for these requirements prior to running, and the script does not run if the requirements are not met.

.. tip::

    The following tips can help you create ``lumopt2`` scripts that are compatible with Slurm:

    - Use the ``lumopt2`` namespace for all lumopt2 object and functions, not ``lmpt`` or previous imported names.
    - For constant and parameters, consider saving them to a shared location using :py:func:`numpy.savez` and loading them within the function using :py:func:`numpy.load`.
    - If you replace the slurm runner with a local runner, the optimization script should run without any changes. However, the pure function requirement isn't verified in this case.

Setting up the Slurm runner
---------------------------

Setting up ``lumopt2`` for Slurm requires the use of the :py:class:`~lumopt2.utils.runner.SlurmRunner` class, which defines the Slurm job parameters and manages the submission of jobs to the cluster.
The Slurm runner class uses a configuration object from :py:class:`~lumopt2.utils.runner.SlurmConfig` to define critical parameters.

To use a Slurm runner for your simulation, first set up the Slurm configuration object.

.. code-block:: python
    :linenos:

    slurm_config = SlurmConfig(
        base_dir="/path/to/base/directory", # This directory stores logs for the optimization and is shared between the head node and compute nodes.
        fdtd_engine_path="/path/to/fdtd/engine", # This is the path to the fdtd-engine executable.
        fdtd_gui_path="/path/to/fdtd/gui", # This is the path to the fdtd-solutions executable.
        python_path="/path/to/lumerical/python", # This is the path to the Lumerical Python directory for lumopt2, typically /opt/Lumerical/vxxx/api/python
        python_exe_path="/path/to/python/executable", # This is the path to the Python executable for your virtual environment.
        excluded_partitions="excluded partitions", # This controls the partitions that you do not want to run on in the cluster
        )

After setting up the configuration, you can set up the Slurm runner object.

.. code-block:: python
    :linenos:

    fdtd_session_head_slurm = lmpt.FdtdSession(show_fdtd_cad=False) # The slurm runner requires a SEPARATE FDTD session

    slurm_runner = SlurmRunner(
        slurm_config=slurm_config, # Points to the SlurmConfig object
        fdtd_session=fdtd_session_head_slurm,
        resource=resource, # "GPU" or "CPU"
        sim_threads_per_process='32', # Number of threads to use for each FDTD simulation process, only applies to CPU optimizations.
        py_threads_per_process='32', # Number of threads to use for each Python process. The Python processes are responsible for calculations of the FoM and other operations that are not done in FDTD.
        num_concurrent_d_eps='1', # Number of concurrent d_eps calculations.
        gpu_targets=['sample_gpu_name'], # List of GPU targets to use for the optimization
    )

Finally, set up the project and optimization objects as you would for a local optimization.

.. note::

    The :py:class:`~lumopt2.core.project.Project` object must use a separate FDTD session from the Slurm runner.

.. code-block:: python
    :linenos:

    fdtd_session = lmpt.FdtdSession()

    project = lmpt.Project(
        setup=generate_base_sim,
        fdtd_session=fdtd_session,
        parametrization=parametrization,
        runner=slurm_runner,
        fom=fom
        )

    optimizer = lmpt.ScipyOptimizer()
    optimization = lmpt.Optimization(project, optimizer)

    optimization.run()

.. tip::

    Considering using a configuration file or environment variable to store critical paths and settings to use in a variety of ``lumopt2`` scripts.

