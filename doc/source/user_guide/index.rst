Getting started
========================
Use Python to analyze data, automate complex workflows, optimizations, and produce publication-quality plots. PyLumerical provides a method to seamlessly use Python to interact with Ansys Lumerical products.

Guides
---------

Important informational resources on key concepts of PyLumerical.

.. grid:: 3

   .. grid-item-card:: Session Management
      :link: https://optics.ansys.com/hc/en-us/articles/360041873053

      Learn how to open, close and interact with Lumerical products through sessions.

   .. grid-item-card:: Script Commands as Methods
      :link: https://optics.ansys.com/hc/en-us/articles/360041579954

      Learn how to interact with Lumerical products using script commands.

   .. grid-item-card:: Working with Simulation Objects
      :link: https://optics.ansys.com/hc/en-us/articles/39744946400659

      Learning how to create and manipulate simulation objects.

.. grid:: 3

   .. grid-item-card:: Passing Data
      :link: https://optics.ansys.com/hc/en-us/articles/360041401434

      Learning how data types are transferred between Lumerical and Python.

   .. grid-item-card:: Accessing Simulation Results
      :link: https://optics.ansys.com/hc/en-us/articles/39744236202771

      Learn how to access simulation results and work with Lumerical datasets.

   .. grid-item-card:: Interop Server
      :link: https://optics.ansys.com/hc/en-us/articles/15499581457811
      
      Learn how to access PyLumerical remotely through the interop server.

My first PyLumerical project
-----------------------------

The code snippet below provides simple project of using PyLumerical to visualize the transmission of a gold thin film illuminated by a planewave.

.. code-block:: python

   import lumapi #Ensure lumapi has already been added to path
   import numpy as np
   import matplotlib.pyplot as plt

   with lumapi.FDTD() as fdtd:
      lambda_range = np.linspace(300e-9, 1100e-9, 500)
      c=2.99792458e8
      f_range = c/lambda_range
      au_index = fdtd.getfdtdindex("Au (Gold) - CRC", f_range, np.min(f_range), np.max(f_range)) #Use the getfdtdindex command to obtain the correct complex index for gold
      

      stackRT_result = fdtd.stackrt(np.transpose(au_index), np.array([10e-9]), f_range) #Use the stackrt command to calculate the transmission and reflection
   #Visualize using matplotlib
   fig, ax = plt.subplots()
   ax.plot(lambda_range*1e9, stackRT_result["Ts"], label="Transmission")
   ax.set_xlabel("Wavelength [nm]")
   ax.set_ylabel("Transmission")
   ax.legend()
   plt.show()

This simulation returns the following result.

.. image:: ../_static/PyLumerical_Example_Image.png
   :alt: PyLumerical example
   :align: center
   :width: 80%

Application examples
----------------------

Application Gallery examples demonstrating how to get started using the Lumerical Python API to interact with Ansys Lumerical products.

Ansys Lumerical FDTD™
~~~~~~~~~~~~~~~~~~~~~~~

- `Nanowire example using FDTD`_ 

.. _Nanowire example using FDTD: https://optics.ansys.com/hc/en-us/articles/360034416574-FDTD-application-example

Ansys Lumerical INTERCONNECT™
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `Monte Carlo analysis in INTERCONNECT`_
- `Optical transceiver co-simulation in INTERCONNECT`_

.. _Optical transceiver co-simulation in INTERCONNECT: https://optics.ansys.com/hc/en-us/articles/360034936773-Python-co-simulation-with-INTERCONNECT
.. _Monte Carlo analysis in INTERCONNECT: https://optics.ansys.com/hc/en-us/articles/360034416574-INTERCONNECT-application-example
