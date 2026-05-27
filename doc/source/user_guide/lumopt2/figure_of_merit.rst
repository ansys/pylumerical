Figure of merit
===============

The figure of merit is the formulation of the optimization goal.
In lumopt2, figure of merits derive from simulation results, which in turn derives from monitors in the base simulation.
After it you define a figure of merit for the optimization, it is passed into the project class.

Simulation results
------------------

The lumopt2 module supports two types of simulation results, :py:class:`~lumopt2.fom.simulation_results.PortResults` and :py:class:`~lumopt2.fom.simulation_results.FieldResults`.

The :py:class:`~lumopt2.fom.simulation_results.FieldResults` class extracts the intensity of fields from a `field region <https://optics.ansys.com/hc/en-us/articles/36967414684947-Field-Region-Simulation-object>`__.

To define a field result object, you need to specify the name of the field region object, the metric to extract, and the wavelength to evaluate the results at.

.. warning::

   The field region object only accepts a single wavelength.

.. code:: python

   # Create a field result object for a wavelength of 940 nm

   intensity = lmpt.FieldResults(monitor_name='field_result', metric='intensity', wavelengths = 940e-9)

The :py:class:`~lumopt2.fom.simulation_results.PortResults` class extracts transmission data from a `FDTD port object <https://optics.ansys.com/hc/en-us/articles/360034382554-Ports-FDTD-Simulation-Object>`__.
This class is typically used for for photonic integrated circuit applications.

To define a port result object, you need to specify the name of the port, the metric to evaluate, as well as the wavelengths to extract the result for.
You can also define a port result object for multiple wavelengths, using a list or numpy array.

.. code:: python

   # Create a port result object for a wavelength between 1200nm and 1400nm (O-Band)

   wavelengths = np.linspace(1200e-9, 1400e-9, 21)
   port_results = lmpt.PortResults('port_out', metric='transmission', wavelengths=wavelengths)

Defining a figure of merit
--------------------------

Once the you create the simulation results, you must then define a figure of merit using the :py:func:`~lumopt2.fom.fom.Fom`, which is used as the target for optimization.

This function takes in simulation result objects, and applies either a pre-defined or custom functions to formulate the figure of merit.
Without defining your own function for the figure of merit, the default functions are to use the mean for field results, and P-norm for port results.

You can provide multiple simulation results as a list to the function. In this case, the default function takes the mean of all field results, or the P-norm of the concatenated port results. When you provide a list, all results must be of the same type.

.. code:: python

   # Define a figure of merit based on a simulation result, using the default function
   # The simulation results are previous defined using PortResult or FieldResults class

   fom = lmpt.Fom(my_simulation_results)

To define a custom function for the figure of merit, you can pass in a callable to the ``fct`` field of the :py:func:`~lumopt2.fom.fom.Fom` function.

This function must take in all simulation results you wish to use as a concatenated autograd array, and outputs a single real-valued scalar value as the figure of merit output.
The function must be differentiable via autograd.

The example below illustrates how to define a custom figure of merit function for a focus region with multiple field region monitors.

.. code:: python

   intensity_focus = lmpt.FieldResults(monitor_name='focus', metric='intensity', wavelengths = 940e-9)
   intensity_norm = lmpt.FieldResults(monitor_name='norm', metric='intensity', wavelengths = 940e-9)
   def custom_fct(result_list):
      return result_list[0]/result_list[1]

   fom = lmpt.Fom([intensity_focus, intensity_norm], fct = custom_fct)

The example below illustrates a weighted sum custom figure of merit for multiple port results.

.. code:: python

   trans_ch1 = lmpt.PortResults('port_out1', metric='transmission', wavelengths=wdm_wavelengths[0], tolerance=5e-9)
   trans_ch2 = lmpt.PortResults('port_out2', metric='transmission', wavelengths=wdm_wavelengths[1], tolerance=5e-9)
   trans_ch3 = lmpt.PortResults('port_out3', metric='transmission', wavelengths=wdm_wavelengths[2], tolerance=5e-9)
   trans_ch4 = lmpt.PortResults('port_out4', metric='transmission', wavelengths=wdm_wavelengths[3], tolerance=5e-9)

   def custom_fct(x):
      p = 2
      pnorm_func = lmpt.PNorm(target=1, p=p)
      fom1 = pnorm_func(x[0])
      fom2 = pnorm_func(x[1])
      fom3 = pnorm_func(x[2])
      fom4 = pnorm_func(x[3])
      return 0.1*fom1 + 0.1*fom2 + 0.3*fom3 + 0.3*fom4

   fom = lmpt.Fom([trans_ch1, trans_ch2, trans_ch3, trans_ch4], fct=custom_fct)


Multiple simulation configuration
---------------------------------

In some cases, it is important to formulate the overall figure of merit based on variations of the same base simulation, for example, multiple wavelengths for the source.

In this case, lumopt2 provides the option to define multiple simulation configurations via the :py:class:`~lumopt2.core.project_config.ProjectConfig` class and the ``config`` argument in simulation results.
You can then combine the result from each simulation configuration into a single figure of merit using the same approach as discussed above.

To create a new project configuration, initialize the :py:class:`~lumopt2.core.project_config.ProjectConfig` with a configurator. The configurator is a a callable function or a path to a Lumerical script file that modifies the base simulation.

For example, you can define the base simulation in ``base_simulation.lsf``, set up the source to be single wavelength, but set up multiple monitors for different wavelengths.

.. code::

   ... #Setup code

   wavelength = 650e-9; # Set to operate at a wavelength of 650 nm in the base simulation

   meshsize = 35e-9;
   setglobalsource('center wavelength',wavelength);
   setglobalsource('wavelength span', 0);
   setglobalsource("optimize for short pulse",false);

   ...
   addfieldregion;
   set('name','fom_red');
   ...

   addfieldregion;
   set('name','fom_blue');

Then, you can define a configuration script that modifies the wavelength of the source in ``blue_config.lsf``.

.. code::

   wl_blue = 450e-9;
   setglobalsource('center wavelength',wl_blue);

When setting up the inverse design project, you can do the following to define the project configuration and use them with the simulation results, and define the figure of merit based on the results of different configurations.

.. code:: python

   config_blue = lmpt.ProjectConfig(configurator=configfile_blue, filename_suffix='blue')
   int_blue   = lmpt.FieldResults('fom_blue',   metric='intensity', wavelengths=450e-9, config=config_blue)

   def custom_fct(x):
      return (x[0] + x[1]) / 2

   fom = lmpt.Fom([int_red, int_green1], fct=custom_fct)

The base setup script is still used when defining the project, but the configuration scripts are automatically applied for the optimization problem when it is run.

.. code:: python

   # Configurator scripts included in fom

   project = lmpt.Project(setup = "base_simulation.lsf",
                       fdtd_session = fdtd_session,
                       parametrization = parametrization,
                       fom = fom)

