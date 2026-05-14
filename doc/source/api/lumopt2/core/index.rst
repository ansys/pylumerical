Core
====

The core module manages FDTD sessions, project setup, configuration, and the main optimization loop.
It provides the central orchestration layer that ties together parametrization, figures of merit,
and optimizers into a complete inverse design workflow.

.. grid:: 2 2 3 3

    .. grid-item-card:: core.fdtd_session
        :link: fdtd_session
        :link-type: doc

        FDTD session management, simulation status, and error handling.

    .. grid-item-card:: core.optimization
        :link: optimization
        :link-type: doc

        The main optimization loop and result container.

    .. grid-item-card:: core.project
        :link: project
        :link-type: doc

        Project setup linking parametrization, FOM, and FDTD session.

    .. grid-item-card:: core.project_config
        :link: project_config
        :link-type: doc

        Configuration for modifying the base simulation.

.. toctree::
   :hidden:

   fdtd_session
   optimization
   project
   project_config
