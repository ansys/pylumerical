.. _ref_release_notes:

Release notes
#############

This document contains the release notes for the project.

.. vale off

.. towncrier release notes start

`0.3.0 <https://github.com/ansys/pylumerical/releases/tag/v0.3.0>`_ - June 11, 2026
===================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Improve autodiscovery to check LUMERICAL_HOME environment variable
          - `#7 <https://github.com/ansys/pylumerical/pull/7>`_

        * - Importing lumopt
          - `#93 <https://github.com/ansys/pylumerical/pull/93>`_

        * - Update Python version to 3.14
          - `#94 <https://github.com/ansys/pylumerical/pull/94>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update \`\`CONTRIBUTORS.md\`\` with the latest contributors
          - `#44 <https://github.com/ansys/pylumerical/pull/44>`_, `#100 <https://github.com/ansys/pylumerical/pull/100>`_

        * - Example: waveguide_FDE and photonic_crystal_bandstructure
          - `#50 <https://github.com/ansys/pylumerical/pull/50>`_

        * - Update burst example in cheatsheet.
          - `#51 <https://github.com/ansys/pylumerical/pull/51>`_

        * - Add example and cheatsheet build flags.
          - `#63 <https://github.com/ansys/pylumerical/pull/63>`_

        * - Added syntax highlighting for examples.
          - `#81 <https://github.com/ansys/pylumerical/pull/81>`_

        * - Add line numbers to code blocks
          - `#82 <https://github.com/ansys/pylumerical/pull/82>`_

        * - Fixed cheatsheet formatting
          - `#84 <https://github.com/ansys/pylumerical/pull/84>`_

        * - Corrected wording and fixed link from AFT
          - `#85 <https://github.com/ansys/pylumerical/pull/85>`_

        * - Example- metalens fdtd
          - `#95 <https://github.com/ansys/pylumerical/pull/95>`_

        * - Added INTERCONNECT example to example index page
          - `#99 <https://github.com/ansys/pylumerical/pull/99>`_

        * - Examples - add output images to examples
          - `#109 <https://github.com/ansys/pylumerical/pull/109>`_

        * - Lumopt2 documentation review
          - `#110 <https://github.com/ansys/pylumerical/pull/110>`_


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Bump jupytext from 1.18.1 to 1.19.0 in the pip-deps group
          - `#52 <https://github.com/ansys/pylumerical/pull/52>`_

        * - Bump jupytext from 1.19.0 to 1.19.1 in the pip-deps group
          - `#57 <https://github.com/ansys/pylumerical/pull/57>`_

        * - Bump ansys-sphinx-theme[autoapi] from 1.6.4 to 1.7.0 in the pip-deps group
          - `#60 <https://github.com/ansys/pylumerical/pull/60>`_

        * - Bump ipykernel from 7.1.0 to 7.2.0 in the pip-deps group
          - `#62 <https://github.com/ansys/pylumerical/pull/62>`_

        * - Bump ansys-sphinx-theme[autoapi] from 1.7.0 to 1.7.1 in the pip-deps group
          - `#71 <https://github.com/ansys/pylumerical/pull/71>`_

        * - Bump ansys-sphinx-theme[autoapi] from 1.7.1 to 1.7.2 in the pip-deps group
          - `#73 <https://github.com/ansys/pylumerical/pull/73>`_

        * - Bump the pip-deps group across 1 directory with 2 updates
          - `#87 <https://github.com/ansys/pylumerical/pull/87>`_

        * - Bump matplotlib from 3.10.8 to 3.10.9 in the pip-deps group across 1 directory
          - `#96 <https://github.com/ansys/pylumerical/pull/96>`_

        * - Bump jupytext from 1.19.1 to 1.19.2 in the pip-deps group
          - `#101 <https://github.com/ansys/pylumerical/pull/101>`_

        * - Bump jupytext from 1.19.2 to 1.19.3 in the pip-deps group
          - `#104 <https://github.com/ansys/pylumerical/pull/104>`_

        * - Bump ansys-sphinx-theme from 1.7.2 to 1.8.0 in the pip-deps group
          - `#106 <https://github.com/ansys/pylumerical/pull/106>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Bump the actions group with 2 updates
          - `#45 <https://github.com/ansys/pylumerical/pull/45>`_, `#75 <https://github.com/ansys/pylumerical/pull/75>`_

        * - Update CHANGELOG for v0.2.0
          - `#46 <https://github.com/ansys/pylumerical/pull/46>`_

        * - Updated source file license headers for 2026
          - `#49 <https://github.com/ansys/pylumerical/pull/49>`_

        * - Bump actions/checkout from 6.0.1 to 6.0.2 in the actions group
          - `#53 <https://github.com/ansys/pylumerical/pull/53>`_

        * - Add missing permission for pull-requests in doc-deploy-dev job
          - `#56 <https://github.com/ansys/pylumerical/pull/56>`_

        * - Fix missing documentation cname environment variable.
          - `#58 <https://github.com/ansys/pylumerical/pull/58>`_

        * - Bump docker/login-action from 3.6.0 to 3.7.0 in the actions group
          - `#59 <https://github.com/ansys/pylumerical/pull/59>`_

        * - Update to use the latest release
          - `#61 <https://github.com/ansys/pylumerical/pull/61>`_

        * - Update missing or outdated files
          - `#70 <https://github.com/ansys/pylumerical/pull/70>`_

        * - Bump actions/download-artifact from 7.0.0 to 8.0.0 in the actions group
          - `#72 <https://github.com/ansys/pylumerical/pull/72>`_

        * - Bump actions/download-artifact from 8.0.0 to 8.0.1 in the actions group
          - `#77 <https://github.com/ansys/pylumerical/pull/77>`_

        * - Add .DS_Store to .gitignore for macOS compatibility
          - `#78 <https://github.com/ansys/pylumerical/pull/78>`_

        * - Bump the actions group across 1 directory with 4 updates
          - `#91 <https://github.com/ansys/pylumerical/pull/91>`_

        * - Bump ansys/actions from 10 to 10.2.12 in the actions group
          - `#97 <https://github.com/ansys/pylumerical/pull/97>`_

        * - Bump ansys/actions from 10.2.12 to 10.3.0 in the actions group
          - `#98 <https://github.com/ansys/pylumerical/pull/98>`_

        * - Bump actions/labeler from 6.0.1 to 6.1.0 in the actions group
          - `#102 <https://github.com/ansys/pylumerical/pull/102>`_

        * - Refactor CI workflows to use common documentation build configuration
          - `#103 <https://github.com/ansys/pylumerical/pull/103>`_

        * - Bump the actions group across 1 directory with 3 updates
          - `#107 <https://github.com/ansys/pylumerical/pull/107>`_


`0.2.0 <https://github.com/ansys/pylumerical/releases/tag/v0.2.0>`_ - December 22, 2025
=======================================================================================

.. tab-set::


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Bump the pip-deps group across 1 directory with 4 updates
          - `#34 <https://github.com/ansys/pylumerical/pull/34>`_

        * - Bump pytest from 9.0.0 to 9.0.2 in the pip-deps group
          - `#37 <https://github.com/ansys/pylumerical/pull/37>`_

        * - Bump the pip-deps group with 2 updates
          - `#41 <https://github.com/ansys/pylumerical/pull/41>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Add \`\`html context\`\`
          - `#26 <https://github.com/ansys/pylumerical/pull/26>`_

        * - PyLumerical Quarto Cheatsheet
          - `#28 <https://github.com/ansys/pylumerical/pull/28>`_

        * - Update \`\`CONTRIBUTORS.md\`\` with the latest contributors
          - `#31 <https://github.com/ansys/pylumerical/pull/31>`_

        * - Jupytext example pages
          - `#33 <https://github.com/ansys/pylumerical/pull/33>`_

        * - Post release wording fix
          - `#42 <https://github.com/ansys/pylumerical/pull/42>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update CHANGELOG for v0.1.0
          - `#23 <https://github.com/ansys/pylumerical/pull/23>`_

        * - Update CODEOWNERS to include additional directories and owners
          - `#29 <https://github.com/ansys/pylumerical/pull/29>`_

        * - Post release cleanup of CI
          - `#32 <https://github.com/ansys/pylumerical/pull/32>`_

        * - Bump the actions group across 1 directory with 4 updates
          - `#36 <https://github.com/ansys/pylumerical/pull/36>`_

        * - Reorganize CODEOWNERS
          - `#39 <https://github.com/ansys/pylumerical/pull/39>`_

        * - Bump codecov/codecov-action from 5.5.1 to 5.5.2 in the actions group
          - `#40 <https://github.com/ansys/pylumerical/pull/40>`_


`0.1.0 <https://github.com/ansys/pylumerical/releases/tag/v0.1.0>`_ - November 14, 2025
=======================================================================================

.. tab-set::


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Add deploy PR documentation label and workflow
          - `#16 <https://github.com/ansys/pylumerical/pull/16>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Add workflows
          - `#5 <https://github.com/ansys/pylumerical/pull/5>`_

        * - Updating numerous files and pipeline for initial release
          - `#17 <https://github.com/ansys/pylumerical/pull/17>`_

        * - Release prep
          - `#20 <https://github.com/ansys/pylumerical/pull/20>`_


.. vale on
