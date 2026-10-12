# # Grating Coupler: Optimization
#
# Given a grating coupler design, this example demonstrates how to optimize the fiber position for improved coupling efficiency.
#
# This example is the **second** part of the grating-coupler workflow:
# - Create a grating coupler: set up the base simulation and run it.
# - **Optimize the grating coupler: improve the fiber position for better coupling efficiency.**
# - Extract S-parameters: export S-parameters to Interconnect.
# - Lumerical FDTD and Zemax Interconnect: export the field to ZBF for import into Zemax.
#
# This example demonstrates how to set up a SciPy optimization with a small number of variables.
#
# ## Prerequisites
#
# A valid FDTD license is required.
#
# ### Import required modules


import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

import ansys.lumerical.core as lumapi

#
# ### Assign key parameters

# +
show_GUI = True
# The `grating_coupler.fsp` file can be obtained by following the previous steps in the grating coupler workflow.
load_file_name = "your/path/to/grating_coupler.fsp"
save_file_name = "your/path/to/grating_coupler_optimized.fsp"

# Unit conversion factors
um_to_m = 1e-6
m_to_um = 1e6

# Optimization variable: fiber x-position `fiber_x_pos`
fiber_x0 = [5.0 * um_to_m]
fiber_x_bounds = [(1.5 * um_to_m, 5.0 * um_to_m)]

# Optimization target: maximize transmission at the target wavelength `lambda_0`
lambda_0 = 1.55 * um_to_m

# User-defined constant
sio2_tox_offset = 0.65 * um_to_m

# -
# ### Set up FDTD simulation environment
#
# Load the grating coupler `.fsp` file. It can be obtained by following the previous steps in the grating coupler workflow.

# +
# Load the project file.
fdtd = lumapi.FDTD(hide=not show_GUI)
fdtd.load(load_file_name)

# Use the coarsest mesh accuracy for faster optimization
fdtd.switchtolayout()
fdtd.setnamed("FDTD", "mesh accuracy", 1)

# Capture the initial fiber and TOX positions and parameters.
fiber_y_pos = fdtd.getnamed("fiber", "y")
fiber_z_pos = fdtd.getnamed("fiber", "z")
fiber_theta = fdtd.getnamed("fiber::core", "rotation 1")
fiber_core_diameter = fdtd.getnamed("fiber::core", "radius") * 2
tox_zpos = fdtd.getnamed("SiO2 TOX", "z")

# Calculate intermediate parameters and assign their values.
port1_z_pos = tox_zpos + fiber_z_pos + sio2_tox_offset * np.cos(np.deg2rad(fiber_theta))
port_offset = 4.0 * fiber_core_diameter * np.tan(np.deg2rad(fiber_theta))
fdtd.setnamed("::model::FDTD::ports::port 1", "y", fiber_y_pos)
fdtd.setnamed("::model::FDTD::ports::port 1", "z", port1_z_pos)
fdtd.setnamed("::model::FDTD::ports::port 1", "theta", fiber_theta)
fdtd.setnamed("::model::FDTD::ports::port 1", "rotation offset", port_offset)

# -
# ### Scipy optimization
# For a small number of variables (<=3), we recommend using SciPy as the optimizer. For a large number of variables, we recommend using [lumopt2](https://lumerical.docs.pyansys.com/version/stable/user_guide/photonic_inverse_design_with_lumopt2.html).
#
# Here, we use the SciPy [Powell method](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-powell.html).
# To run the optimization, define:
# - an objective function that takes the parameters and returns a fitness value,
# - an initial guess for the variables, and
# - bounds that physically constrain the variables.

# +
# To optimize more variables, add them to `x0` and `bounds`, then unpack them here.
fitness_history = []


def objective(params: np.ndarray) -> float:
    """Objective function for optimizing the fiber's x-position.

    Args:
        params (np.ndarray): Array containing the fiber x-position [fiber_x_pos].

    Returns
    -------
        float: The negative transmission at the target wavelength.
    """
    # Step 1: Capture the current parameter (fiber x-position).
    fiber_x_pos = float(params[0])

    # Step 2: Apply the current parameter to the simulation layout.
    # Fiber x-position
    fdtd.switchtolayout()
    fdtd.setnamed("fiber", "x", fiber_x_pos)
    # Port 1 position
    port1_x_pos = fiber_x_pos + sio2_tox_offset * np.sin(np.deg2rad(fiber_theta))
    fdtd.setnamed("::model::FDTD::ports::port 1", "x", port1_x_pos)

    # Step 3: Extract the merit function value (transmission at the target wavelength).
    fdtd.run()
    # Extract the wavelengths and transmission values from the simulation result.
    transmission = fdtd.getresult("::model::FDTD::ports::port 2", "T")
    wavelengths = np.asarray(transmission["lambda"]).squeeze()
    values = np.abs(np.asarray(transmission["T"]).squeeze())
    fitness = float(values[np.argmin(np.abs(wavelengths - lambda_0))])

    # Append the current fitness to the history to track optimization progress.
    fitness_history.append(fitness)

    # The objective function must return a value to minimize, so return the negative fitness.
    return -fitness


# +
# Run the optimization using SciPy's `minimize` function. This may take a while because it runs multiple simulations.
result = sp.optimize.minimize(objective, fiber_x0, method="Powell", bounds=fiber_x_bounds)
if not result.success:
    raise RuntimeError(result.message)

best_fiber_x_pos = result.x[0]
print(f"Optimal fiber x: {best_fiber_x_pos * m_to_um:.3f} um; transmission: {-result.fun:.4f}")

# -
# ### Apply the optimization result to the simulation layout

# +
best_port1_x_pos = best_fiber_x_pos + sio2_tox_offset * np.sin(np.deg2rad(fiber_theta))

fdtd.switchtolayout()
fdtd.setnamed("fiber", "x", best_fiber_x_pos)
fdtd.setnamed("::model::FDTD::ports::port 1", "x", best_port1_x_pos)
fdtd.save(save_file_name)

# +
# Plot the optimization progress.
best_fitness = np.maximum.accumulate(fitness_history)
plt.plot(best_fitness)
plt.xlabel("Objective evaluation")
plt.ylabel("Best transmission")
plt.title(f"Fitness improvement: {best_fitness[0]:.4f} to {best_fitness[-1]:.4f} (+{best_fitness[-1] - best_fitness[0]:.4f})")
plt.tight_layout()
plt.show(block=False)

# -
# <img src="images/fitness_history.png" width="600">

# +
# Close the application when the GUI is hidden.
if not show_GUI:
    fdtd.close()
