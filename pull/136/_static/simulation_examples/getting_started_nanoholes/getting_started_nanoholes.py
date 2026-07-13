# Import modules

from collections import OrderedDict

import matplotlib.pyplot as plt

import ansys.lumerical.core as lumapi

# --- Parameters ---
# Define parameters

filename = "Nanohole_array.fsp"

# Parameters related to the patterned film
periodicity = 400e-9  # 400 nm periodic array
film_thickness = 100e-9
hole_radius = 100e-9  # radius of the nanoholes
nx = ny = 3  # Number of nanoholes

# Parameters for the substrate
substrate_thickness = 1e-6
substrate_span = 1.2e-6

# FDTD region and mesh
fdtd_z_span = 1e-6  # Ensure span is large enough to capture both T, R monitors
transmission_z = 0.4e-6  # z position of top "T" monitor
reflection_z = -0.2e-6  # z position of bottom "R" monitor
dx = 0.01e-6  # mesh override resolution

# Source and wavelengths
source_z = 0.3e-6  # position of source
wavelength_start = 0.4e-6
wavelength_stop = 0.7e-6
# --- Parameters end ---

# --- Simulation setup ---
# Initialize session and build simulation objects. Set hide = True to hide the Lumerical GUI.

with lumapi.FDTD(hide=False) as fdtd:
    # Add the substrate
    fdtd.addrect(name="substrate", 
                 x_span=substrate_span, 
                 y_span=substrate_span, 
                 z_max=0, 
                 z_min=substrate_thickness, 
                 material="SiO2 (Glass) - Palik")

    # Add the gold film
    fdtd.addrect(name="film", 
                 x_span=substrate_span, 
                 y_span=substrate_span, 
                 z_max=film_thickness, 
                 z_min=0, 
                 material="Au (Gold) - CRC")

    # Add the nanohole array in the gold layer
    # For this, we use the built-in rectangular photonic crystal object from the library
    pc_props = {
        "name": "nanoholes",
        "material": "etch",
        "radius": hole_radius,
        "z": film_thickness / 2,
        "z span": film_thickness,
        "nx": nx,
        "ny": ny,
        "ax": periodicity,
        "ay": periodicity,
    }
    fdtd.addobject("rect_pc")
    fdtd.set(pc_props)

    # Set up the simulation region
    fdtd_geometry_props = {"x": 0, "x span": periodicity, "y": 0, "y span": periodicity, "z": 0, "z span": fdtd_z_span}
    # Use symmetric boundary conditions in x and y and steep angle PML profile in z
    fdtd_boundary_props = {
        "allow symmetry on all boundaries": 1,
        "x min bc": "anti-symmetric",
        "x max bc": "anti-symmetric",
        "y min bc": "symmetric",
        "y max bc": "symmetric",
        "z min bc": "PML",
        "z max bc": "PML",
        "pml profile": 3,
    }
    # Combine properties settings into one dictionary
    fdtd_props = OrderedDict({**fdtd_geometry_props, **fdtd_boundary_props})
    fdtd.addfdtd(properties=fdtd_props)

    # Add a mesh override region around the holes
    fdtd.addmesh(dx=dx, dy=dx, dz=dx, based_on_a_structure=1, structure="circle")

    # Add plane wave source
    fdtd.addplane(injection_axis="z-axis", direction="backward", x_span=substrate_span, y_span=substrate_span, z=source_z)
    fdtd.setglobalsource("wavelength start", wavelength_start)
    fdtd.setglobalsource("wavelength stop", wavelength_stop)

    # Set up frequency domain monitors to measure R and T
    # First, set global monitor properties
    # Source limits will be used by default to define min/max wavelength
    fdtd.setglobalmonitor("frequency points", 50)
    # Now add the monitors
    fdtd.adddftmonitor(name="T_monitor", 
                       monitor_type="2D Z-normal", 
                       x_span=substrate_span, 
                       y_span=substrate_span, 
                       z=transmission_z)
    fdtd.adddftmonitor(name="R_monitor", 
                       monitor_type="2D Z-normal", 
                       x_span=substrate_span, 
                       y_span=substrate_span, 
                       z=reflection_z)

    # zoom CAD view around simulation region
    fdtd.select("FDTD")
    fdtd.setview("extent")

    fdtd.save(filename)
    print("File saved to folder as: " + filename)

    # Open the file and run the simulation! Visualize the T/R spectrum.
# --- Simulation setup end --


# --- Run ---
with lumapi.FDTD(filename, hide=True) as fdtd:
    print("Starting simulation now...")
    fdtd.run()
    print("Run completed.")

    # Retrieve results
    T = fdtd.getresult("T_monitor", "T")  # Returns lumerical dataset T vs lambda/f
    R = fdtd.getresult("R_monitor", "T")

    # Visualize using matplotlib
    fig, ax = plt.subplots()
    ax.plot(T["lambda"] * 1e9, T["T"], label="Transmission")
    ax.plot(R["lambda"] * 1e9, -1 * R["T"], label="Reflection")  # light traveling along -z so T result is negative
    ax.set_xlabel("Wavelength [nm]")
    ax.set_ylabel("T/R")
    ax.legend()
    plt.show()
# --- Run end ---