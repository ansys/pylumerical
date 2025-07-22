import pytest
import ansys.lumerical.core.autodiscovery as autodiscovery
import ansys.api.lumerical.lumapi as lumapi

base_install_path = autodiscovery.locate_lumerical_install()

lumapi.InteropPaths.setLumericalInstallPath(base_install_path)
