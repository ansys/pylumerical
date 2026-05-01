# # Thermal Waveguide Tuner (HEAT)
#
# Getting started example for HEAT simulation with PyLumerical.
# Calculates the temperature profile for a thermal waveguide tuner.
# Prerequisites: Valid HEAT license is required.

import matplotlib.pyplot as plt
import numpy as np

import ansys.lumerical.core as lumapi

with lumapi.DEVICE() as device:
    # Create materials
    device.addmodelmaterial({"name": "Silicon"})
    device.addmaterialproperties("HT", "Si (Silicon)")

    device.addmodelmaterial({"name": "Aluminium"})
    device.addmaterialproperties("HT", "Al (Aluminium) - CRC")

    device.addmodelmaterial({"name": "SiO2"})
    device.addmaterialproperties("HT", "SiO2 (Glass) - Sze")

    device.addmodelmaterial({"name": "Air"})
    device.addmaterialproperties("HT", "Air")

    # Create geometry
    device.addrect({"name": "substrate", "x": 0, "x span": 0.45e-6, "y": 0.11e-6, "y span": 0.22e-6, "z": 0, "z span": 1e-6, "material": "Silicon"})
    device.addrect({"name": "waveguide", "x": 0, "x span": 100e-6, "y": -21e-6, "y span": 38e-6, "z": 0, "z span": 1e-6, "material": "Silicon"})
    device.addrect({"name": "oxide", "x": 0, "x span": 100e-6, "y": 4e-6, "y span": 12e-6, "z": 0, "z span": 1e-6, "material": "SiO2"})
    device.addrect({"name": "air", "x": 0, "x span": 100e-6, "y": 7.21e-6, "y span": 5.58e-6, "z": 0, "z span": 1e-6, "material": "Air"})
    device.addrect({"name": "wire", "x": 0, "x span": 2e-6, "y": 2.32e-6, "y span": 0.2e-6, "z": 0, "z span": 1e-6, "material": "Aluminium"})

    # Set simulation region
    device.select("simulation region")  # Simulation region named "simulation region" is included in new simulation by default
    device.set({"dimension": "2D Z-Normal", "x": 0, "x span": 80e-6, "y": 0, "y span": 18e-6, "z": 0})

    # Add HEAT solver object
    device.addheatsolver({"norm length": 200e-6})

    # Add boundary conditions
    device.addtemperaturebc("HEAT")
    device.set({"temperature": 300, "surface type": "simulation region", "y min": True})

    device.addconvectionbc("HEAT")
    device.set({"h convection": 10, "surface type": "material:material", "material 1": "SiO2", "material 2": "Air"})

    # Add heat sources
    device.adduniformheat(
        {"geometry type": "volume", "volume type": "solid", "volume solid": "wire", "use solver norm length": True, "total power": 0.02}
    )

    # Add monitors
    device.addtemperaturemonitor(
        "HEAT", {"name": "temperature monitor", "monitor type": "2D z-normal", "x": 0, "x span": 20e-6, "y min": -5e-6, "y max": 4.42e-6, "z": 0}
    )

    # Run simulation
    device.save("thermal_tuner.ldev")
    device.run("HEAT")

    # Visualize results
    results = device.getresult("HEAT::temperature monitor", "temperature")

    # HEAT results are returned in an unstructured dataset, need to be converted to a rectilinear grid for pyplot
    vertices = device.getdata("HEAT::temperature monitor", "temperature", "vertices")
    elements = device.getdata("HEAT::temperature monitor", "temperature", "elements")
    temperature_unstructured = results["T"]

    x = np.linspace(-10e-6, 10e-6, 1000)
    y = np.linspace(-5e-6, 4.42e-6, 1000)

    temperature = device.interptri(elements, vertices[:, :2], temperature_unstructured, x, y)

    # Plot temperature profile
    im = plt.pcolormesh(x * 1e6, y * 1e6, temperature.T, shading="nearest")
    cbar = plt.colorbar(im)
    cbar.set_label("Temperature (K)")
    plt.xlabel("x (um)")
    plt.ylabel("y (um)")
    plt.show()
