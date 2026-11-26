Base simulation
===============

The base simulation defines the FDTD simulation that is used for optimization.
In lumopt2, you can define the base simulation using an existing Lumerical FDTD ``.fsp`` project file, a Lumerical script file that sets up the simulation, or a Python callable that sets up the simulation.

Setting up the base simulation
------------------------------

The base simulation contains sources, monitors, and geometries necessary for the optimization. To set up the base simulation, you can use the Lumerical FDTD GUI, Lumerical scripting, or Python with PyLumerical.

The following resources provide general information on how to set up Lumerical simulation:

- `FDTD Product Reference Manual <https://optics.ansys.com/hc/en-us/articles/360033154434-FDTD-product-reference-manual>`__
- `Lumerical scripting language index <https://optics.ansys.com/hc/en-us/articles/360037228834-Lumerical-scripting-language-By-category>`__
- :ref:`Simulation automation section of the user guide <simulation-automation>`

.. note::

   You don't need to set up the optimization region in the base simulation, as this is separately defined in Python and passed into the parametrization.

To run optimization using ``lumopt2``, the base simulation needs specific objects to capture the simulation results for the figure of merit. See the :doc:`figure of merit article <figure_of_merit>` for more details.

.. tip::

   If your figure of merit depends on multiple different base simulation setup, you can use the :py:class:`~lumopt2.core.project_config.ProjectConfig` object, along with the ``config`` argument when defining simulation results.
   See the :doc:`figure of merit article <figure_of_merit>` for more details.

The :doc:`simple metalens example <getting_started_simple_metalens>` provides a sample FDTD project file for setting up a base simulation for a general parametric optimization case.
The :doc:`L-bend example <getting_started_l_bend>` provides an example of setting up the base simulation for a photonic integrated circuit application using PyLumerical.
The :doc:`L-bend shape optimization example <getting_started_l_bend_shape>` provides an example of setting up the base simulation for shape optimization.

Further information on setting up the base simulation for each type of optimization are in the sections below.

Parametric optimization
^^^^^^^^^^^^^^^^^^^^^^^

For a general parametric optimization that directly maps optimization parameters to object properties, include the source, field region monitor, and objects whose properties are being optimized in the base simulation.

For parametric optimization using the :py:class:`~lumopt2.parametrization.closed_curve.ClosedCurve` class, typically used in photonic integrated circuit applications, include only the ports and any input and output waveguides.
The optimizable section is set up separately during :doc:`parametrization <parametrization>`.

Shape optimization
^^^^^^^^^^^^^^^^^^

For a shape optimization problem, set up the `layer builder <https://optics.ansys.com/hc/en-us/articles/360034382394-Layer-builder-Simulation-object>`__ object, load the initial gds and process file.

You must ensure that the layer builder object conforms to the following requirements:

- Layer builder is centered at the origin - importing a gds may move the layer builder, ensure it is correctly positioned after the import
- The ``gds position reference`` setting is set to ``Centered at origin``
- Layer builder span is set to cover the entirety of the pattern you wish to optimize

Several layer builder features are unsupported for ``lumopt2``:

- Boolean operation on layers
- Sidewall angle on layers
- Rotation of the layer builder object
- Pattern growth delta

Passing base simulation
-----------------------

The base simulation is passed into the optimization workflow through the :py:class:`~lumopt2.core.project.Project` object, as the :py:class:`Project.setup <lumopt2.core.project.Project>` attribute.

To pass a base simulation that is either a FDTD project or a Lumerical script, provide the file path as a string.
For further information on the :doc:`parametrization <parametrization>`, :doc:`figure of merit <figure_of_merit>`, :ref:`FDTD session <optimization-fdtd-session>`, and :ref:`runner <optimization-runner>`, see the corresponding articles in the user guide.

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


