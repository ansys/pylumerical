Callbacks
==========

Callbacks are functions that are called at specific points during the optimization, you can use callbacks to visualize and log results during the optimization.
To use callbacks, pass a list of callback objects to the :py:class:`~lumopt2.core.optimization.Optimization` class as the ``callbacks`` argument.

.. code:: python

   optimization = lmpt.Optimization(
       project=project,
       optimizer=optimizer,
       callbacks=[visualizer_callback, file_logger_callback, custom_callback,...]
   )

If you do not explicitly provide any callbacks, a :py:class:`~lumopt2.utils.file_logger.FileLogger` is automatically added so every run produces a log file in the project folder.

To disable all callbacks, pass an empty list to the argument ``callbacks``.

.. code:: python

   optimization = lmpt.Optimization(
       project=project,
       optimizer=optimizer,
       callbacks=[]
   )

Built-in callbacks
------------------

The lumopt2 module provides various built-in callbacks for simple visualization and logging. You can also define your own callbacks as seen in the section below.

Visualization
~~~~~~~~~~~~~

:py:class:`~lumopt2.utils.graphical_visualizer.GraphicalVisualizer` creates a live matplotlib figure that updates as the optimization progresses.
You compose the figure from a list of panels, each of which owns one subplot.
The visualizer by default saves a PNG image of the figure to the project folder after every update.

.. code:: python

   visualizer = lmpt.GraphicalVisualizer()
   optimization = lmpt.Optimization(project, optimizer, callbacks=[visualizer])

The following panels are available:

- :py:class:`~lumopt2.utils.panels.fom.FomPanel`: plots the figure of merit vs. iteration.
- :py:class:`~lumopt2.utils.panels.gradient.GradientNormPanel`: plots the gradient norm vs. iteration.
- :py:class:`~lumopt2.utils.panels.geometry.GeometryPanel`: shows the current geometry, only available for closed curve parametrization.
- :py:class:`~lumopt2.utils.panels.monitor.MonitorPanel`: plots the result of any monitor object.

When you do not specify panels, the visualizer automatically plots adds a :py:class:`~lumopt2.utils.panels.fom.FomPanel`, a :py:class:`~lumopt2.utils.panels.gradient.GradientNormPanel`, and a :py:class:`~lumopt2.utils.panels.geometry.GeometryPanel` for closed curve parametrizations.

To compose a custom figure, pass a list of panels and set the grid layout with ``layout=(rows, cols)``.
The example below sets up a 2x2 figure with a figure-of-merit panel, gradient norm, geometry view, and a field monitor:

.. code:: python

   visualizer = lmpt.GraphicalVisualizer(
       figsize=(12, 10),
       layout=(2, 2),
       panels=[
           lmpt.FomPanel(),
           lmpt.GradientNormPanel(),
           lmpt.GeometryPanel(),
           lmpt.MonitorPanel(
               monitor_name='field_monitor',
               result_name='Ey',
               operation='real',
               title='Ey field (real part)',
           ),
       ],
       save_plots=True,
       block_on_end=True,
   )

To run without an on-screen window, set ``show_window=False``.
In this case, the visualizer still saves the images to the project folder.

.. code:: python

   visualizer = lmpt.GraphicalVisualizer(show_window=False, save_plots=True)

You can also control whether the visualizer plots every iteration, or only after a certain interval.

.. code:: python

   visualizer = lmpt.GraphicalVisualizer(update_interval=5) # Update only once every 5 iterations

Logger
~~~~~~

:py:class:`~lumopt2.utils.file_logger.FileLogger` writes a log of the optimization run to a file called ``optimization.log`` in the project folder.
Each evaluation and each iteration is written as a single line containing the figure of merit value, the parameter vector, and the elapsed time.

.. code:: python

   file_logger = lmpt.FileLogger()
   optimization = lmpt.Optimization(project, optimizer, callbacks=[file_logger])


To write the log to a specific path instead of the default project folder, pass a path as a string to the ``log_file`` argument:

.. code:: python

   file_logger = lmpt.FileLogger(log_file='path_to_my_logfile.log')

Custom callbacks
----------------

Structure
~~~~~~~~~

You can define your own callback by creating a class that uses :py:class:`~lumopt2.utils.callbacks.BaseCallback` as a subclass, and override the methods triggers at certain points during the optimization.
You only need to override the relevant methods in your custom callback function, as all other methods are empty by default.

The example below shows a custom callback that prints the figure of merit value at the end of each iteration.

.. code:: python

   import lumopt2 as lmpt

   class MyCallback(lmpt.BaseCallback):
       def on_iteration_end(self, project, iteration, params, fom_value,
                            gradient=None, **kwargs):
           print(f"Iteration {iteration}: FOM = {fom_value:.4e}")

   optimization = lmpt.Optimization(project, optimizer, callbacks=[MyCallback()])

Trigger timings
~~~~~~~~~~~~~~~

The following methods are available to override, listed in the order they are called during a run:

- ``on_optimization_start(self, project, num_params, bounds, **kwargs)``: called once before the optimization starts.
- ``on_iteration_start(self, iteration, params, **kwargs)``: called before each iteration.
- ``on_function_eval(self, project, eval_num, params, fom_value, gradient=None, **kwargs)``: called after every figure of merit evaluation. This can fire multiple times per iteration.
- ``on_iteration_end(self, project, iteration, params, fom_value, gradient=None, **kwargs)``: called after each iteration completes.
- ``on_optimization_end(self, success, final_fom, final_params, num_iterations, **kwargs)``: called once when the optimization finishes. This is always called, even if the run is interrupted.
