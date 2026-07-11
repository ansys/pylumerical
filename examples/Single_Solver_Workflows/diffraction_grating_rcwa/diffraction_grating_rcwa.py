# # Diffraction Grating (RCWA)
#
# This example simulates a simple diffraction grating using RCWA.
#
# In Part 1, we set up the structures. We define a 1D trapezoidal blazed grating (commonly used in AR/VR applications). 
# The grating is parameterized by its periodicity, fill factor, top width, and depth.
# In Part 2, we use RCWA to calculate the complex transmission/reflection of the grating. 
# In Part 3, we plot the results.
#
# Prerequisites: Valid FDTD license is required. 

# Perform required imports

# +
import os,sys
import ansys.lumerical.core as lumapi
import numpy as np
from collections import OrderedDict
import itertools

import matplotlib.pyplot as plt # Only required for plotting
# -

# ## Part 1: Set up structures and simulation objects. 

# +
# Define parameters

# Set filename for saving and loading
filename = '1D_diffraction_grating.fsp'

# Units
um = 1e-6
nm = 1e-9

# Grating parameters
period_x = 0.600*um # Period (pitch) of the grating in x direction, 1D grating
fill_factor = 0.5
depth  = 0.40*um
top_factor = 0.3 # The top width of the grating tooth as a factor of the bottom width, for a trapezoidal profile. Set to 0 for rectangular profile.
num_teeth = 5 # Number of grating teeth to create; only one is needed for periodic boundary conditions

# Base/ substrate parameters
base_x = 1.5*period_x*num_teeth # The x span of the base/substrate 
base_y = 3*period_x
base_z = 5*um # Typically we inject light into the substrate/base and assume it is infinitely thick compared to the teeth

# Set materials 
n_grat = 1.565 # Refractive index of the grating material, simple non-dispersive material
n_base = 1.565 # Refractive index of the base material, simple non-dispersive material

# Define wavelengths of interest
wl_min = 350*nm
wl_max = 800*nm

# Define angles of interest
theta_min = 0
theta_max = 90
phi_min = 0
phi_max = 360

# Simulation parameters
sim_x_span = period_x # The x span of the simulation region, set to one period for periodic boundary conditions
sim_y_span = period_x # The y span of the simulation region; here the grating is uniform in y, so this can be made thinner if desired
z_buffer = wl_min # A buffer region above and below the structure to ensure the simulation region is large enough to avoid boundary effects
sim_z_max = depth + z_buffer # Good practice to make sure the simulation region is at least one wavelength larger than the structure
sim_z_min = -z_buffer


# +
# Initialize session and build simulation objects. Set hide = True to hide the Lumerical GUI. 
# This block will build a 1D trapezoidal blazed grating structure on a substrate. 
# The simulation file will be saved to the current working directory with the name specified in the "filename" variable above.

def build_1D_grating(fdtd, filename, period_x, fill_factor, depth, top_factor, num_teeth, base_x, base_y, base_z, n_grat, n_base):
    """
    Builds a 1D trapezoidal blazed grating structure on a substrate.

    Parameters:
    fdtd: The name of a Lumerical session object
    filename: File name to save to
    period_x: Period (pitch) of the grating in x direction
    fill_factor: The width of the bottom of the grating tooth as a factor of the period
    depth: Depth of the grating
    top_factor: The top width of the grating tooth as a factor of the bottom width
    num_teeth: Number of grating teeth to create (note only 1 is needed for periodic simulation)
    base_x, base_y, base_z: Dimensions of the base/substrate, should extend through simulation region
    n_grat: Refractive index of the grating material
    n_base: Refractive index of the base material
    """

    fdtd.addstructuregroup({"name": "1D_grating"})
    # First add the base/substrate
    fdtd.addrect({"name": "base", "x": 0, "y": 0, "x span": base_x, "y span": base_y, "z min": -base_z, "z max": 0, "index": n_base})
    
    # Now add the grating teeth 
    for n in range(num_teeth):
        # Define the vertices of the polygon
        x1, y1 = 0, 0
        x2, y2 = period_x*fill_factor, 0
        x3, y3 = period_x*top_factor*fill_factor, depth
        x4, y4 = 0, depth
        vtx = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
        # Set the properties of the grating. We add a rotation to orient from the xy plane to the xz plane
        grating_props = {"name": f"tooth_{n}", "x": n*period_x - 0.5*num_teeth*period_x, "y": 0, "index": n_grat, "first axis": "x", "rotation 1": 90 }
        fdtd.addpoly(grating_props)
        fdtd.setnamed(f"tooth_{n}", "vertices", vtx) # Set the vertices of the polygon
        fdtd.setnamed(f"tooth_{n}", "z span", base_y) # This is the thickness of the grating tooth in the y direction since there is a rotation
        fdtd.addtogroup("1D_grating") # Adds the recently created polygon to the structure group
        fdtd.save(filename)

def build_rcwa(fdtd, filename, x_min, x_max, y_min, y_max, z_min, z_max):      
    """
    Sets up the RCWA simulation object geometry.
    Note the RCWA interfaces are set according to the minimum and maximum z positions of the grating and base objects. 
    Therefore, you must build the grating first and add the RCWA simulation object after the grating is built.

    Parameters:
    fdtd: The name of a Lumerical session object
    filename: File name to save to
    x_min, x_max, y_min, y_max, z_min, z_max: Boundaries of the simulation region
    """
    # Set up RCWA simulation object
    fdtd.addrcwa({"x min": x_min, "x max": x_max, "y min": y_min, "y max": y_max, "z min": z_min, "z max": z_max, 
                  "simulation region": "3D", "propagation direction": "forward"})

    # Set the RCWA interface positions. The interface positions are set from the minimum and maximum z positions of the grating object.
    # For documentation, see https://optics.ansys.com/hc/en-us/articles/12959229278611-RCWA-Solver-Simulation-Object
    fdtd.setnamed("RCWA", "interface position", "reference")
    # Here, set the number of interfaces in each layer; here we set 10 interfaces for the slanted grating
    # Only 1 interface is needed for the base since it is uniform in z
    interfaces = [["::model::1D_grating", "max", 10], ["::model::base", "max", 1]]
    fdtd.setnamed("RCWA", "interface reference positions", interfaces)

    fdtd.save(filename)


# Build the grating and RCWA simulation objects
with lumapi.FDTD(hide = False) as fdtd:
    build_1D_grating(fdtd, filename, period_x, fill_factor, depth, top_factor, num_teeth, base_x, base_y, base_z, n_grat, n_base)
    print("Grating geometry saved to file: " + filename)
    x_shift = -0.25*period_x # Shift the RCWA simulation region by a quarter period to avoid the interface coinciding with the grating tooth edge
    build_rcwa(fdtd, filename, -0.5*period_x + x_shift, 0.5*period_x + x_shift, -0.5*period_x, 0.5*period_x, -2*depth, 3*depth)
    print("RCWA simulation geometry saved to file: " + filename)
   
# -

# <img src="images/diffraction_grating_screenshot.png" width="600">

# ## Part 2: RCWA Simulation.
#

# +
# Open the previously saved file, configure wavelength/angle excitation settings, and run the RCWA simulation. 
# The grating_characterization result is returned. For documentation, see https://optics.ansys.com/hc/en-us/articles/12959229278611-RCWA-Solver-Simulation-Object
# Grating_characterization returns the complex S-parameters for each grating order split into S and P polarizations. 

# Set the number of wavelengths and angles to simulate
# Setting to 1 will use the minimum value set above 
num_wavelengths = 20
num_theta = 4
num_phi = 3

def run_rcwa_simulation(fdtd, filename, wl_min, wl_max, num_wavelengths, theta_min = 0, theta_max = 90, num_theta = 1, phi_min = 0, phi_max = 180, num_phi = 1):
    """
    Runs the RCWA simulation and retrieves the grating characterization results.

    Parameters:
    fdtd: The name of a Lumerical session object
    filename: File name to load
    wl_min: Minimum wavelength
    wl_max: Maximum wavelength
    num_wavelengths: Number of wavelength points
    theta_min: Minimum incident angle (theta)
    theta_max: Maximum incident angle (theta)
    num_theta: Number of theta points
    phi_min: Minimum azimuthal angle (phi)
    phi_max: Maximum azimuthal angle (phi)
    num_phi: Number of phi points
    """
    # First, return to layout
    fdtd.switchtolayout()

    # Set RCWA incident illumination properties 
    fdtd.setnamed("RCWA", "propagation direction", "forward") # Propagate forward or backward along z axis

    fdtd.setnamed("RCWA", "use wavelength spacing", True)
    fdtd.setnamed("RCWA", "minimum wavelength", wl_min)
    fdtd.setnamed("RCWA", "maximum wavelength", wl_max)
    fdtd.setnamed("RCWA", "frequency points", num_wavelengths)
    fdtd.setnamed("RCWA", "incident angle", "range")
    fdtd.setnamed("RCWA", "minimum theta", theta_min)
    fdtd.setnamed("RCWA", "maximum theta", theta_max)
    fdtd.setnamed("RCWA", "theta points", num_theta)
    fdtd.setnamed("RCWA", "minimum phi", phi_min)
    fdtd.setnamed("RCWA", "maximum phi", phi_max)
    fdtd.setnamed("RCWA", "phi points", num_phi)

    # Set result properties
    fdtd.setnamed("RCWA", "report grating characterization", True)
    fdtd.setnamed("RCWA", "return theta and phi as separate parameters when possible", True)

    # Save and run
    fdtd.save(filename)  
    fdtd.run()  # Run the simulation
    fdtd.save(filename)  # Save the file after running to save the results

    # Retrieve results
    gc = fdtd.getresult("RCWA", "grating_characterization")  # full complex S-parameters
    total_energy = fdtd.getresult("RCWA", "total_energy")  # total T/R for each polarization 

    return gc, total_energy

# Now use the function to run the RCWA simulation and retrieve the results
with lumapi.FDTD(filename, hide = False) as fdtd:
    gc, total_energy = run_rcwa_simulation(fdtd, filename, wl_min, wl_max, num_wavelengths, theta_min, theta_max, num_theta, phi_min, phi_max, num_phi)
    print("RCWA simulation completed and results retrieved.")

# Print the sweep parameters
print("RCWA sweep parameters:")
print("lambda:", np.unique(gc["lambda"])*1e9, "nm")  # Convert to nm for display
print("theta:", np.unique(gc["theta"]), "deg")
print("phi:",  np.unique(gc["phi"]), "deg")
# -



# ## Part 3: Plot results and export to LSWM. 

# +
# Now plot useful results.
# The following function helps to extract useful results from the grating_characterization object for plotting.

def extract_T_values_gc(gc, order_n=0, order_m=0, angle_theta=0, angle_phi=0):
    """Extracts T, R results versus wavelength for the specified order and angle for both S and P polarizations."""
    Tss = gc["Tss"]  # Result returned vs. wavelength, theta, phi, orders n and m
    Tpp = gc["Tpp"]
    Rss = gc["Rss"]
    Rpp = gc["Rpp"]

    # Get m and n indices of the specified order
    m = np.where(gc["m"] == order_m)[0]
    n = np.where(gc["n"] == order_n)[0]
    # Get theta and phi indices at normal incidence
    theta_phi = np.where((gc["theta"] == angle_theta) & (gc["phi"] == angle_phi))[0]
    wavelengths = gc["lambda"]  # Wavelength values corresponding to the results

    # Calculate transmission and reflection for both polarizations
    plot_Tss = np.abs(Tss[:, theta_phi, n, m])**2  # wavelength, theta, phi, order n, order m
    plot_Rss = np.abs(Rss[:, theta_phi, n, m])**2
    plot_Tpp = np.abs(Tpp[:, theta_phi, n, m])**2
    plot_Rpp = np.abs(Rpp[:, theta_phi, n, m])**2

    return plot_Tss, plot_Rss, plot_Tpp, plot_Rpp, wavelengths

def extract_T_values_total_energy(total_energy, angle_theta=0, angle_phi=0):
    """Extracts T, R results versus wavelength for the specified angle for both S and P polarizations."""
    Ts = total_energy["Ts"]  # Result returned vs. wavelength, theta, phi
    Tp = total_energy["Tp"]
    Rs = total_energy["Rs"]
    Rp = total_energy["Rp"]

    # Get theta and phi indices at normal incidence
    theta = np.where(total_energy["theta"] == angle_theta)[0]
    phi = np.where(total_energy["phi"] == angle_phi)[0]
    wavelengths = total_energy["lambda"]  # Wavelength values corresponding to the results

    # Calculate transmission and reflection for both polarizations
    plot_Ts = np.abs(Ts[:, theta, phi])  # wavelength, theta, phi
    plot_Rs = np.abs(Rs[:, theta, phi])
    plot_Tp = np.abs(Tp[:, theta, phi])
    plot_Rp = np.abs(Rp[:, theta, phi])

    return plot_Ts, plot_Rs, plot_Tp, plot_Rp, wavelengths



# +
# Plot RCWA results

# Plot efficiencies for specific orders
order_ns = range(-3, 4)  # Specify the range of diffraction orders to plot, e.g., from -3 to 3

# Set up plotting
fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharex=True, sharey=True)

def order_style(order_n):
    if order_n == 0:
        return "black", "-"
    color_map = {
        -3: "#1f4e8c",
        -2: "#3d73b9",
        -1: "#6a9bd5",
        1: "#8c1d18",
        2: "#bf4a43",
        3: "#d97a73",
    }
    return color_map[order_n], "-"

for n in order_ns:
    Tss, Rss, Tpp, Rpp, wavelengths = extract_T_values_gc(gc, order_n=n)
    color, style = order_style(n)
    axes[0].plot(wavelengths*1e9, Tss, label=f"Tss n = {n}", color=color, linestyle=style)
    #axes[0].plot(wavelengths*1e9, Rss, label=f"Rss n = {n}", color=color, linestyle="--")
    axes[1].plot(wavelengths*1e9, Tpp, label=f"Tpp n = {n}", color=color, linestyle=style)
    #axes[1].plot(wavelengths*1e9, Rpp, label=f"Rpp n = {n}", color=color, linestyle="--")

# Retrieve overall T/R results at normal incidence
total_Ts, total_Rs, total_Tp, total_Rp, wavelengths = extract_T_values_total_energy(total_energy)  # Total transmission for each polarization
axes[0].plot(wavelengths*1e9, total_Ts, label="Total Ts", color="black", linewidth=4)
#axes[0].plot(wavelengths*1e9, total_Rs, label="Total Rs", color="black", linestyle="--", linewidth=4)
axes[1].plot(wavelengths*1e9, total_Tp, label="Total Tp", color="black", linewidth=4)
#axes[1].plot(wavelengths*1e9, total_Rp, label="Total Rp", color="black", linestyle="--", linewidth=4)

for ax in axes:
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Efficiency")
    ax.legend()

axes[0].set_title("S Polarization")
axes[1].set_title("P Polarization")

fig.tight_layout()
plt.show(block=False)

# -

# <img src="images/diffraction_efficiency.png" width="600">
