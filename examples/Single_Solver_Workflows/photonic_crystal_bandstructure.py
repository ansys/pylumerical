# # Photonic Crystal Bandstructure (FDTD)
#
# This example demonstrates a photonic crystal simulation utilizing a built-in Structure Group object.
# Based on: https://optics.ansys.com/hc/en-us/articles/360041566614-Rectangular-Photonic-Crystal-Bandstructure
#
#
# In Part 1, we build the structure and set the FDTD simulation region. In this case, the spheres are holes (filled with air, n = 1)
# and the background material is a simple dielectric material. Some advanced simulation objects, including the photonic crystal array
# and bandstructure analysis groups, are imported from the Object Library. We run a single simulation and visualize the resulting spectrum.
#
# In Part 2, we set up a series of sweeps to collect the resonant frequencies. In this example, we use the built-in sweep tool in Lumerical,
# but the parameter sweeps could also be set up from Python. We then run the sweeps and plot the results.
#
# Prerequisites: Valid FDTD license is required.

# Perform required imports

# +
import matplotlib.pyplot as plt  # Only required for plotting
import numpy as np

import ansys.lumerical.core as lumapi

# -

# Part 1: Set up structures and simulation objects

# +
# Define parameters

# set desired period of the array (3D)
ax = 0.5e-6
ay = 0.5e-6
az = 0.5e-6

# number of spheres in each direction
nx = 3
ny = 3
nz = 3

sphere_radius = 0.25e-6
sphere_index = 1  # Specify index if "Object defined dielectric" is used; otherwise, specify material from database below
sphere_material = "etch"  # Etch n = 1 (air)
background_index = 3.6055

# Define frequencies / wavelengths of interest
f1 = 1e12  # THz
f2 = 220e12  # THz
# -

# Initialize session. Set hide = True to hide the Lumerical GUI.
fdtd = lumapi.FDTD(hide=False)

# +
# Add objects

# Add and set up rectangular lattice array of spheres
fdtd.addobject("rect_pc_3D")
fdtd.set("x", 0)
fdtd.set("y", 0)
fdtd.set("z", 0)
fdtd.set("index", sphere_index)
fdtd.set("material", sphere_material)
fdtd.set("nx", nx)
fdtd.set("ny", ny)
fdtd.set("nz", nz)
fdtd.set("ax", ax)
fdtd.set("ay", ay)
fdtd.set("az", az)
fdtd.set("radius", sphere_radius)

# +
# Add and set up FDTD simulation region

dx = 0.025e-6  # Mesh dx, dy, dz

fdtd.addfdtd()
fdtd.set("x", 0)
fdtd.set("x span", ax)
fdtd.set("y", 0)
fdtd.set("y span", ay)
fdtd.set("z", 0)
fdtd.set("z span", az)
fdtd.set("index", background_index)
fdtd.set("mesh type", "uniform")
fdtd.set("dx", dx)
fdtd.set("dy", dx)
fdtd.set("dz", dx)
fdtd.set("x min bc", "Bloch")
fdtd.set("y min bc", "Bloch")
fdtd.set("z min bc", "Bloch")
# Settings for bloch conditions
# We generally use bandstructure units, but for the simulation region it's
# most convenient to use SI units because kx and ky can have different
# normalizations if the x and y spans are different.
# A normalization factor of 2*pi/a is applied to k later in the sweeps.
fdtd.set("set based on source angle", False)
fdtd.set("bloch units", "SI")


# +
# Set up sources (dipole cloud) and monitors (bandstructure)
# These are both Analysis Groups available from the object library

fdtd.addobject("dipole_cloud")
fdtd.set("f1", f1)
fdtd.set("f2", f2)
fdtd.set("n dipoles", 3)
fdtd.set("kx", 0.5)
fdtd.set("ky", 0)
fdtd.set("kz", 0)
fdtd.set("lattice type", 3)
fdtd.set("z span", az)
fdtd.set("ax", ax)
fdtd.set("ay", ay)
fdtd.set("az", az)
fdtd.set("a", az)

fdtd.addobject("bandstructure")
fdtd.set("x span", ax)
fdtd.set("y span", ay)
fdtd.set("z span", az)
fdtd.set("f1", f1)
fdtd.set("f2", f2)
fdtd.set("n monitors", 10)
# -

# zoom CAD view around simulation region
fdtd.select("FDTD")
fdtd.setview("extent")

fdtd.save("photonic_crystal_bandstructure.fsp")
fdtd.run()
fdtd.runanalysis()

# Visualize the spectrum from a single simulation
single_spectrum = fdtd.getresult("bandstructure", "spectrum")
fdtd.visualize(single_spectrum)

print("Part 1 complete. Single simulation has been run. Next, we set up and run sweeps.")

# Part 2: Set up and run sweeps to extract resonant frequencies and plot the bandstructure

# +
# Normalization factor for SI units; see note above.
norm_x = 2 * np.pi / ax
norm_y = 2 * np.pi / ay
norm_z = 2 * np.pi / az

# Add Gamma-X sweep

fdtd.addsweep()
fdtd.setsweep("sweep", "name", "Gamma-X")
fdtd.setsweep("Gamma-X", "type", "Ranges")
fdtd.setsweep("Gamma-X", "number of points", 20)

# set the sweep properties
props_kx = {"Name": "kx", "Parameter": "::model::FDTD::kx", "Type": "Number", "Start": 0 * norm_x, "Stop": 0.5 * norm_x}
fdtd.addsweepparameter("Gamma-X", props_kx)
props_ky = {"Name": "ky", "Parameter": "::model::FDTD::ky", "Type": "Number", "Start": 0 * norm_y, "Stop": 0 * norm_y}
fdtd.addsweepparameter("Gamma-X", props_ky)
props_kz = {"Name": "kz", "Parameter": "::model::FDTD::kz", "Type": "Number", "Start": 0 * norm_z, "Stop": 0 * norm_z}
fdtd.addsweepparameter("Gamma-X", props_kz)

# define results
result_fs = {"Name": "fs", "Result": "::model::bandstructure::fs"}
fdtd.addsweepresult("Gamma-X", result_fs)
result_spectrum = {"Name": "fs", "Result": "::model::bandstructure::spectrum"}
fdtd.addsweepresult("Gamma-X", result_spectrum)

# Add X-M sweep

fdtd.addsweep()
fdtd.setsweep("sweep", "name", "X-M")
fdtd.setsweep("X-M", "type", "Ranges")
fdtd.setsweep("X-M", "number of points", 20)

# set the sweep properties
props_kx = {"Name": "kx", "Parameter": "::model::FDTD::kx", "Type": "Number", "Start": 0.5 * norm_x, "Stop": 0.5 * norm_x}
fdtd.addsweepparameter("X-M", props_kx)
props_ky = {"Name": "ky", "Parameter": "::model::FDTD::ky", "Type": "Number", "Start": 0 * norm_y, "Stop": 0.5 * norm_y}
fdtd.addsweepparameter("X-M", props_ky)
props_kz = {"Name": "kz", "Parameter": "::model::FDTD::kz", "Type": "Number", "Start": 0 * norm_z, "Stop": 0 * norm_z}
fdtd.addsweepparameter("X-M", props_kz)

# define results
result_fs = {"Name": "fs", "Result": "::model::bandstructure::fs"}
fdtd.addsweepresult("X-M", result_fs)
result_spectrum = {"Name": "fs", "Result": "::model::bandstructure::spectrum"}
fdtd.addsweepresult("X-M", result_spectrum)

# Add M-R sweep

fdtd.addsweep()
fdtd.setsweep("sweep", "name", "M-R")
fdtd.setsweep("M-R", "type", "Ranges")
fdtd.setsweep("M-R", "number of points", 20)

# set the sweep properties
props_kx = {"Name": "kx", "Parameter": "::model::FDTD::kx", "Type": "Number", "Start": 0.5 * norm_x, "Stop": 0.5 * norm_x}
fdtd.addsweepparameter("M-R", props_kx)
props_ky = {"Name": "ky", "Parameter": "::model::FDTD::ky", "Type": "Number", "Start": 0.5 * norm_y, "Stop": 0.5 * norm_y}
fdtd.addsweepparameter("M-R", props_ky)
props_kz = {"Name": "kz", "Parameter": "::model::FDTD::kz", "Type": "Number", "Start": 0 * norm_z, "Stop": 0.5 * norm_z}
fdtd.addsweepparameter("M-R", props_kz)

# define results
result_fs = {"Name": "fs", "Result": "::model::bandstructure::fs"}
fdtd.addsweepresult("M-R", result_fs)
result_spectrum = {"Name": "fs", "Result": "::model::bandstructure::spectrum"}
fdtd.addsweepresult("M-R", result_spectrum)

# +
# Run all the sweeps - this may take a few minutes
print("Sweeps have been set up. Starting sweep run now.")
fdtd.runsweep()
print("Sweep run completed. Now retrieving and plotting results.")

# If you have previously run the sweeps, you can load them using this line instead:
# fdtd.loadsweep()


# +
# Retrieve and analyze data from the sweeps
fs_all = np.zeros((50, 60))  # 50 is the number of frequencies, and 60 bandstructure points = 20 points per sweep x 3 sweeps

sweepname = "Gamma-X"
resonance = fdtd.getsweepresult(sweepname, "fs")  # Results are returned as Python dict
resonance_fs = resonance["fs"]
fs_all[0:50, 0:20] = resonance_fs

sweepname = "X-M"
resonance = fdtd.getsweepresult(sweepname, "fs")  # Results are returned as Python dict
resonance_fs = resonance["fs"]
fs_all[0:50, 20:40] = resonance_fs

sweepname = "M-R"
resonance = fdtd.getsweepresult(sweepname, "fs")  # Results are returned as Python dict
resonance_fs = resonance["fs"]
fs_all[0:50, 40:60] = resonance_fs

# -

k = np.linspace(1, 60, 60)
c = 3 * 10**8
for f in range(0, 50):
    plt.scatter(k, fs_all[f] * ax / c)
plt.xlabel("k (Gamma-X-M-R-Gamma")
plt.ylabel("Resonant Frequency f (Hz*a/c)")
plt.show()
