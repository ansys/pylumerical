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

        .. tab-item:: POSIX
        
            .. code-block:: bash

                source .venv/bin/activate

        .. tab-item:: Command Line

            .. code-block:: bash

                .venv\\Scripts\\activate.bat

        .. tab-item:: Windows Powershell

            .. code-block:: bash

                .venv\\Scripts\\Activate.ps1

#. Install PyLumerical in editable mode:

   .. code:: bash

      python -m pip install --e .

#. Install additional requirements as needed for build, documentation, and tests:

   .. code:: bash

      python -m pip install -U pip setuptools tox
      python -m pip install -r requirements_build.txt
      python -m pip install ansys-lumerical-core[tests]
      python -m pip install ansys-lumerical-core[doc]
      
#. Finally, verify your development installation by running:

   .. code:: bash

      tox

How to test
------------

This project takes advantage of `tox`_. This tool allows to automate common
development tasks (similar to Makefile) but it's oriented towards Python
development.

Using tox
^^^^^^^^^^

As Makefile has rules, `tox`_ has environments. In fact, the tool creates its
own virtual environment to isolate the test files from the project in
order to guarantee the project's integrity. 

Environment commands for tox:

- **tox -e style**: checks for coding style quality.
- **tox -e py**: checks for unit tests.
- **tox -e py-coverage**: checks for unit testing and code coverage.
- **tox -e doc**: checks for documentation building process.


Raw testing
^^^^^^^^^^^

.. vale off

If required, you can call the style commands (`black`_, `isort`_,
`flake8`_) or unit testing ones (`pytest`_) from the command line. However,
this doesn't guarantee that your project is being tested in an isolated
environment, which is the reason to consider using `tox`_.

.. vale on

Pre-commit
-----------

Style checks in PyLumerical is enforced using `pre-commit`_. You can install  `pre-commit`_ to check your code style prior to committing changes.

.. code:: bash

    python -m pip install pre-commit && pre-commit install


Documentation
-------------

For building documentation, you can either run the usual rules provided in the
`Sphinx`_ Makefile, such as:

.. code:: bash

    make -C doc/ html && open doc/html/index.html

However, the recommended way of checking documentation integrity is using:

.. code:: bash

    tox -e doc && open .tox/doc_out/index.html


Distributing
------------

If you would like to create either source or wheel files, start by installing
the building requirements and then executing the build module:

.. code:: bash

    python -m pip install -r requirements/requirements_build.txt
    python -m build
    python -m twine check dist/*


.. LINKS AND REFERENCES
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _pip: https://pypi.org/project/pip/
.. _pre-commit: https://pre-commit.com/
.. _PyAnsys Developer's guide: https://dev.docs.pyansys.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _tox: https://tox.wiki/
