Examples
========

Examples source files for PyLumerical are .py files. The PyLumerical documentation infrastructure converts these .py source files into .rst files for display on the documentation site, by first converting them into Jupyter Notebooks using `Jupytext <https://jupytext.readthedocs.io/en/latest/>`_, and then converting the notebooks into .rst files using `nbsphinx <https://nbsphinx.readthedocs.io/en/latest/>`_.

Formatting
----------

Example files must be compliant with `PEP8 <https://peps.python.org/pep-0008/>`_ guidelines, as listed on the PyAnsys Developer's `guide <https://dev.docs.pyansys.com/how-to/documenting.html#examples>`_.

PyLumerical examples uses the "Light" format for jupytext conversion. To write comment cells into your source file, follow the formatting guidelines listed in the `Jupytext documentation <https://jupytext.readthedocs.io/en/latest/formats-scripts.html>`_.

Always ensure that your example files run without errors, and are properly formatted prior to submitting a pull request.

The documentation build process currently not automatically execute the examples, as such, no outputs are displayed in the resulting documentation pages.

You can test your examples locally by running them as scripts, and you can test that the documentation formatting is correct by locally building the documentation. See the `contributing section <../doc/source/contributing.rst>`_ for more information.
