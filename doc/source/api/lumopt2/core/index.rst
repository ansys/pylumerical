lumopt2.core
============

The core module contains classes to orchestrate the optimization processm, utilizing other modules as the input.

.. grid:: 2 2 3 3

    .. grid-item-card:: core.optimization
        :link: optimization
        :link-type: doc

        Classes for overall optimization workflow and results, using the project, optimizer, and visualizer.

    .. grid-item-card:: core.project
        :link: project
        :link-type: doc

        Main project classes to set up the optimization problem including parameters, FoMs, and resources to run the project on.

    .. grid-item-card:: core.fdtd_session
        :link: fdtd_session
        :link-type: doc

        Classes to interact with a FDTD session.

.. grid:: 2 2 3 3

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
