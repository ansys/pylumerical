# # Basic Session Management
#
# This example demonstrates how to initialize a local Lumerical session.
# PyLumerical interacts with Lumerical products through sessions.
#
# ## Prerequisites: 
# 
# Valid FDTD and MODE licenses are required.




# ### Perform required imports

import ansys.lumerical.core as lumapi

#
# ### Open an interactive session

fdtd = lumapi.FDTD()
# Wait for a second, then add FDTD region
fdtd.pause(1)
fdtd.addfdtd()
fdtd.print("Example complete. Press space bar to close.")
fdtd.pause(30)  # Will close in 30 seconds if left idle
fdtd.close()

mode = lumapi.MODE()
mode.print("Example complete. Press space bar to close.")
mode.pause(30)
mode.close()

# Load a session but hide the application window
fdtd = lumapi.FDTD(hide=True)
fdtd.close()


# ### Use the "with" context manager

with lumapi.FDTD() as fdtd:
    fdtd.addfdtd()
    fdtd.print("Example complete. Press space bar to close.")
    fdtd.pause(30)
# FDTD closes automatically



# ### Session wrapped in a function
# Get the number of grid cells in FDTD region for set span


def get_x_cells(fdtd_span):
    """Return the number of grid cells in FDTD region for a set span."""
    with lumapi.FDTD() as fdtd:
        # Adds FDTD region with span set by fdtd_span
        fdtd.addfdtd(dimension="3D", x_span=fdtd_span, y_span=fdtd_span, z_span=fdtd_span)
        # Get the x-coordinates of created FDTD region
        x = fdtd.getresult("FDTD", "x")
    x_cells = len(x)
    return x_cells


# ### Test the function and print out the result
test = get_x_cells(1e-6)
print(test)
