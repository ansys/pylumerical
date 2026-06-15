## Contains templates for the documentation build

- An auto summary template following ansys-sphinx-theme 1.7.2 is used
    - The ansys-sphinx-theme template doesn't apply to non-html builds (latex/linkcheck), which makes sphinx fall back to the default and tries to document `__init__`, when it's overridden in the Ansys theme.
    - The `__init__` documentation causes errors for PyLumerical, because some of the docstrings are empty or malformed because those aren't meant to be shown/documented anyways.