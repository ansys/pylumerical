Autodiscovery
=============

PyLumerical requires Lumerical |supported_lum_release| or later to run. The autodiscovery function first attempts to find the installation location using the following methods:

1. **Environment variable**: PyLumerical checks the ``LUMERICAL_HOME`` environment variable for the installation path. If found, this path is used.

2. **Windows registry**: On Windows, PyLumerical checks the registry for the installation path of Lumerical products.

3. **Default installation paths**: If the registry lookup fails, or if you are using Linux, PyLumerical checks the default installation paths:
    - On Windows, with the Lumerical standalone installer: ``C:\Program Files\Lumerical\``
    - On Windows, with the Ansys automated installer: ``C:\Program Files\Ansys Inc\``
    - On Linux, with the Lumerical standalone installer: ``/opt/lumerical/``
    - On Linux, with the Ansys automated installer: ``~/Ansys/ansys_inc/``

When PyLumerical finds an installation path, it configures the interop path. If bundled ``lumopt2`` is present, PyLumerical enables
``import lumopt2`` and ``import ansys.lumerical.core.lumopt2`` directly without exposing unrelated modules from ``<install>/api/python``.

If PyLumerical can't find the installation path automatically, it returns a warning.
Set ``LUMERICAL_HOME`` before import and start a new Python session. Manual ``sys.path`` overrides for ``lumopt2`` are unsupported.

The autodiscovery helpers below run automatically when you import PyLumerical:

.. autosummary::
    :toctree: _autosummary

    ansys.lumerical.core.autodiscovery.locate_lumerical_install
    ansys.lumerical.core.autodiscovery.get_lumerical_api_python_path
