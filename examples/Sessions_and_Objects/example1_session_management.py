# %% [markdown]
# ## Basic FDTD Simulation - Lumerical style commands
#
# This simple example demonstrates using PyLumerical to start a session using Lumerical Script File (lsf) style commands.
# Sets up and runs a basic FDTD simulation. E field results are plotted in Lumerical.
# [Lumerical API](https://optics.ansys.com/hc/en-us/articles/360037824513-Python-API-overview)
#
#
# ## Prerequisites:
#
# Valid FDTD license is required.
#

# %%
import ansys.lumerical.core as lumapi

# Set hide = True to hide the Lumerical GUI.
fdtd = lumapi.FDTD(hide=False)

# -

#
# ### Set up simulation region

fdtd.addfdtd()
fdtd.set("x", 0)
fdtd.set("x span", 8e-6)
fdtd.set("y", 0)
fdtd.set("y span", 8e-6)
fdtd.set("z", 0.25e-6)
fdtd.set("z span", 0.5e-6)

# ### Set up source

fdtd.addgaussian()
fdtd.set("injection axis", "z")
fdtd.set("direction", "forward")
fdtd.set("x", 0)
fdtd.set("x span", 16e-6)
fdtd.set("y", 0)
fdtd.set("y span", 16e-6)
fdtd.set("z", 0.2e-6)
fdtd.set("use scalar approximation", 1)
fdtd.set("waist radius w0", 2e-6)
fdtd.set("distance from waist", 0)
fdtd.setglobalsource("wavelength start", 1e-6)
fdtd.setglobalsource("wavelength stop", 1e-6)

# ### Set up monitor

fdtd.adddftmonitor()
fdtd.set("monitor type", "2D Z-normal")
fdtd.set("x", 0)
fdtd.set("x span", 16e-6)
fdtd.set("y", 0)
fdtd.set("y span", 16e-6)
fdtd.set("z", 0.3e-6)

# ### Run and save simulation

fdtd.save("fdtd_tutorial.fsp")
fdtd.run()

# ### Retrieve and plot results

E = fdtd.getresult("monitor", "E")
fdtd.visualize(E)

# ### Keep session open until user clicks space bar

fdtd.print("Example complete. Hit space bar to close.")


# %% [markdown]
# ## Python style commands
#
# A simple example to demonstrate using PyLumerical.
#
# Sets up and runs a basic FDTD simulation. E field results are plotted using Matplotlib
# Demonstrates initializing objects using keyword arguments and OrderedDict.

# %%
from collections import OrderedDict

import matplotlib.pyplot as plt

# -

# ### Open interactive session with the "with" context manager, run session, retrieve and plots results, and close session

# Set hide = True to hide the Lumerical GUI.
with lumapi.FDTD() as fdtd:
    # Set up simulation region using keyword arguments
    fdtd.addfdtd(x=0, x_span=8e-6, y=0, y_span=8e-6, z=0.25e-6, z_span=0.5e-6)

    # Set up source using Python OrderedDict
    # OrderedDict is recommended when order is important
    # Here, the scalar appproximation prop should be set before waist radius
    props = OrderedDict(
        [
            ("injection axis", "z"),
            ("direction", "forward"),
            ("x", 0),
            ("x span", 16e-6),
            ("y", 0),
            ("y span", 16e-6),
            ("z", 0.2e-6),
            ("use scalar approximation", 1),
            ("waist radius w0", 2e-6),
            ("distance from waist", 0),
            ("wavelength start", 1e-6),
            ("wavelength stop", 1e-6),
        ]
    )
    fdtd.addgaussian(properties=props)

    # Set up monitor using regular dict
    props = {"monitor type": "2D Z-normal", "x": 0, "x span": 16e-6, "y": 0, "y span": 16e-6, "z": 0.3e-6}
    fdtd.adddftmonitor(properties=props)

    # Run and save simulation
    fdtd.save("fdtd_tutorial.fsp")
    fdtd.run()

    # Retrieve and plot results
    E2 = fdtd.getelectric("monitor")[:, :, 0, 0]

    plt.figure()
    plt.imshow(E2)
    plt.show()

    print("Example complete. Press Enter to close.")
    input()
