Lumerical class
===============

The Lumerical class is the main interface to all Ansys Lumerical products. It represents an interactive session with a Lumerical product, and provides methods to create simulation objects, run simulations, and access results.

Each Lumerical product has its own class that inherits from a base Lumerical class, which can't be directly used.

The table below shows each inherited class and their corresponding Lumerical product.

.. autosummary::
    :toctree: _autosummary

    ansys.lumerical.core.FDTD
    ansys.lumerical.core.MODE
    ansys.lumerical.core.DEVICE
    ansys.lumerical.core.INTERCONNECT

The PyLumerical :doc:`User guide <../user_guide/index>` provides information on how to get started, and details of how to use the Lumerical class methods to interact with Lumerical products.