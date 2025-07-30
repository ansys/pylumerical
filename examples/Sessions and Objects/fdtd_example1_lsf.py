"""

A simple example to demonstrate using PyLumerical using Lumerical Script File (lsf) style commands.

-------------------------------------------------
Sets up and runs a basic FDTD simulation. E field results are plotted in Lumerical.


Prerequisites: Valid FDTD license is required.
"""

###############################################################################
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~

import ansys.lumerical.core as lumapi

# Set hide = True to hide the Lumerical GUI.
fdtd = lumapi.FDTD(hide=False)

# Set up simulation region
fdtd.addfdtd()
fdtd.set("x", 0)
fdtd.set("x span", 8e-6)
fdtd.set("y", 0)
fdtd.set("y span", 8e-6)
fdtd.set("z", 0.25e-6)
fdtd.set("z span", 0.5e-6)

# Set up source
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

# Set up monitor
fdtd.adddftmonitor()
fdtd.set("monitor type", "2D Z-normal")
fdtd.set("x", 0)
fdtd.set("x span", 16e-6)
fdtd.set("y", 0)
fdtd.set("y span", 16e-6)
fdtd.set("z", 0.3e-6)

# Run and save simulation
fdtd.save("fdtd_tutorial.fsp")
fdtd.run()

# Retrieve and plot results
E = fdtd.getresult("monitor", "E")
fdtd.visualize(E)

# Keep session open until user clicks space bar
fdtd.print("Example complete. Hit space bar to close.")
fdtd.pause(60)
