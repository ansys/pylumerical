Contributing
============

PyLumerical follows the `PyAnsys <https://dev.docs.pyansys.com/how-to/contributing.html>`_ contribution guidelines. Ensure that you are familiar with the contents of this guide before contributing to PyLumerical.

The following section provides information for contributing to PyLumerical.

Installing PyLumerical in developer mode
-----------------------------------------

Installing PyLumerical in developer mode allows
you to modify the source and enhance it.

#. Start by cloning this repository:

   .. code:: bash

      git clone https://github.com/ansys/pylumerical

#. Create a clean Python virtual environment:

   .. code:: bash

      # Create a virtual environment
      python -m venv .venv

#. Activate the virtual environment:

   .. tab-set::

        .. tab-item:: Linux

            .. code-block:: bash

                source .venv/bin/activate

        .. tab-item:: Windows Command Prompt

            .. code-block:: bash

                .venv\\Scripts\\activate.bat

        .. tab-item:: Windows Powershell

            .. code-block:: bash

                .venv\\Scripts\\Activate.ps1

#. Install PyLumerical in editable mode:

   .. code:: bash

      python -m pip install -U pip
      python -m pip install -e .

#. Install additional requirements as needed for documentation and tests:

   .. code:: bash

      python -m pip install .[tests]
      python -m pip install .[doc]

Code style
----------

Use `pre-commit`_ to ensure that your code meets the style requirements for PyLumerical prior to filing a pull request. The automatic CI/CD procedures uses the same checks as pre-commit, hence, it's preferable to first run pre-commit locally.

To install `pre-commit`_ and check over all your files, run the following commands:

.. code:: bash

    pip install pre-commit
    pre-commit run --all-files


You can also set up pre-commit as a hook to automatically run before committing changes.

.. code:: bash

    pre-commit install


Testing
-------

PyLumerical uses `pytest`_ for testing.

To run tests, first install the test requirements seen in the previous section, and then run the following command in the root directory of the repository:

.. code:: bash

    pytest --cov="<path_to_virtual_environment>\Lib\site-packages\ansys\api\lumerical" --cov="<pylumerical_repository>\tests\unit" --cov-report=html:coverage_report --verbose

Replace ``<path_to_virtual_environment>`` with the path to your virtual environment, and ``<pylumerical_repository>`` with the path to your local PyLumerical repository.

Documentation
-------------

PyLumerical uses reStructuredText and `Sphinx`_ for documentation.

Before building the documentation locally, first install the documentation requirements seen in the previous section. You don't need additional dependencies unless you want to build the examples and cheatsheet locally.

By default, PyLumerical disables local builds of the examples and cheatsheet.

To enable them, first install the following dependencies:

* **Examples**: PyLumerical requires `Pandoc <https://pandoc.org/installing.html>`_ to build the examples locally.
* **Cheatsheet**: PyLumerical requires `Quarto <https://quarto.org/docs/get-started/>`_  and a LaTeX distribution, such as `MiKTeX <https://miktex.org>`_, to build the cheatsheet locally.

After installing the dependencies, enable local builds of the examples and cheatsheet by setting the following environment variables:

* **Examples**: Set ``BUILD_PYLUMERICAL_EXAMPLES=TRUE`` to enable local builds of the examples.
* **Cheatsheet**: Set ``BUILD_PYLUMERICAL_CHEATSHEET=TRUE`` to enable local builds of the cheatsheet.

To build the documentation, navigate to the ``/doc`` directory and run:

.. tab-set::

    .. tab-item:: Windows

        .. code-block:: bash

            .\\make.bat html

    .. tab-item:: Linux

        .. code-block:: bash

            make html


The documentation is under the ``doc/_build/html`` directory.

You can also clean the documentation build directory by running:

.. tab-set::

    .. tab-item:: Windows

        .. code-block:: bash

            .\\make.bat clean

    .. tab-item:: Linux

        .. code-block:: bash

            make clean


.. LINKS AND REFERENCES

.. _pre-commit: https://pre-commit.com/
.. _PyAnsys Developer's guide: https://dev.docs.pyansys.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/

