.. grid:: 1 2 2 2

    .. grid-item::

        .. button-link:: ../../_static/simulation_examples/lumopt2_3x3pillar/metalens_3x3.py
            :color: secondary
            :shadow:
            :align: center

            :octicon:`download` Download Python Script (.py)


    .. grid-item::

        .. button-link:: ../../_static/simulation_examples/lumopt2_3x3pillar/metalens_3x3.fsp
            :color: secondary
            :shadow:
            :align: center

            :octicon:`download` Download Simulation File (.fsp)

Getting started with lumopt2: simple metalens
==================================================

This article discusses the usage of the lumopt2 inverse design module in Lumerical FDTD for a basic parametric optimization.

Using a basic metalens formed by a 3x3 array of pillars, this example highlights key functionalities of the lumopt2 module and walks you through the steps necessary to create and run a simple optimization.
The simulation file and script associated with this example can be downloaded using the download buttons above.

Prior to working through the example, please ensure that lumopt2 is successfully set up and importable as seen from the :doc:`introduction <../photonic_inverse_design_with_lumopt2>` page.

Base simulation file
--------------------
The base simulation file consists of an array of 9 silicon cylinders, arranged in a 3x3 array, embedded in an silicon oxide substrate. Each cylinder has a fixed height, but the radius can vary within set bounds for optimization. This structure mimics a simple metalens arrangements with cylindrical meta-atoms.

.. image:: ../../_static/images/lumopt2_3x3pillar/pillar_schematic.png
    :align: center
    :alt: Schematic of the 3x3 pillar structure

A Gaussian source illuminates the metalens from above. The optimization aims to maximize the field intensity in a central region of a plane below the metalens, normalized by the intensity across the full plane within the simulation region. This drives the metalens to focus the beam onto the target region.

.. image:: ../../_static/images/lumopt2_3x3pillar/sim_setup.png
    :align: center
    :scale: 75%
    :alt: Simulation setup showing the 3x3 pillar structure with source and monitor.

The attached Lumerical FDTD project (.fsp) file contains the already set up base simulation, with a `simulation region <https://optics.ansys.com/hc/en-us/articles/360034382534-FDTD-solver-Simulation-Object>`__, `gaussian source <https://optics.ansys.com/hc/en-us/articles/360034382854-Plane-wave-and-beam-source-Simulation-object>`__, `cylinder geometries <https://optics.ansys.com/hc/en-us/articles/360034901513-Circle-Simulation-Object>`__, as well as `field region objects <https://optics.ansys.com/hc/en-us/articles/36967414684947-Field-Region-Simulation-object>`__ that are used in the figure of merit.

This example omits the details in setting up the base simulation file, but you can do this by using the `FDTD GUI interface <https://optics.ansys.com/hc/en-us/articles/360033154434-FDTD-product-reference-manual>`__, via the `Lumerical Scripting Language <https://optics.ansys.com/hc/en-us/articles/360037228834-Lumerical-scripting-language-By-category>`__, via :doc:`PyLumerical <../index>`, or a combination thereof. You can pre-configure your simulation as done in this example or choose to set up the simulation along side your lumopt2 optimization script.

.. tip::
    For lumopt2 optimizations, specific objects, such as `field region <https://optics.ansys.com/hc/en-us/articles/36967414684947-Field-Region-Simulation-object>`__ or `ports <https://optics.ansys.com/hc/en-us/articles/360034382554-Ports-FDTD-Simulation-Object>`__ are required for setting up the figure-of-merit.

Importing libraries
-------------------

To start using lumopt2, use the following import statement.

.. code-block:: python
    :lineno-start: 5

    import ansys.lumerical.core.lumopt2 as lmpt

The lumopt2 module exposes various important classes and functions directly from the top level namespace. For a full list of available functions, and for module level descriptions, refer to the :doc:`API reference <../../api/lumopt2/index>`.

Optimization region setup
------------------------------

Define the optimization region using the :py:class:`~lumopt2.utils.common.Box` class.

.. code-block:: python
    :lineno-start: 12

    optimization_region = lmpt.Box(x_span = 1e-6, y_span = 1e-6, z_min = 1e-6, z_max = 1e-6 + 750e-9,
                               dx = 0.025e-6, dy = 0.025e-6, dz = 0.025e-6)

This defines a box with 1 micron side length in the x and y-diirections, and a height of 750 nm in the z-direction, covering the area where the pillar geometry is expected to change.

.. note::

    Ensure that your optimization region fully contains all possible changes to the geometry during optimization.

Parametrization setup
----------------------

Link each cylinder radius to the optimization using the :py:class:`~lumopt2.parametrization.parametrization.Parametrization`, which maps arbitrary parameters in the optimization problem to properties of pre-existing Lumerical objects.
This class is the most general way to parametrize a design in lumopt2, and does not rely on geometry-specific operations like :py:class:`~lumopt2.parametrization.closed_curve.ClosedCurve`.

.. tip::

    For an example of setting up a parametric optimization using the :py:class:`~lumopt2.parametrization.closed_curve.ClosedCurve`, see the :doc:`L-bend example <getting_started_l_bend>`.

.. code-block:: python
    :lineno-start: 16

    num_cyl = 3*3
    bounds = [(0.05e-6, 0.1e-6)]*num_cyl
    def param_func(params):
        return {f'cyl{idx}::radius': value for idx, value in enumerate(params)}
    parametrization = lmpt.Parametrization(func=param_func, bounds=bounds, optimization_region=optimization_region)

Define the bounds for each cylinder.
Here the bounds variable defines the lower and upper bound for each pillar individually. For simplicity, the same bounds are used for all pillars, by defining the tuple ``(lower_bound, upper_bound)`` and repeating it in a list for the total number of pillars.

.. code-block:: python
    :lineno-start: 17

    bounds = [(0.05e-6, 0.1e-6)]*num_cyl

The :py:class:`~lumopt2.parametrization.parametrization.Parametrization` class takes in a function, ``param_func`` that maps between the optimization parameters and the Lumerical object properties.
The function needs to map a parameter array to a dictionary, such that the keys correspond to the object properties in the Lumerical simulation, and the values are calculated from elements in the parameter array.
The mapping function is as follows.

.. code-block:: python
    :lineno-start: 18

    def param_func(params):
        return {f'cyl{idx}::radius': value for idx, value in enumerate(params)}

For this problem, the function generates a dictionary by enumerating through the input parameter array.
The keys are in the format of ``cyl{idx}::radius``, where the field prior to ``::``, such as ``cyl0``, ``cyl1``, corresponds to the Lumerical object names as set up in the simulation file, and the field after ``::`` corresponds to the name of the object property.
If you set up objects in a group, the format is ``group_name::object_name::property_name``.

.. tip::

    You can check the list of property names for an object with the `getnamed <https://optics.ansys.com/hc/en-us/articles/360034408574-getnamed-Script-command>`__ command, or through the GUI.

Finally, create the ``parametrization`` class by passing in the function that generates the map, the bounds, and the optimization region from earlier.

.. code-block:: python
    :lineno-start: 18

    parametrization = lmpt.Parametrization(func=param_func, bounds=bounds, optimization_region=optimization_region)


Figure of merit setup
---------------------

As explained before, the target of this optimization example is to maximize the ratio of the field intensity at a "focus" region compared to a normalization region.

.. code-block:: python
    :lineno-start: 26

    # Sum of field intensity at 'focus' normalized by sum of field intensity at 'norm'
    intensity_focus = lmpt.FieldResults(monitor_name='focus', metric='intensity', wavelengths = 940e-9)
    intensity_norm = lmpt.FieldResults(monitor_name='norm', metric='intensity', wavelengths = 940e-9)
    def custom_fct(result_list):
        return result_list[0]/result_list[1]
    fom = lmpt.Fom([intensity_focus, intensity_norm], fct = custom_fct)

Here, the code defines the two simulation results using the :py:class:`~lumopt2.fom.simulation_results.FieldResults` class, which takes in the name of a field region object, ``focus`` or ``norm``, the result to extract, ``intensity``, and the wavelength to extract the field at, which is 940nm.

.. code-block:: python
    :lineno-start: 27

    intensity_focus = lmpt.FieldResults(monitor_name='focus', metric='intensity', wavelengths = 940e-9)
    intensity_norm = lmpt.FieldResults(monitor_name='norm', metric='intensity', wavelengths = 940e-9)

Next, the two simulation results must be combined into a single figure of merit value, which is accomplished through a custom function.
The function assumes a list of numbers as input, which are the simulation results ``intensity_focus`` and ``intensity_norm`` in this case.

.. code-block:: python
    :lineno-start: 29

    def custom_fct(result_list):
        return result_list[0]/result_list[1]

Finally, create the figure of merit using :py:func:`~lumopt2.fom.fom.Fom`, with the first argument as the list of results, and the second argument as the function defined earlier to convert the results to an optimization target.

.. code-block:: python
    :lineno-start: 31

    fom = lmpt.Fom([intensity_focus, intensity_norm], fct = custom_fct)

.. note::

    The field region object only accepts a single wavelength, but you can use :ref:`multiple configurations <multi-sim-config>` for multiple wavelengths. The :py:class:`~lumopt2.fom.simulation_results.PortResults` class does support multiple wavelengths directly. See the :doc:`L-bend example <getting_started_l_bend>` for more details.

Project setup
-------------

Now that the base simulation, parametrization, and figure of merit are defined, combine them all in an optimization project using the :py:class:`~lumopt2.core.project.Project` class.
In addition, the :py:class:`~lumopt2.core.project.Project` class can also be used to specify how the FDTD simulations are run via the ``fdtd_session`` and ``runner`` parameters.

.. code-block:: python
    :lineno-start: 34

    project = lmpt.Project(setup = os.path.join(cwd_path, 'metalens_3x3.fsp'), parametrization = parametrization, fom = fom,
                       fdtd_session = lmpt.FdtdSession(show_fdtd_cad = False), runner = lmpt.LocalRunner(resource = 'GPU'))

Here, the base simulation is set up via the pre-existing .fsp file, and the parametrization and figure of merit are set up as seen from previous sections. The FDTD session defined by :py:class:`~lumopt2.core.fdtd_session.FdtdSession` specifies that the FDTD GUI will remain hidden to avoid FDTD windows popping up during the optimization.
Finally, the local runner defined by :py:class:`~lumopt2.utils.runner.LocalRunner` specifies that the first GPU resource enabled in the `FDTD Resource Configuration <https://optics.ansys.com/hc/en-us/articles/360058790674-Resource-configuration-elements-and-controls>`__ will be used.

.. tip::

    For further information on setting up resources, see the `Resource configuration elements and controls Knowledge Base article <https://optics.ansys.com/hc/en-us/articles/360058790674-Resource-configuration-elements-and-controls>`__.

Validate and run optimization
-----------------------------

After setting up all the optimization components, run ``project.visualize_fom(params=params)`` to validate that the set up is valid, and compute the figure of merit for the initial design.

At this point, the console launches FDTD, and displays the value of the figure of merit.

.. code-block:: bash

    XX:XX:XX - INFO - FDTD version '8.35.4519' meets the minimum requirement.
    XX:XX:XX - INFO - Generating optimization project...
    XX:XX:XX - INFO - FoM value is: 0.07328441206421814
    XX:XX:XX - INFO - FDTD version '8.35.4519' meets the minimum requirement.
    Press Enter to continue...

In the FDTD window that opens, you can confirm that the simulation region is in the right position using the ``optimization_mesh``, ``optimization_dft``, and ``optimization_index`` objects.

.. image:: ../../_static/images/lumopt2_3x3pillar/sim_validation.png
    :align: center
    :scale: 75%
    :alt: FDTD simulation window showing the optimization region and monitors.

After this validation, the optimization object is set up using the :py:class:`~lumopt2.core.project.Project` class from earlier, the :py:class:`~lumopt2.optimizer.scipy_optimizer.ScipyOptimizer` class for defining the optimization algorithm, and the :py:class:`~lumopt2.utils.graphical_visualizer.GraphicalVisualizer` class for configuring the data displayed during optimization.
The :py:class:`~lumopt2.optimizer.scipy_optimizer.ScipyOptimizer` class takes in the optimization bounds, the maximum number of iterations, and the tolerance for convergence. These are passed to the default recommended optimizer in the `scipy <https://scipy.org/>`__ python library, which is L-BFGS-B.
For further discussions on optimizers, see the :ref:`optimizer section of the optimization session article <optimization-session-optimizers>`.

.. code-block:: python
    :lineno-start: 41

    optimizer = lmpt.ScipyOptimizer(bounds = bounds, max_iter = 15, gtol = 1e-9)
    visualizer = lmpt.GraphicalVisualizer()
    optimization = lmpt.Optimization(project, optimizer, visualizer)

Finally, use the ``optimization.run()`` method to start the optimization.

.. code-block:: python
   :lineno-start: 44

    optimization.run()

When the optimization starts, the console outputs the current progress, and a matplotlib window opens to visualize results for each iteration. A new folder is also created to store the optimization results with the name format ``lumopt2_project_<time_stamp>``.

The optimization in this example is set to run for a maximum of 15 iterations. After each iteration, the plot updates and shows the current figure of merit value, as well as the L2 norm of the parameter gradient, calculated as :math:`\sqrt{\sum_i (\frac{\partial \text{FoM}}{\partial \text{Param}_i})^2}`.

.. tip::

    You can customize the visualizer to display different metrics. For more information, see :doc:`callback article <callbacks>`.

Results
--------

After the optimization finishes, the final optimized parameters are displayed in the console along with the final figure of merit.

.. code-block:: bash

    XX:XX:XX - INFO - ============================================================
    XX:XX:XX - INFO - Optimization completed
    XX:XX:XX - INFO - Final FOM: 0.123604
    XX:XX:XX - INFO - Total iterations: 15
    XX:XX:XX - INFO - Stopping reason: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT
    XX:XX:XX - INFO - ============================================================
    XX:XX:XX - INFO - Saved optimization plot to <optimization_folder/optimization_plot_iter15.png>
    XX:XX:XX - INFO - Best parameters (9 values):
    XX:XX:XX - INFO -   [ 7.61010969e-08,  1.00000000e-07,  7.66330617e-08,  5.00000000e-08,  5.18586837e-08,
    XX:XX:XX - INFO -     5.00000000e-08,  7.61160062e-08,  1.00000000e-07,  7.66139584e-08]

The final optimization plot is as follows.

.. image:: ../../_static/images/lumopt2_3x3pillar/final_optimization_results.png
    :align: center
    :width: 80%
    :alt: Optimization plot showing the figure of merit and gradient norm over the course of the optimization.

.. tip::

    You can also export the optimized design back to a Lumerical FDTD project file. To do so, use the :py:class:`Project.save_project() <lumopt2.core.project.Project>` method.

Further resources
-----------------

After completing this example, further explore lumopt2 using the following pages.

.. grid:: 2 2 3 3

    .. grid-item-card:: lumopt2 user guide
        :link: ../photonic_inverse_design_with_lumopt2
        :link-type: doc

        Reference for key concepts in lumopt2 in further detail.

    .. grid-item-card:: lumopt2 API reference
        :link: ../../api/lumopt2/index
        :link-type: doc

        Full API reference for lumopt2, including all available classes and functions.

    .. grid-item-card:: L-Bend example
        :link: getting_started_l_bend
        :link-type: doc

        Learn about the workflow for photonic integrated circuit through a more complex example with an L-bend.

.. grid:: 1 2 2 2

    .. grid-item::

        .. button-link:: ../../_static/simulation_examples/lumopt2_3x3pillar/metalens_3x3.py
            :color: secondary
            :shadow:
            :align: center

            :octicon:`download` Download Python Script (.py)


    .. grid-item::

        .. button-link:: ../../_static/simulation_examples/lumopt2_3x3pillar/metalens_3x3.fsp
            :color: secondary
            :shadow:
            :align: center

            :octicon:`download` Download Simulation File (.fsp)

..