"""

Basic session management
------------------------
This example demonstrates how to initialize a local Lumerical session.
PyLumerical interacts with Lumerical products through sessions. 


Prerequesites: Valid FDTD license is required. 
"""

###############################################################################
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~

import ansys.lumerical.core as lumapi
import time

###############################################################################
#
# Open an interactive session
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

fdtd = lumapi.FDTD()
# Wait for 5 seconds, then add fdtd region
time.sleep(5)
fdtd.addfdtd()
time.sleep(2)
fdtd.close()

mode = lumapi.MODE()
# Wait for 5 seconds, then close
time.sleep(5)
mode.close()

# Load a session but hide the application window
fdtd = lumapi.FDTD(hide=True)
fdtd.close()

###############################################################################
#
# Use the "with" context manager
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

with lumapi.FDTD() as fdtd:
    fdtd.addfdtd()
    time.sleep(2)
# FDTD closes automatically

###############################################################################
#
# Session wrapped in a function
# Get the number of grid cells in FDTD region for set span
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_x_cells(fdtd_span):
    """Return the number of grid cells in FDTD region for a set span."""
    fdtd = lumapi.FDTD()
    # Adds FDTD region with span set by fdtd_span
    fdtd.addfdtd(dimension = "3D", x_span = fdtd_span, y_span = fdtd_span, z_span = fdtd_span)
    x = fdtd.getresult("FDTD","x") # Get x coordinates of created FDTD region
    x_cells = len(x)
    return x_cells

# Test the function and print out the result
test = get_x_cells(1e-6)
print(test)

