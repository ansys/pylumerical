Autodiscovery
=============

.. TO-DO: Variablize the supported product version here

PyLumerical requires Lumerical products version 2022 R1 or later to run. The autodiscovery function first attempts to find the installation location using the following methods:

1. **Windows registry**: On Windows, PyLumerical checks the registry for the installation path of Lumerical products.

2. **Default installation paths**: If the registry lookup fails, or if you are using Linux, PyLumerical checks the default installation paths:
    - On Windows, with the Lumerical standalone installer: ``C:\Program Files\Lumerical\``
    - On Windows, with the Ansys automated installer: ``C:\Program Files\ANSYS Inc\ANSYS Optics\``
    - On Linux, with the Lumerical standalone installer: ``/opt/Lumerical/``
    - On Linux, with the Ansys automated installer: ``~/Ansys/ansys_inc/``

If PyLumerical can't find the installation path automatically, it returns a warning, and you can set the path manually.

The autodiscovery function below is automatically ran when you import PyLumerical:

.. autosummary:: 
    :toctree: _autosummary

    ansys.lumerical.core.autodiscovery.locate_lumerical_install