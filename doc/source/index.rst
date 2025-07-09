PyLumerical documentation |version|
===================================


PyLumerical is the Python automation library for Ansys Lumerical photonics simulation software. Use PyLumerical to seamlessly control Ansys Lumerical products including Ansys Lumerical FDTD™, Ansys Lumerical MODE™, Ansys Lumerical Multiphysics™, and Ansys Lumerical INTERCONNECT™ directly in Python.

You can use PyLumerical to set up geometry and material, run simulations, and retrieve results from Lumerical products, while leveraging the power of extensive Python libraries. 

If you have existing automation in the Lumerical Scripting Language, you can also use them seamlessly with PyLumerical, and build your Python workflow around them.

As a part of the PyAnsys project, PyLumerical also enables you to integrate with other Ansys products to create complex and accurate multiphysics workflows.

.. note::

   The Lumerical inverse design library lumopt and the high performance computing (HPC) scheduler automation library lumslurm aren't available in PyLumerical, and only available as a part of the Lumerical Python API.

   The Lumerical Python API is still provided with Lumerical products. If you wish to use the Lumerical Python API instead of PyLumerical, please see the `Lumerical Python API documentation <https://optics.ansys.com/hc/en-us/articles/360037824513-Python-API-overview>`_ in the Lumerical Knowledge Base.

.. grid:: 3

   .. grid-item-card:: Getting started
      :link: getting_started/index
      :link-type: doc

      New to PyLumerical? This quick start guide provides you with information to rapidly get started.

   .. grid-item-card:: User guide
      :link: user_guide/index
      :link-type: doc

      In-depth information on key concepts of PyLumerical.

   .. grid-item-card:: API reference
      :link: api/index
      :link-type: doc

      Desciption of classes and methods of the PyLumerical module.


..
   Just reuse the root readme to avoid duplicating the documentation.
   Provide any documentation specific to your online documentation
   here.

.. include:: ../../README.rst
   :start-after: .. contribute_start

.. toctree::
   :hidden:
   :maxdepth: 3

   getting_started/index
   user_guide/index
   api/index
   examples
   contributing
   changelog



