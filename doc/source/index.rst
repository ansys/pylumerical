PyLumerical |version|
===================================

PyLumerical is the Python automation library for Ansys Lumerical photonics simulation software. Use PyLumerical to seamlessly control Ansys Lumerical products including Ansys Lumerical FDTD™, Ansys Lumerical MODE™, Ansys Lumerical Multiphysics™, and Ansys Lumerical INTERCONNECT™ directly in Python.

Capabilities
-------------------

.. grid:: 1 3 3 3
   :gutter: 3

   .. grid-item-card:: Run Lumerical products directly in Python
      :text-align: center
      :padding: 3 3 4 4

      Set up geometry, material, run simulations locally and on cloud, and retrieve results from Lumerical products.


   .. grid-item-card:: Seamlessly integrate existing automation
      :text-align: center
      :padding: 3 3 4 4

      Leverage Lumerical Scripting Language commands with Pythonic syntaxes, seamlessly integrate with existing automation scripts.


   .. grid-item-card:: Leverage the Python and PyAnsys ecosystem
      :text-align: center
      :padding: 3 3 4 4

      Leverage extensive Python libraries and easily integrate with other Ansys products through the PyAnsys ecosystem to create powerful multiphysics workflows.

Documentation
--------------

.. grid:: 2 2 3 3

   .. grid-item-card::
      :link: getting_started/index
      :link-type: doc

      :fa:`person-running` Getting started
      ^^^

      New to PyLumerical? This quick start guide provides you with information to rapidly get started.


   .. grid-item-card::
      :link: user_guide/index
      :link-type: doc

      :fa:`book` User guide
      ^^^

      In-depth information on key concepts of PyLumerical.

   .. grid-item-card::
      :link: api/index
      :link-type: doc

      :fa:`code` API reference
      ^^^

      Description of classes and methods of the PyLumerical module.

.. grid:: 2 2 2 2

   .. grid-item-card::
      :link: examples
      :link-type: doc

      :fa:`clone` Examples
      ^^^

      Application examples with PyLumerical.

   .. grid-item-card::
      :link: contributing
      :link-type: doc

      :fa:`user-group` Contributing
      ^^^

      Learn how to contribute to the PyLumerical project.

.. note::

   The Lumerical inverse design library `lumopt` and the high performance computing (HPC) scheduler automation library `lumslurm` are currently only available as a part of the Lumerical Python API and unavailable in PyLumerical.

   The `Lumerical Python API <https://optics.ansys.com/hc/en-us/articles/360037824513-Python-API-overview>`_ is still provided with Lumerical products.

.. toctree::
   :hidden:
   :maxdepth: 3

   getting_started/index
   user_guide/index
   api/index
   examples
   contributing
   changelog



