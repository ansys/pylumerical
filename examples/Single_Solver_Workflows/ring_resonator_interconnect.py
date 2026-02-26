# # Simple Ring Resonator (INTERCONNECT)
#
# Getting started example for INTERCONNECT simulation with PyLumerical.
# Calculates the transmission spectrum of a ring resonator with 50 um radius.
# Prerequisites: Valid INTERCONNECT license is required.

import matplotlib.pyplot as plt
import numpy as np

import ansys.lumerical.core as lumapi

# +
# Define ring properties
radius = 50e-6  # in m
coupling_coefficient = 0.05
effective_index = 2.8
group_index = 3.4
loss = 300  # in dB/m

# Define analysis properties
center_frequency = 193.1e12  # in Hz
frequency_range = 1e12  # in Hz
num_points = 10000
# -

# Build and run simulation in INTERCONNECT
with lumapi.INTERCONNECT() as intc:  # Open INTERCONNECT
    # Add circuit elements and set properties
    intc.addelement("Waveguide Coupler", {"name": "Add Coupler", "coupling coefficient 1": coupling_coefficient})

    intc.addelement("Waveguide Coupler", {"name": "Drop Coupler", "coupling coefficient 1": coupling_coefficient})

    intc.addelement(
        "Straight Waveguide",
        {"name": "Waveguide 1", "length": np.pi * radius, "loss 1": loss, "effective index 1": effective_index, "group index 1": group_index},
    )

    intc.addelement(
        "Straight Waveguide",
        {"name": "Waveguide 2", "length": np.pi * radius, "loss 1": loss, "effective index 1": effective_index, "group index 1": group_index},
    )

    # Connect circuit elements
    intc.connect("Add Coupler", "port 4", "Waveguide 1", "port 1")
    intc.connect("Add Coupler", "port 2", "Waveguide 2", "port 2")
    intc.connect("Drop Coupler", "port 3", "Waveguide 1", "port 2")
    intc.connect("Drop Coupler", "port 1", "Waveguide 2", "port 1")

    # Set up Optical Network Analyzer
    intc.addelement(
        "Optical Network Analyzer",
        {"name": "ONA", "center frequency": center_frequency, "frequency range": frequency_range, "number of points": num_points},
    )

    # Connect ONA to circuit input and output
    intc.connect("ONA", "output", "Add Coupler", "port 1")
    intc.connect("ONA", "input 1", "Add Coupler", "port 3")

    # Run simulation
    intc.run()

    # Visualize ring transmission results
    results = intc.getresult("ONA", "input 1/mode 1/transmission")  # Get transmission from ONA
    transmission = results["TE transmission"]
    wavelength = results["wavelength"]

    # Plot transmission
    plt.plot(wavelength * 1e6, np.abs(transmission) ** 2)  # Plot power transmission
    plt.xlabel("Wavelength (um)")
    plt.ylabel("Transmission")
    plt.show()
