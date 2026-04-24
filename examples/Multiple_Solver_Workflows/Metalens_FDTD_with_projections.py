# PyLumerical Metalens (FDTD)
#
# This example automates design and simulation of a metalens using Ansys Lumerical FDTD.
# A metalens is an array of pillars, also called unit cells or meta-atoms, that are arranged across a surface to create a macroscopic optical element. Each unit cell locally adjusts the phase of the light, and by arranging the unit cells across the surface, a global phase profile can be achieved. Typically, this phase profile is designed to act as a lens.
#
# In this example, we use Python to automate metalens design and simulation. We follow a standard approach of separately designing a target phase profile and a suitable library of unit cells under periodic boundary conditions. A target phase profile at a specific design wavelength must be provided; this can come from theory or an optimized phase profile from Zemax or another design process can be imported. The unit cell library is designed and simulated in Lumerical RCWA. Once the target phase profile and unit cell library are determined, we loop through each location on the phase profile and select the unit cell from the library that best matches the target phase at that location. The complete metalens is constructed in Lumerical FDTD using the Assembly Group object (https://optics.ansys.com/hc/en-us/articles/23889799301523-Assembly-Groups-Simulation-Objects).
# Please note that simulating large metalenses may require significant RAM; please check memory requirements prior to running Step 3 for full FDTD simulation.
#

# Part 0: Perform required imports and specify design parameters.
# Units are meters unless otherwise specified.

# +
# Import required modules

from collections import OrderedDict

import matplotlib.pyplot as plt  # Recommended, but only required for plotting
import numpy as np

import ansys.lumerical.core as lumapi

# +
# Global design parameters

# Constants for units
mm = 1e-3
um = 1e-6
nm = 1e-9
c = 3e8

target_wavelength = 550 * nm  # Specify the design wavelength. The unit cells will be most closely matched to the target at this wavelength.
polarization = "S"  # Returns S or P results; they are the same for symmetric unit cells at normal incidence

# +
# Unit cell specifications

period = 300 * nm  # Unit cell periodicity. This MUST be the same as the grid spacing of the target phase profile.
height = 800 * nm  # All pillars the same height
shape = "circle"  # Specify 'circle' or 'square'
min_feature_size = 30 * nm  # Optional; sets a minimum pillar / gap size for the unit cell library
num_pillars = 50  # Sets the number of unique pillar sizes in the library

# Set materials
# Use the exact spelling of a material from the Lumerical database.
pillar_material = "Si3N4 (Silicon Nitride) - Luke"  # Use the exact spelling of a material from the Lumerical database
substrate_material = "SiO2 (Glass) - Palik"

# Specify filename for unit cell simulations - a new file will be created
unit_cell_filename = "unit_cell_rcwa.fsp"

# +
# Target phase profile specifications

lens_radius = 10 * um  # The overall radius of the lens
assume_symmetry = True  # To save memory, we can work with a quarter circle at a time and bring it back to full lens at the end

# Specify phase profile type - see descriptions of three functions below
# Option 1: Spherical phase (specify desired focal length and wavelength)
# Option 2: Zemax Binary-2 phase (copy and paste optimized coefficients from Zemax)
type_lens = "spherical"  # Specify "spherical" or "Binary2"

# For spherical and cylindrical lenses - specify focal length. Not used for Binary2.
focal_length = 50 * um

# Copy parameters from Zemax for Binary2
norm_radius = 100 * mm  # Normalization radius
# Copy a list of the p^2 coefficients from Zemax
zemax_coeffs = [-2.279343664281709e006, -3.943219031309796e006, 8.648523491639540e009, -1.743623426550141e012]

# -

# Part 1: Create target phase mask

# +
# Define functions to generate target phase
# Here, R = X^2 + Y^2 is the radial coordinate


def get_spherical_phase(X, Y, focal_length, wavelength):
    # Specify a design wavelength and target focal length at that wavelength
    phase = (2 * np.pi / wavelength) * (focal_length - np.sqrt(X**2 + Y**2 + focal_length**2))
    phase = phase - np.amin(phase)  # remove constant offset
    phase = phase % (2 * np.pi)  # Take modulo 2pi
    return phase


def get_Binary2_phase(X, Y, norm_radius, zemax_coeffs):
    # Copy and paste Binary2 coefficients from Zemax; focusing behavior will be determined from those
    numterms = len(zemax_coeffs)
    R = np.sqrt(X ^ 2 + Y ^ 2)
    phase = R * 0
    for n in range(0, numterms):
        phase = phase + (zemax_coeffs(n) * (R / norm_radius) ** (2 * n))
    phase = phase - np.amin(phase)  # remove constant offset
    phase = phase % (2 * np.pi)  # Take modulo 2pi
    return phase


def circularize(phase_mask, assume_symmetry):  # Applies a circular mask to the phase.
    # If assume_symmetry is True, then we shift the center of the circle to the corner.
    mask_width = phase_mask.shape[0]
    mask_height = phase_mask.shape[1]
    if assume_symmetry:
        center = (0, 0)  # center is at index 0,0 - this is not spatial location
        mask_rad = min(mask_width, mask_height)
    else:
        center = (int(mask_width / 2), int(mask_height / 2))
        mask_rad = min(center)
    mask_grid = phase_mask * 0
    for n in range(0, len(mask_grid)):
        for m in range(0, len(mask_grid[n])):
            distance = np.sqrt((n - center[0]) ** 2 + (m - center[1]) ** 2)
            if distance <= mask_rad:
                mask_grid[n, m] = 1
    return phase_mask * mask_grid


# +
# Create phase mask grid

if assume_symmetry:  # Evaluate only a quarter map
    x = np.arange(0, lens_radius, period)
    y = np.arange(0, lens_radius, period)
else:
    x = np.arange(-lens_radius, lens_radius, period)
    y = np.arange(-lens_radius, lens_radius, period)

xx, yy = np.meshgrid(x, y)

# +
# Calculate and plot phase mask

# In this example, we are using the spherical phase function
if type_lens == "spherical":
    target_phase = get_spherical_phase(xx, yy, focal_length, target_wavelength)
    print("Using spherical phase profile with target f = " + str(focal_length / um) + " microns.")
elif type_lens == "Binary2":
    target_phase = get_binary2_phase(xx, yy, norm_radius, zemax_coeffs)
    print("Using Binary2-type phase profile.")
else:
    print("Target phase not specified - please specify the target phase map.")

target_phase_width = target_phase.shape[0]  # get size of array
target_phase_height = target_phase.shape[1]  # get size of array

plt.imshow(circularize(target_phase, assume_symmetry), extent=[0, period * target_phase_width / mm, 0, period * target_phase_height / mm])
plt.colorbar()
plt.title("Target Phase Mask")
plt.xlabel("x (mm)")
plt.ylabel("y (mm)")
plt.show(block=False)
plt.pause(5)


# -

# Part 2: Create simple unit cell library.
# Note 1: In this example, we use Lumerical RCWA for speed. However, it is also possible to use FDTD if desired.
# Note 2: We use a loop in Python to set up and run RCWA simulations for different pillar widths. It is also possible to set up sweeps using Lumerical's built-in Optimizations and Sweeps tools. To avoid continuously opening and closing instances of Lumerical, we initialize a single instance of Lumerical named 'rcwa' and rebuild geometry on each run.

# +
# create a single RCWA unit cell simulation


def single_RCWA(session_name, shape, radius, period, height, pillar_material, substrate_material, wavelength, theta, phi):
    """
    Runs a single RCWA simulation for a single geometric structure and set of illumination conditions.
    session_name: the name of an existing, open Lumerical FDTD instance.
    Geometry params:
    shape: The cross-sectional shape of the pillar, either 'circle' or 'square'
    radius: For circular pillar, the radius. For square pillars, the total pillar width is 2*radius
    period: The periodicity of the unit cell. Used to set the span of RCWA simulation region
    pillar_material: The name of the pillar material in Lumerical material database
    substrate_material: The name of the substrate material in the Lumerical material database
    Illumination params:
    wavelength: the simulation wavelength
    theta: the illumination angle theta, in degrees
    phi: the illumination angle phi, in degrees

    Returns: phase (in units of 0 to 2pi), amp
    """
    # First: check for obvious errors
    if 2 * radius > period:
        print("Pillar width exceeds unit cell periodicity! Please check radius and period settings.")

    # Initialize session: switch back to layout and clear existing geometry
    session_name.switchtolayout()
    session_name.deleteall()

    Lmax = np.amin(wavelength)  # Used to determine vertical span of simulation region

    # Set up objects

    # Substrate
    session_name.addrect(name="substrate", material=substrate_material, x=0, x_span=2 * period, y=0, y_span=2 * period, z_max=0)
    n_sub = session_name.getindex(substrate_material, c / wavelength)
    session_name.set("z min", -2 * Lmax / n_sub)

    # Pillar
    if shape == "circle":
        session_name.addcircle(name="pillar", material=pillar_material, x=0, y=0, radius=radius, z_min=0, z_max=height)
    if shape == "square":
        session_name.addrect(name="pillar", material=pillar_material, x=0, x_span=2 * radius, y=0, y_span=2 * radius, z_min=0, z_max=height)
    n_pillar = session_name.getindex(pillar_material, c / wavelength)

    # Set up session_name simulation object - general properties
    session_name.addrcwa(x=0, y=0, x_span=period, y_span=period, z_min=-0.5 * Lmax / n_sub, z_max=0.5 * Lmax / n_pillar + height)
    session_name.setnamed("RCWA", "report grating characterization", True)

    # Set the RCWA interface positions. The interface positions are set from the minimum and maximum z positions of the pillar object.
    # For documentation, see https://optics.ansys.com/hc/en-us/articles/12959229278611-RCWA-Solver-Simulation-Object
    session_name.setnamed("RCWA", "interface position", "reference")
    interfaces = [["::model::pillar", "max", 1], ["::model::pillar", "min", 1]]
    session_name.setnamed("RCWA", "interface reference positions", interfaces)

    # Set RCWA excitation properties
    session_name.setnamed("RCWA", "use wavelength spacing", True)
    session_name.setnamed("RCWA", "wavelength center", wavelength)
    session_name.setnamed("RCWA", "wavelength span", 0)
    session_name.setnamed("RCWA", "frequency points", 1)
    # By default, a single incident angle is used; a table or list can be used later instead
    session_name.setnamed("RCWA", "angle theta", 0)
    session_name.setnamed("RCWA", "angle phi", 0)

    # Save and run
    session_name.save(unit_cell_filename)  # this file will be overwritten on each run
    session_name.run()  # Run single RCWA simulation

    # Retrieve results
    gc = session_name.getresult("RCWA", "grating_characterization")  # result is returned as Python dict
    if polarization == "S":
        T_results = gc["Tss"]  # Result returned vs. theta/phi, orders n and m
    else:
        T_results = gc["Tpp"]

    # Get m and n indices of 0th order
    m = np.where(gc["m"] == 0)[0]
    n = np.where(gc["n"] == 0)[0]
    S0 = T_results[0, 0, n, m]
    phase = np.angle(S0) + np.pi  # returned in radians in the range (-pi, pi]
    amp = np.abs(S0) ** 2

    return phase[0], amp[0]


# +
# Test the above function - run a single rcwa simulation and print results

with lumapi.FDTD(hide=False) as rcwa:
    testphase, testamp = single_RCWA(rcwa, "square", 120e-9, period, height, pillar_material, substrate_material, target_wavelength, 0, 0)
    print("Phase: " + str(testphase * 180 / np.pi) + " degrees")
    print("Amplitude: " + str(testamp))

# +
# Now run a sweep over a range of pillar widths

sweep_res = 10  # Number of points in sweep
min_pillar = min_feature_size
max_pillar = 0.5 * period - min_feature_size
pillar_radius = np.linspace(min_pillar, max_pillar, sweep_res)  # list of pillar radius (half total width) to sweep

# Initialize arrays to hold results
phase_results = pillar_radius * 0
amp_results = pillar_radius * 0

with lumapi.FDTD(hide=False) as rcwa:
    for n in range(0, sweep_res):
        radius = pillar_radius[n]
        phase_results[n], amp_results[n] = single_RCWA(
            rcwa, "circle", radius, period, height, pillar_material, substrate_material, target_wavelength, 0, 0
        )

    # Unwrap and shift phase so smallest pillar is at 0 phase shift
    phase_results = np.unwrap(phase_results)
    phase_results = phase_results - phase_results[0]

# +
# Plot results

plt.subplot(2, 1, 1)
plt.plot(pillar_radius / nm, phase_results, "r")
plt.xlabel("Pillar Radius (half total width)")
plt.ylabel("Phase (radians)")

plt.subplot(2, 1, 2)
plt.plot(pillar_radius / nm, amp_results, "r")
plt.xlabel("Pillar Radius (half total width)")
plt.ylabel("Amplitude")

plt.show(block=False)
plt.pause(5)

# -

# Part 3: Obtain the radius vs. position to match the target phase profile as closely as possible.

# +
# Phase vs. radius table to use for mapping

radius_array = target_phase * 0  # initialize array

for n in range(0, len(target_phase)):
    for m in range(0, len(target_phase[n])):
        difference = np.abs(target_phase[n, m] - phase_results)
        smallest_difference_index = difference.argmin()  # Find the index of the closest phase
        closest_radius = pillar_radius[smallest_difference_index]  # Choose pillar corresponding to that closest index
        radius_array[n, m] = closest_radius

# Apply the circular mask
radius_array = circularize(radius_array, assume_symmetry)

# +
# Plot the design

plt.imshow(radius_array / nm, extent=[0, period * target_phase_width / mm, 0, period * target_phase_height / mm])
plt.colorbar()
plt.title("Radius Array")
plt.xlabel("x (mm)")
plt.ylabel("y (mm)")
plt.show(block=False)
plt.pause(5)
# -


# Part 3: Build full metalens in FDTD and analyze results. We use the Assembly Group Object for efficiency.
#
# Note 1: set "pillar rendering detail" to 0 to speed up rendering in viewports.
# The pillars will appear polygonal in the viewports but it does not change anything in the simulation, it is purely for speeding up rendering in the viewports of the UI. It will not allow a setting of larger than 0.5 (normally 1 is maximum).
#
# Note 2: When using assembly group, structure is not displayed in the viewport if the number of objects exceeds 32000. An index monitor can be used to visualize structures. To hide the FDTD GUI entirely, enter the flag "hide = True".

# +
# Set options
pillar_rendering_detail = 0

# Set filename for saving
full_lens_filename = "FDTD_metalens_target_" + str(target_wavelength / nm) + "nm.fsp"

# -


# +
# Initialize session and build simulation objects.
# We utilize the Assembly Group to build the metalens structure.

with lumapi.FDTD(hide=False) as fdtd:
    # Substrate rectangle
    fdtd.addrect(name="substrate", material=substrate_material, x_span=3 * lens_radius, y_span=3 * lens_radius, z_max=0, z_min=-2 * target_wavelength)

    # Metalens pillars - utilizes assembly group
    # Faster, more efficient, less memory required
    # Structure is not displayed if number of objects exceeds 32000

    fdtd.addassemblygroup(name="metalens")
    fdtd.addcircle()
    fdtd.addtogroup("metalens")
    fdtd.setnamed("metalens", "parameters", ["x", "y", "radius"])

    # create mapping matrix: length is total number of pillars by 3
    count = 0  # keep track of index

    print("Building metalens objects...")
    if assume_symmetry:
        # Bring back to 4-fold circle if symmetry is used
        mapping = np.zeros((4 * len(x) * len(y), 3))
        for n in range(0, len(target_phase)):
            for m in range(0, len(target_phase[n])):
                if radius_array[n, m] > 0:
                    mapping[count, :] = [xx[n, m], yy[n, m], radius_array[n, m]]
                    count = count + 1
                    mapping[count, :] = [xx[n, m], -yy[n, m], radius_array[n, m]]
                    count = count + 1
                    mapping[count, :] = [-xx[n, m], yy[n, m], radius_array[n, m]]
                    count = count + 1
                    mapping[count, :] = [-xx[n, m], -yy[n, m], radius_array[n, m]]
                    count = count + 1
                else:
                    count = count + 4
    else:
        # No symmetry - build array exactly
        mapping = np.zeros((len(x) * len(y), 3))
        for n in range(0, len(target_phase)):
            for m in range(0, len(target_phase[n])):
                if radius_array[n, m] > 0:
                    mapping[count, :] = [xx[n, m], yy[n, m], radius_array[n, m]]
                count = count + 1

    fdtd.setnamed("metalens", "mapping", np.transpose(mapping))
    fdtd.select("metalens::circle")
    # Apply properties to these metalens circles
    fdtd.set("material", pillar_material)
    fdtd.set("z min", 0)
    fdtd.set("z max", height)
    fdtd.set("detail", np.amin([0, pillar_rendering_detail]))
    print("Metalens built. Adding remaining simulation objects and saving to file: " + full_lens_filename)

    # Add FDTD region, source, and monitors

    # FDTD region
    buffer_space = 1.5 * target_wavelength  # amount of free space around metalens structure
    fdtd_geometry_props = {
        "x": 0,
        "x span": 2 * (lens_radius + buffer_space),
        "y": 0,
        "y span": 2 * (lens_radius + buffer_space),
        "z min": -buffer_space,
        "z max": height + buffer_space,
    }
    fdtd_boundary_props = {
        "x min bc": "Anti-Symmetric",
        "x max bc": "PML",
        "y min bc": "Symmetric",
        "y max bc": "PML",
        "z min bc": "PML",
        "z max bc": "PML",
    }
    # Combine properties settings into one dictionary
    fdtd_props = OrderedDict({**fdtd_geometry_props, **fdtd_boundary_props})
    fdtd.addfdtd(properties=fdtd_props)

    # Plane wave source
    source_geometry_props = {
        "injection axis": "z",
        "direction": "forward",
        "x": 0,
        "x span": 3 * lens_radius,
        "y": 0,
        "y span": 3 * lens_radius,
        "z": -target_wavelength,
    }
    source_frequency_props = {"override global source settings": 1, "wavelength start": 0.4e-6, "wavelength stop": 0.9e-6}
    source_props = OrderedDict({**source_geometry_props, **source_frequency_props})
    fdtd.addplane(properties=source_props)

    # Add monitors (top-down and side views)
    # For the top-down monitor, we will use results to calculate far-field projections.
    # Therefore, we collect results at one frequency point.
    monitor_geometry_props = {
        "name": "field_above",
        "monitor type": "2D Z-normal",
        "x": 0,
        "x span": 3 * lens_radius,
        "y": 0,
        "y span": 3 * lens_radius,
        "z": height + buffer_space / 2,
    }
    monitor_frequency_props = {
        "override global monitor settings": 1,
        "use source limits": 0,
        "minimum wavelength": target_wavelength,
        "maximum wavelength": target_wavelength,
        "frequency points": 1,
    }
    monitor_props = OrderedDict({**monitor_geometry_props, **monitor_frequency_props})
    fdtd.adddftmonitor(properties=monitor_props)
    # In the side monitor, we collect results using the global frequency settings.
    # By default these settings are 5 wavelength points set to match the min and max source frequency.
    monitor_props = {
        "name": "side_view",
        "monitor type": "2D Y-normal",
        "x": 0,
        "x span": 3 * lens_radius,
        "y": 0,
        "z min": -buffer_space,
        "z max": height + buffer_space,
    }
    fdtd.adddftmonitor(properties=monitor_props)

    # Zoom CAD view around the simulation region
    fdtd.select("metalens")
    fdtd.setview("extent")

    # Save to file
    fdtd.save(full_lens_filename)
    print("File saved, complete.")

# +
# Memory check

use_GPU = False

with lumapi.FDTD(full_lens_filename, hide=True) as fdtd:
    if use_GPU == True:
        memory_check = fdtd.runsystemcheck("FDTD", "GPU")
        max_memory = memory_check["Approximate_GPU_Memory_Requirements"]["Maximum_Bytes"] * 1e-9  # convert to Gb
        min_memory = memory_check["Approximate_GPU_Memory_Requirements"]["Minimum_Bytes"] * 1e-9  # convert to Gb
        print("GPU VRAM estimate is " + str(round(min_memory, 2)) + " Gb (min) to " + str(round(max_memory, 2)) + " Gb (max).")
    else:
        memory_check = fdtd.runsystemcheck("FDTD", "CPU")
        recommended_memory = memory_check["Memory_Recommended_Bytes"] * 1e-9  # convert to Gb
        alerts = memory_check["Approximate_Memory_Requirements"]["Alert"]
        print("Recommended CPU RAM: " + str(round(recommended_memory, 2)) + " Gb.")
        print("Alerts:  " + alerts)

# +
# Configure resources and run simulations

with lumapi.FDTD(full_lens_filename, hide=True) as fdtd:
    # Add CPU/GPU resources
    cpuRes = fdtd.addresource("FDTD")
    fdtd.setresource("FDTD", cpuRes, "device type", "CPU")
    fdtd.setresource("FDTD", cpuRes, "name", "PyLum CPU")
    gpuRes = fdtd.addresource("FDTD")
    fdtd.setresource("FDTD", gpuRes, "device type", "GPU")
    fdtd.setresource("FDTD", gpuRes, "name", "PyLum GPU")
    fdtd.save(full_lens_filename)


# -

with lumapi.FDTD(full_lens_filename, hide=False) as fdtd:
    if use_GPU == True:
        print("Running on GPU, starting now.")
        fdtd.run("FDTD", "GPU", "PyLum GPU")
        fdtd.save(full_lens_filename)
        print("File run and saved.")
    else:
        print("Running on CPU, starting now.")
        fdtd.run("FDTD", "CPU", "PyLum CPU")
        fdtd.save(full_lens_filename)
        print("File run and saved.")


# +
# Retrieve and plot results from monitors

with lumapi.FDTD(full_lens_filename, hide=True) as fdtd:
    E_above = fdtd.getresult("field_above", "E")
    x, y = E_above["x"], E_above["y"]
    z = E_above["z"][0][0]
    Ex, Ey, Ez = E_above["E"][:, :, 0, 0, 0], E_above["E"][:, :, 0, 0, 1], E_above["E"][:, :, 0, 0, 2]

    eFieldAmplitude_top = np.abs(Ex) ** 2 + np.abs(Ey) ** 2 + np.abs(Ez) ** 2
    X, Y = np.meshgrid(x, y)  # Create meshgrid

    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    ax1.contourf(X, Y, eFieldAmplitude_top)
    ax1.set_aspect("equal")
    ax1.set_title("E Field at z = " + str(np.round(z * 10e6, decimals=2)) + " microns")

    E_side = fdtd.getresult("side_view", "E")
    x_side, y_side, z_side = E_side["x"], E_side["y"], E_side["z"]
    Ex, Ey, Ez = E_side["E"][:, 0, :, 0, 0], E_side["E"][:, 0, :, 0, 0], E_side["E"][:, 0, :, 0, 0]

    eFieldAmplitude_side = np.abs(Ex) ** 2 + np.abs(Ey) ** 2 + np.abs(Ez) ** 2
    X, Z = np.meshgrid(x_side, z_side)  # Create meshgrid

    ax2.contourf(X, Z, np.transpose(eFieldAmplitude_side))
    ax2.set_title("E Field, Side View")

    plt.show(block=False)
    plt.pause(5)
# -


# +
# Plot far-field projections out to the focal point
# Plotting a slice along z is usually a fast calculation

with lumapi.FDTD(full_lens_filename, hide=True) as fdtd:
    x = 0
    y = 0
    z_res = 100  # number of z points for the projection
    z_list = np.linspace(0, 1.5 * focal_length, z_res)
    proj_index = 1.0  # the refractive index of the medium you are projecting through; n = 1 for air

    # Plot a slice along z - this is a relatively fast calculation
    proj = np.zeros(z_res)

    # The second to last param of "1" here refers to using the first (and only, in this case) frequency point collected by the monitor
    proj = fdtd.farfieldexact3d("field_above", x, y, z_list, 1, proj_index)

# -

proj_Ex, proj_Ey, proj_Ez = proj[0, 0, :, 0], proj[0, 0, :, 1], proj[0, 0, :, 2]
proj_intensity = np.abs(proj_Ex) ** 2 + np.abs(proj_Ey) ** 2 + np.abs(proj_Ez) ** 2
plt.plot(z_list / um, proj_intensity, "k-")
plt.xlabel("Z position (microns)")
plt.ylabel("E field intensity")
plt.title("Projected Field Intensity (a.u.), slice along z")
plt.show(block=False)
plt.pause(5)

# +
# Now, plot a cross-sectional image of the xz plane
# Note that this calculation may take some time if your field data has high resolution

with lumapi.FDTD(full_lens_filename, hide=True) as fdtd:
    x = fdtd.getdata("field_above", "x")
    x_res = 100
    x_list = np.linspace(min(x), max(x), x_res)
    y = 0
    z_res = 50  # number of z points for the projection
    z_list = np.linspace(0, 1.5 * focal_length, z_res)

    proj_image = fdtd.farfieldexact3d("field_above", x_list, y, z_list, 1, proj_index)

# +
proj_Ex, proj_Ey, proj_Ez = proj_image[:, 0, :, 0], proj_image[:, 0, :, 1], proj_image[:, 0, :, 2]
proj_intensity = np.abs(proj_Ex) ** 2 + np.abs(proj_Ey) ** 2 + np.abs(proj_Ez) ** 2

# Note: We generally recommend plotting field data from Lumerical using contourf since data from monitors may be nonuniformly sampled
# Here, we have manually specified the projection points using linspace so imshow is appropriate
plt.imshow(proj_intensity, extent=[min(z_list) / um, max(z_list) / um, min(x_list) / um, max(x_list) / um])
plt.xlabel("X (microns)")
plt.ylabel("Z (microns)")
plt.title("Projected Field Intensity (a.u.), x-z image")
plt.show(block=False)
plt.pause(5)
# -
