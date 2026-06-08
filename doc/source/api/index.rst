API reference
=============

The API reference provides an overview of classes and methods used in PyLumerical.

.. vale off

lumapi
-------

.. vale on

.. grid:: 2 2 3 3

    .. grid-item-card:: Interface classes
        :link: interface_class
        :link-type: doc

        Main classes to programmatically interact with Lumerical products.

    .. grid-item-card:: Auxiliary classes
        :link: simobject_class
        :link-type: doc

        Auxiliary classes used to represent simulation objects, their results, and IDs.

    .. grid-item-card:: Autodiscovery
        :link: autodiscovery
        :link-type: doc

        Function to automatically discover Lumerical installation.

.. vale off

lumopt2
-------

.. vale on

.. grid:: 1 1 1 1

    .. grid-item-card:: lumopt2
        :link: lumopt2/index
        :link-type: doc

        Inverse design module for photonic devices using the adjoint method.

.. toctree::
    :hidden:
    :caption: Simulation Automation

    interface_class
    simobject_class
    autodiscovery

.. toctree::
    :hidden:
    :caption: Photonic Inverse Design

    lumopt2/index