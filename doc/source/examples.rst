Examples
########
These examples demonstrate the behavior and usage of PyLumerical.

.. code-block:: python
    :linenos:

    import ansys.lumerical.core as lumapi
    # Launch Lumerical FDTD
    fdtd = lumapi.FDTD()
    x = fdtd.linspace(0, 1, 101)
    y = fdtd.sin(2 * 3.1415 * x)
    fdtd.plot(x, y)

.. Provide links to the files in doc/source/examples below: