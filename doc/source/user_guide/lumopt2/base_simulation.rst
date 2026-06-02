Base simulation
===============

The base simulation defines the FDTD simulation that is used for optimization.
In lumopt2, you can define the base simulation using an existing Lumerical FDTD ``.fsp`` project file, a Lumerical script file that sets up the simulation, or a Python callable that sets up the simulation.

The base simulation typically contains the necessary geometry, sources, and monitors to run the optimization, including specialized objects to collect supported simulation results for the formulation of the figures of merit.

.. note::

   The :py:class:`~lumopt2.parametrization.closed_curve.ClosedCurve` geometries, which are specialized objects used for photonic integrated circuti applications, are not set up in the base simulation. Instead, they are setup using Python. See the :doc:`parametrization <parametrization>` article for further information.

You don't need to set up the optimization region in the base simulation, as this is separately defined in Python and passed into the parametrization.

Passing base simulation
-----------------------

The base simulation is passed into the optimization workflow through the :py:class:`~lumopt2.core.project.Project` object, as the :py:class:`Project.setup <lumopt2.core.project.Project>` attribute.

To pass a base simulation that is either a FDTD project or a Lumerical script, provide the file path as a string.

.. code:: python

   project = lmpt.Project(setup = os.path.join(cwd_path, 'my_fdtd_project.fsp'), parametrization = parametrization, fom = fom,
                       fdtd_session = fdtd_session, runner = runner)

.. code:: python

   project = lmpt.Project(setup = os.path.join(cwd_path, 'setup_my_fdtd_project.lsf'), parametrization = parametrization, fom = fom,
                       fdtd_session = fdtd_session, runner = runner)

To pass a base simulation that is defined through a Python function, provide the function handle.

.. code:: python

   from my_setup_module import my_setup_function

   project = lmpt.Project(setup = my_setup_function, parametrization = parametrization, fom = fom,
                       fdtd_session = fdtd_session, runner = runner)

.. tip::

   If your figure of merit depends on multiple different base simulation setup, you can use the :py:class:`~lumopt2.core.project_config.ProjectConfig` object, along with the ``config`` argument when defining simulation results.
   See the :doc:`figure of merit article <figure_of_merit>` for more details.

.. tip::

   If you are new to setting up simulations in Ansys Lumerical FDTD™, please refer to the following resources:

   - Using the FDTD GUI: `FDTD Product Reference Manual <https://optics.ansys.com/hc/en-us/articles/360033154434-FDTD-product-reference-manual>`__
   - Using Lumerical scripting: `Lumerical scripting language index <https://optics.ansys.com/hc/en-us/articles/360037228834-Lumerical-scripting-language-By-category>`__
   - Using PyLumerical: :ref:`Simulation automation section of the user guide <simulation-automation>`

.. Not sure if better here or in figure of merit user guide documentation

Simulation objects for optimization
-----------------------------------

The lumopt2 module uses simulation result classes, such as :py:class:`~lumopt2.fom.simulation_results.FieldResults` and :py:class:`~lumopt2.fom.simulation_results.PortResults`, as a basis for defining figures of merit.

These result classes requires input of specific Lumerical simulation objects:
- :py:class:`~lumopt2.fom.simulation_results.FieldResults`: Extracts field data, and requires its data from a `field region <https://optics.ansys.com/hc/en-us/articles/36967414684947-Field-Region-Simulation-object>`__ object.
- :py:class:`~lumopt2.fom.simulation_results.PortResults`: Extracts transmission data from a port, and requires its data from a `FDTD port object <https://optics.ansys.com/hc/en-us/articles/360034382554-Ports-FDTD-Simulation-Object>`__ object.


