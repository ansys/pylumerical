# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: .venv
# ---

# # A simple example using MODE.
# Waveguide (FDE): https://optics.ansys.com/hc/en-us/articles/360042800453-Waveguide-FDE
#
# The Finite Difference Eigenmode (FDE) solver in MODE is used to characterize a straight waveguide.
#
# In Part 1, we build the structure and set the FDE simulation region.
# In Part 2, we calculate the supported mode profiles of the waveguide.
# In Part 3, we perform a frequency sweep and obtain the effective index, group index, and dispersion.
#
# Prerequisites:
# Valid MODE license is required.

# Perform required imports

from collections import OrderedDict

import ansys.lumerical.core as lumapi

# Part 1: Set up structures and simulation objects

# +
# Set hide = True to hide the Lumerical GUI.
mode = lumapi.MODE(hide=False)

# Set key parameters
wavelength = 1.55e-6  # Center wavelength
# Set the waveguide cross-section and material
wg_width = 0.5e-6
wg_height = 0.22e-6
wg_material = "Si (Silicon) - Palik"
# Set substrate and cladding cross-section and material
sub_width = 10e-6
sub_height = 5e-6
sub_material = "SiO2 (Glass) - Palik"
clad_width = 10e-6
clad_height = 5e-6
clad_material = "SiO2 (Glass) - Palik"
# Set FDE region
fde_x_span = 3e-6
fde_y_span = 3e-6
fde_y_center = wg_height / 2
fde_z = 0e-6

z_span = 1.0e-6  # Sets z span for all structures, but note FDE solver utilizes a cross section

# Build substrate and cladding
mode.addrect(name="substrate", x=0, x_span=sub_width, y_min=-sub_height, y_max=0, z=0, z_span=z_span, material=sub_material)
mode.addrect(name="clad", x=0, x_span=clad_width, y_min=0, y_max=clad_height, z=0, z_span=z_span, material=clad_material)
# Build waveguide
# Use mesh order override to ensure waveguide object is prioritized over substrate and cladding
wg_props = OrderedDict(
    [
        ("name", "waveguide"),
        ("x", 0),
        ("x span", wg_width),
        ("y min", 0),
        ("y max", wg_height),
        ("z", 0),
        ("z span", z_span),
        ("material", wg_material),
        ("override mesh order from material database", True),
        ("mesh order", 1),
    ]
)
mode.addrect(properties=wg_props)

# Add FDE solver region
fde_props = OrderedDict([("x", 0), ("x span", fde_x_span), ("y", fde_y_center), ("y span", fde_y_span), ("z", fde_z)])
mode.addfde(properties=fde_props)

# Add mesh override region
mesh_props = OrderedDict(
    [
        ("set maximum mesh step", True),
        ("override x mesh", True),
        ("override y mesh", True),
        ("dx", 0.01e-6),
        ("dy", 0.01e-6),
        ("based on a structure", True),
        ("structure", "waveguide"),
    ]
)
mode.addmesh(properties=mesh_props)
# -

# Part 2: Calculate the supported modes of the waveguide. The analysis_props are equivalent to the settings
# in the Eigensolver Analysis window in the GUI.

# +
mode.setanalysis("wavelength", wavelength)
mode.setanalysis("number of trial modes", 10)
mode.setanalysis("search", "near n")
mode.setanalysis("use max index", True)
mode.findmodes()

# Select and plot the fundamental mode
selected_mode_number = 1
selected_mode = "mode" + str(selected_mode_number)
Efield = mode.getresult("FDE::data::" + selected_mode, "E")

# Plot in Python  - requires matplotlib
# Note that passing field data from Lumerical to Python may require additional effort.
# Lumerical uses an unstructured mesh, so the spacing between points may be non-constant.
# Ex = mode.getdata("FDE::data::"+selected_mode,"Ex")[:,:,0,0]
# Ey = mode.getdata("FDE::data::"+selected_mode,"Ey")[:,:,0,0]
# Ez = mode.getdata("FDE::data::"+selected_mode,"Ez")[:,:,0,0]
# absE = np.abs(Ex)**2+np.abs(Ey)**2+np.abs(Ez)**2
# plt.figure()
# plt.imshow(np.transpose(absE))
# plt.show()

# Plot in Lumerical GUI
mode.visualize((Efield))
# -
# Part 3: Perform a frequency sweep for the selected mode of the waveguide.


# +
mode.selectmode(selected_mode_number)
mode.setanalysis("track selected mode", 1)
mode.setanalysis("detailed dispersion calculation", 1)
mode.setanalysis("stop wavelength", 1.6e-6)
mode.setanalysis("number of points", 10)
mode.frequencysweep()

# Save completed simulation file
mode.save("fde_wg_tutorial.lms")

mode.print("Example complete. Hit space bar to continue.")
mode.pause(60)
# -
