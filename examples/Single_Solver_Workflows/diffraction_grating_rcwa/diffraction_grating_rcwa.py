# # Diffraction Grating (RCWA)
#
# This example simulates a simple diffraction grating using RCWA.
#
# In Part 1, we set up the structures. We define a 1D trapezoidal blazed grating (commonly used in AR/VR applications).
# The grating is parameterized by its periodicity, fill factor, top width, and depth.
# In Part 2, we use RCWA to calculate the complex transmission/reflection of the grating.
# In Part 3, we plot the results.
# In Part 4, we use FDTD to calculate transmission, to see if the two results converge.
#
# Prerequisites: Valid FDTD license is required.

# Perform required imports
from typing import Dict, Tuple  # Only required for better type hint

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt  # Only required for plotting
import numpy as np

import ansys.lumerical.core as lumapi

# ## Part 1: Set up structures and simulation objects

# +
# Define parameters

# Set whether user want to see GUI pop
show_GUI = True

# Set filename for saving and loading
filename = "1D_diffraction_grating.fsp"

# Units
um_to_m = 1e-6
nm_to_m = 1e-9
m_to_nm = 1e9

# Grating parameters
period_x_m = 0.600 * um_to_m  # Period (pitch) of the grating in x direction, 1D grating
fill_factor = 0.5
depth_m = 0.40 * um_to_m
top_factor = 0.3  # The top width of the grating tooth as a factor of the bottom width, for a trapezoidal profile. Set to 0 for rectangular profile.
num_teeth = 5  # Number of grating teeth to create; only one is needed for periodic boundary conditions

# Base/ substrate parameters
base_x_m = 1.5 * period_x_m * num_teeth  # The x span of the base/substrate
base_y_m = 3 * period_x_m
base_z_m = 5 * um_to_m  # Typically we inject light into the substrate/base and assume it is infinitely thick compared to the teeth

# Set materials
n_grat = 1.565  # Refractive index of the grating material, simple non-dispersive material
n_base = 1.565  # Refractive index of the base material, simple non-dispersive material

# Define wavelengths of interest
wl_min_m = 350 * nm_to_m
wl_max_m = 800 * nm_to_m

# Define angles of interest
theta_min = 0
theta_max = 90
phi_min = 0
phi_max = 360

# Simulation parameters
sim_x_span_m = period_x_m  # The x span of the simulation region, set to one period for periodic boundary conditions
sim_y_span_m = period_x_m  # The y span of the simulation region; here the grating is uniform in y, so this can be made thinner if desired
z_buffer_m = wl_min_m  # A buffer region above and below the structure to ensure the simulation region is large enough to avoid boundary effects
sim_z_max_m = depth_m + z_buffer_m  # Good practice to make sure the simulation region is at least one wavelength larger than the structure
sim_z_min_m = -z_buffer_m


# +
# Initialize session and build simulation objects. Set hide = True to hide the Lumerical GUI.
# This block will build a 1D trapezoidal blazed grating structure on a substrate.
# The simulation file will be saved to the current working directory with the name specified in the "filename" variable above.


def build_1d_grating(
    fdtd,
    filename,
    period_x_m: float,
    fill_factor: float,
    depth: float,
    top_factor: float,
    num_teeth: int,
    base_x: float,
    base_y: float,
    base_z: float,
    n_grat: float,
    n_base: float,
) -> None:
    """
    Build a 1D trapezoidal blazed grating structure on a substrate.

    Parameters
    ----------
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
        x2, y2 = period_x_m * fill_factor, 0
        x3, y3 = period_x_m * top_factor * fill_factor, depth
        x4, y4 = 0, depth
        vtx = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
        # Set the properties of the grating. We add a rotation to orient from the xy plane to the xz plane
        grating_props = {
            "name": f"tooth_{n}",
            "x": n * period_x_m - 0.5 * num_teeth * period_x_m,
            "y": 0,
            "index": n_grat,
            "first axis": "x",
            "rotation 1": 90,
        }
        fdtd.addpoly(grating_props)
        fdtd.setnamed(f"tooth_{n}", "vertices", vtx)  # Set the vertices of the polygon
        fdtd.setnamed(f"tooth_{n}", "z span", base_y)  # This is the thickness of the grating tooth in the y direction since there is a rotation
        fdtd.addtogroup("1D_grating")  # Adds the recently created polygon to the structure group
        fdtd.save(filename)


def build_rcwa(fdtd, filename, x_min: float, x_max: float, y_min: float, y_max: float, z_min: float, z_max: float) -> None:
    """
    Set up the RCWA simulation object geometry.

    Note the RCWA interfaces are set according to the minimum and maximum z positions of the grating and base objects.
    Therefore, you must build the grating first and add the RCWA simulation object after the grating is built.

    Parameters
    ----------
    fdtd: The name of a Lumerical session object
    filename: File name to save to
    x_min, x_max, y_min, y_max, z_min, z_max: Boundaries of the simulation region
    """
    # Set up RCWA simulation object
    fdtd.addrcwa(
        {
            "x min": x_min,
            "x max": x_max,
            "y min": y_min,
            "y max": y_max,
            "z min": z_min,
            "z max": z_max,
            "simulation region": "3D",
            "propagation direction": "forward",
        }
    )

    # Set the RCWA interface positions. The interface positions are set from the minimum and maximum z positions of the grating object.
    # For documentation, see https://optics.ansys.com/hc/en-us/articles/12959229278611-RCWA-Solver-Simulation-Object
    fdtd.setnamed("RCWA", "interface position", "reference")
    # Here, set the number of interfaces in each layer; here we set 10 interfaces for the slanted grating
    # Only 1 interface is needed for the base since it is uniform in z
    interfaces = [["::model::1D_grating", "max", 10], ["::model::base", "max", 1]]
    fdtd.setnamed("RCWA", "interface reference positions", interfaces)

    fdtd.save(filename)


# Build the grating and RCWA simulation objects
fdtd = lumapi.FDTD(hide=not show_GUI)
build_1d_grating(fdtd, filename, period_x_m, fill_factor, depth_m, top_factor, num_teeth, base_x_m, base_y_m, base_z_m, n_grat, n_base)
print("Grating geometry saved to file: " + filename)
x_shift = -0.25 * period_x_m  # Shift the RCWA simulation region by a quarter period to avoid the interface coinciding with the grating tooth edge
build_rcwa(fdtd, filename, -0.5 * period_x_m + x_shift, 0.5 * period_x_m + x_shift, -0.5 * period_x_m, 0.5 * period_x_m, -2 * depth_m, 3 * depth_m)
print("RCWA simulation geometry saved to file: " + filename)
# -

# <img src="images/diffraction_grating_screenshot.png" width="600">

# ## Part 2: RCWA Simulation
#

# +
# Configure wavelength/angle excitation settings, and run the RCWA simulation.
# The grating_characterization result is returned. For documentation, see https://optics.ansys.com/hc/en-us/articles/12959229278611-RCWA-Solver-Simulation-Object
# Grating_characterization returns the complex S-parameters for each grating order split into S and P polarizations.

# Set the number of wavelengths and angles to simulate
# Setting to 1 will use the minimum value set above
num_wavelengths = 20
num_theta = 4
num_phi = 3


def run_rcwa_simulation(
    fdtd,
    filename,
    wl_min: float,
    wl_max: float,
    num_wavelengths: int,
    theta_min: float = 0.0,
    theta_max: float = 90.0,
    num_theta: int = 1,
    phi_min: float = 0.0,
    phi_max: float = 180.0,
    num_phi: int = 1,
) -> Tuple[Dict, Dict]:
    """
    Run the RCWA simulation and retrieves the grating characterization results.

    Parameters
    ----------
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

    Returns
    -------
    gc: The grating_characterization result, containing the full complex S-parameters (Tss, Tpp, Rss, Rpp)
        versus wavelength, theta, phi, and diffraction orders n and m
    total_energy: The total_energy result, containing the total transmission/reflection (Ts, Tp, Rs, Rp)
        versus wavelength, theta, and phi for each polarization
    """
    # First, return to layout
    fdtd.switchtolayout()

    # Set RCWA incident illumination properties
    fdtd.setnamed("RCWA", "propagation direction", "forward")  # Propagate forward or backward along z axis

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
gc, total_energy = run_rcwa_simulation(
    fdtd, filename, wl_min_m, wl_max_m, num_wavelengths, theta_min, theta_max, num_theta, phi_min, phi_max, num_phi
)
print("RCWA simulation completed and results retrieved.")

# Print the sweep parameters
print("RCWA sweep parameters:")
print("lambda:", np.unique(gc["lambda"]) * m_to_nm, "nm")  # Convert to nm for display
print("theta:", np.unique(gc["theta"]), "deg")
print("phi:", np.unique(gc["phi"]), "deg")
# -


# ## Part 3: Plot results and export to LSWM

# +
# Now plot useful results.
# The following function helps to extract useful results from the grating_characterization object for plotting.


def extract_values_gc(
    gc, order_n: int = 0, order_m: int = 0, angle_theta: float = 0.0, angle_phi: float = 0.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Extract T, R results versus wavelength for the specified order and angle for both S and P polarizations.

    Parameters
    ----------
    gc: The grating_characterization result dictionary returned by the RCWA simulation, containing the complex
        S-parameters (Tss, Tpp, Rss, Rpp) versus wavelength, theta, phi, and diffraction orders n and m
    order_n: Diffraction order index along n to extract
    order_m: Diffraction order index along m to extract
    angle_theta: Incident theta angle (deg) to extract
    angle_phi: Incident phi angle (deg) to extract

    Returns
    -------
    plot_Tss, plot_Rss, plot_Tpp, plot_Rpp: Transmission/reflection efficiencies versus wavelength for the
        specified order and angle, for S and P polarizations respectively
    wavelengths: Wavelength values corresponding to the results
    """
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
    plot_Tss = np.abs(Tss[:, theta_phi, n, m]) ** 2  # wavelength, theta, phi, order n, order m
    plot_Rss = np.abs(Rss[:, theta_phi, n, m]) ** 2
    plot_Tpp = np.abs(Tpp[:, theta_phi, n, m]) ** 2
    plot_Rpp = np.abs(Rpp[:, theta_phi, n, m]) ** 2

    return plot_Tss, plot_Rss, plot_Tpp, plot_Rpp, wavelengths


def extract_values_total_energy(
    total_energy: dict, angle_theta: float = 0.0, angle_phi: float = 0.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Extract T, R results versus wavelength for the specified angle for both S and P polarizations.

    Parameters
    ----------
    total_energy: The total_energy result dictionary returned by the RCWA simulation, containing the total
        transmission/reflection (Ts, Tp, Rs, Rp) versus wavelength, theta, and phi for each polarization
    angle_theta: Incident theta angle (deg) to extract
    angle_phi: Incident phi angle (deg) to extract

    Returns
    -------
    plot_Ts, plot_Rs, plot_Tp, plot_Rp: Total transmission/reflection efficiencies versus wavelength at the
        specified angle, for S and P polarizations respectively
    wavelengths: Wavelength values corresponding to the results
    """
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


def order_style(order_n: int):
    """
    Help plot diffraction orders with different colors.

    Parameters
    ----------
    order_n: Diffraction order index to get the plotting color/linestyle for. Order 0 is plotted in black;
        negative orders (-3 to -1) use shades of blue, and positive orders (1 to 3) use shades of red

    Returns
    -------
    A tuple of (color, linestyle) to use when plotting the given diffraction order
    """
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
    Tss, Rss, Tpp, Rpp, wavelengths = extract_values_gc(gc, order_n=n)
    color, style = order_style(n)
    axes[0].plot(wavelengths * 1e9, Tss, label=f"Tss n = {n}", color=color, linestyle=style)
    # axes[0].plot(wavelengths*1e9, Rss, label=f"Rss n = {n}", color=color, linestyle="--")
    axes[1].plot(wavelengths * 1e9, Tpp, label=f"Tpp n = {n}", color=color, linestyle=style)
    # axes[1].plot(wavelengths*1e9, Rpp, label=f"Rpp n = {n}", color=color, linestyle="--")

# Retrieve overall T/R results at normal incidence
total_Ts, total_Rs, total_Tp, total_Rp, wavelengths = extract_values_total_energy(total_energy)  # Total transmission for each polarization
axes[0].plot(wavelengths * 1e9, total_Ts, label="Total Ts", color="black", linewidth=4)
# axes[0].plot(wavelengths*1e9, total_Rs, label="Total Rs", color="black", linestyle="--", linewidth=4)
axes[1].plot(wavelengths * 1e9, total_Tp, label="Total Tp", color="black", linewidth=4)
# axes[1].plot(wavelengths*1e9, total_Rp, label="Total Rp", color="black", linestyle="--", linewidth=4)

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

# ## Part 4: Verify the results with FDTD
# Unlike RCWA, FDTD simulation requires a dedicated defined source to excite EM field, and a dedicated defined monitor to capture EM field.


# +
# Function to set up FDTD simulation environment: a FDTD mesh with proper boundary conditions, a source, and a monitor
def set_fdtd_simulation(
    fdtd, filename, x_min: float, x_max: float, y_min: float, y_max: float, z_min: float, z_max: float, wl_min: float, wl_max: float
) -> None:
    """
    Set up the FDTD simulation environment: one FDTD mesh, one plane wave source, and one DFT 2D monitor.

    Parameters
    ----------
    fdtd: The name of a Lumerical session object
    filename: File name to save to
    x_min, x_max, y_min, y_max, z_min, z_max: Boundaries of the simulation region
    wl_min, wl_max: Source wavelength range
    """
    # First, return to layout
    fdtd.switchtolayout()

    # Set up FDTD simulation object
    # The FDTD simulation area is set to be identical to the previous RCWA
    fdtd.addfdtd(
        {
            "x min": x_min,
            "x max": x_max,
            "y min": y_min,
            "y max": y_max,
            "z min": z_min,
            "z max": z_max,
            "x min bc": "Periodic",
            "y min bc": "Periodic",
            "z min bc": "PML",
            "z max bc": "PML",
        }
    )

    # For FDTD, a dedicated source and monitor is required
    fdtd.addplane(
        {
            "name": "source",
            "injection axis": "z-axis",
            "x min": x_min,
            "x max": x_max,
            "y min": y_min,
            "y max": y_max,
            "z": z_min * 0.95,  # z position: inside the FDTD range, slightly closer to z = 0
            "wavelength start": wl_min,
            "wavelength stop": wl_max,
        }
    )

    # A plane monitor put at the top
    fdtd.adddftmonitor(
        {
            "name": "monitor",
            "monitor type": "2D Z-normal",
            "x min": x_min,
            "x max": x_max,
            "y min": y_min,
            "y max": y_max,
            "z": z_max * 0.95,  # z position: inside the FDTD range, slightly closer to z = 0
            "output Ex": 1,
            "output Ey": 1,
        }
    )

    # Save
    fdtd.save(filename)


# Now use the function to define a FDTD simulation area, plane wave source, and 2D plane monitor
set_fdtd_simulation(
    fdtd,
    filename,
    x_min=-0.5 * period_x_m + x_shift,
    x_max=0.5 * period_x_m + x_shift,
    y_min=-0.5 * period_x_m,
    y_max=0.5 * period_x_m,
    z_min=-2 * depth_m,
    z_max=3 * depth_m,
    wl_min=wl_min_m,
    wl_max=wl_max_m,
)


# +
def set_polarization_angle_and_run_fdtd(fdtd, filename, source_name: str = "source", polarization_angle: float = 0.0) -> None:
    """
    Set the polarization angle of the FDTD source and run the FDTD simulation.

    Parameters
    ----------
    fdtd: The name of a Lumerical session object
    filename: File name to save to
    source_name: Name of the source object whose polarization angle is set
    polarization_angle: Polarization angle (deg) to set on the source. Use 0 for P-polarization,
        or 90 for S-polarization
    """
    # First, return to layout
    fdtd.switchtolayout()

    # Set polarization angle
    fdtd.setnamed(source_name, "polarization angle", polarization_angle)

    # Save and run
    fdtd.save(filename)
    fdtd.run("FDTD")  # Run FDTD only
    fdtd.save(filename)  # Save the file after running to save the results


# Here we test P-polarization: polarization_angle = 0, axis = axes[1]
set_polarization_angle_and_run_fdtd(fdtd, filename, polarization_angle=0)
axis = axes[1]

# # Otherwise use S-polarization: polarization_angle = 90, axis = axes[0]
# set_polarization_angle_and_run_FDTD(fdtd, filename, polarization_angle=90)
# axis = axes[0]


# +
# Capture the total transmission and plot
freq_list = fdtd.getdata("monitor", "f").flatten()
wavelength_m_list = 3e8 / freq_list
transmission_list = fdtd.transmission("monitor").flatten()

axis.scatter(
    wavelength_m_list * 1e9,  # Transfer to nm
    transmission_list,
    color="red",
    s=80,
    marker="x",
    zorder=10,
)

fig  # plot the figure
# -
# <img src="images/diffraction_efficiency_FDTD_total.png" width="600">
#
# According to grating equation (normal incidence)
# $$ \frac{m \lambda}{D} = \sin{\theta}, $$
# the $m$ -th order beam should be propagated at $\arcsin{(\frac{m \lambda}{D})}$ direction,
# where $D$ is the grating period `period_x_m`.
#
# Therefore, we calculate `order_ux` as $\frac{m \lambda}{D}$, compare it with Lumerical FDTD
# far field monitor's internal `fdtd.farfieldux()`, to get the transmission of each order at each wavelength point.

# +
# Calculate the far field data

# First, define a few parameters to use Lumerical FDTD's far field related feature
ux_map_pix_num = 500  # far field monitor's resolution, higher value -> higher accuracy
uy_map_pix_num = 1  # for simplification as we are modeling a 1D grating on x-direction
illumination_type = 2  # 1: Gaussian. 2: plane wave.
num_of_period_x = 20  # how many monitor (in this case, the DFT monitor "monitor") periods is considered when calculating the far field,
# higher value -> higher accuracy -> sharper peaks in far field -> requires higher `ux_map_pix_num`
num_of_period_y = 1  # for simplification as we are modeling a 1D grating on x-direction


def find_main_lobe(y: np.ndarray, peak_idx: int) -> Tuple[int, int]:
    """
    Find the indices that defines the full lobe for given function and index.

    Parameters
    ----------
    y: 1D array of function values (e.g., far field energy distribution) to search within
    peak_idx: Index of the peak within `y` around which the main lobe is found

    Returns
    -------
    A tuple (left_idx, right_idx) of indices bounding the main lobe around `peak_idx`, clipped to the
    valid range of `y`
    """
    # left minimum
    left_idx = peak_idx - 1
    while left_idx > 1 and y[left_idx - 1] <= y[left_idx]:
        left_idx -= 1

    # right minimum
    right_idx = peak_idx + 1
    while right_idx < len(y) - 2 and y[right_idx] >= y[right_idx + 1]:
        right_idx += 1

    return np.max((left_idx, 0)), np.min((right_idx, len(y)))


# Calculate transmission at each wavelength, each order
transmission_order_wavelength = np.zeros((len(order_ns), len(wavelength_m_list)))
for w_idx, wavelength_m in enumerate(wavelength_m_list):
    # Capture the far field monitor
    E = fdtd.farfield3d(
        "monitor",
        w_idx + 1,  # monitor name, frequency index (start at 1)
        ux_map_pix_num,
        uy_map_pix_num,
        illumination_type,
        num_of_period_x,
        num_of_period_y,
    ).flatten()
    ux = fdtd.farfieldux("monitor", w_idx + 1, ux_map_pix_num, uy_map_pix_num, illumination_type).flatten()
    uy = fdtd.farfielduy("monitor", w_idx + 1, ux_map_pix_num, uy_map_pix_num, illumination_type)

    # For each wavelength, calculate corresponding ux of each order of interests
    order_ux = order_ns * wavelength_m / period_x_m  # legal value: >-1 & <1

    # Find the index of order_ux that closest to ux
    order_ux_idx = np.abs(ux[:, None] - order_ux.flatten()).argmin(axis=0)

    total_energy = np.trapezoid(E, ux)
    for i, idx in enumerate(order_ux_idx):
        left_idx, right_idx = find_main_lobe(E, idx)
        main_lobe_energy = np.trapezoid(E[left_idx:right_idx], ux[left_idx:right_idx])
        transmission_order_wavelength[i, w_idx] = float(main_lobe_energy / total_energy * transmission_list[w_idx])

# Plot
for i, order in enumerate(order_ns):
    transmission_wavelength = transmission_order_wavelength[i, :].flatten()
    axis.scatter(
        wavelength_m_list * 1e9,  # Transfer to nm
        transmission_wavelength,
        color=order_style(order)[0],
        s=60,
        marker="x",
        zorder=10,
    )
fdtd_marker = Line2D([], [], color="black", marker="x", linestyle="None", label="FDTD confirmation")
axis.legend(handles=axis.get_legend_handles_labels()[0] + [fdtd_marker])

fig  # plot the figure

# -
# <img src="images/diffraction_efficiency_FDTD_total_order.png" width="600">

# +
# Safely close the Lumerical task
if not show_GUI:
    fdtd.close()
# -
