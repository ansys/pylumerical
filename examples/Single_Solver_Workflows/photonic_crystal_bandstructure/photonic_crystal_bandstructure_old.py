# # Photonic Crystal Bandstructure (FDTD)
#
# This example demonstrates a photonic crystal simulation utilizing a built-in Structure Group object. Based on: https://optics.ansys.com/hc/en-us/articles/360041566614-Rectangular-Photonic-Crystal-Bandstructure 
#
#
# In Part 1, we build the structure and set the FDTD simulation region. In this case, the spheres are holes (filled with air, n = 1) and the background material is a simple dielectric material. Some advanced simulation objects, including the photonic crystal array and bandstructure analysis groups, are imported from the Object Library. We run a single simulation and visualize the resulting spectrum. 
#
# In Part 2, we set up a series of sweeps to collect the resonant frequencies. In this example, we use the built-in sweep tool in Lumerical, but the parameter sweeps could also be set up from Python. We then run the sweeps and plot the results. 
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

# Part 1: Set up structures and simulation objects

# <img src="images/simulation_screenshot.png" width="600">

# +
# Define parameters

# Set filename for saving and loading
filename = 'photonic_pc_bandstructure.fsp'

# set desired period of the array (3D)
ax = 0.5e-6
ay = 0.5e-6
az = 0.5e-6

# number of spheres in each direction
nx = 3
ny = 3
nz = 3

sphere_radius = 0.25e-6
sphere_index = 1 # Specify index if "Object defined dielectric" is used; otherwise, specify material from database below
sphere_material = "etch" # Etch n = 1 (air)
background_index = 3.6055

# Define frequencies / wavelengths of interest
f1 = 1e12 # THz
f2 = 220e12 # THz

# +
# Initialize session and build simulation objects. Set hide = True to hide the Lumerical GUI. 
# This block will build an array of spheres for the photonic crystal structure. 
# We add an FDTD region, sources, and monitors. The sources and monitors are imported from the Object Library. 
# Finally, the simulation file is saved to the file name set earlier.

with lumapi.FDTD(hide = False) as fdtd:

    # Add rectangular lattice array of spheres
    # Note you can also use Lumerical's built-in "rect_pc_3D" object using fdtd.addobject("rect_pc_3D")
    # In this example, we construct the array programmatically
    fdtd.addstructuregroup({"name": "rect_pc_3D"})
    for ix, iy, iz in itertools.product(*map(range, (nx,ny,nz))):
        objname = f"c{ix}{iy}{iz}"
        fdtd.addsphere({"name": objname, "x":(ix-1)*ax, "y":(iy-1)*ay, "z":(iz-1)*az, "radius":sphere_radius, "material":sphere_material})
        fdtd.addtogroup("rect_pc_3D") # Adds the recently created sphere to the structure group

    # Add FDTD region
    dx = 0.025e-6 # Mesh dx, dy, dz
    fdtd_geometry_props = {"x": 0, "x span" : ax, "y": 0, "y span" : ay, "z": 0, "z span" : az}
    fdtd_mesh_props = {"index" : background_index, "mesh type": "uniform", "dx": dx, "dy": dx, "dz": dx}
    fdtd_boundary_props = {"x min bc" : "Bloch", "y min bc" : "Bloch", "z min bc": "Bloch", "set based on source angle": False, "bloch units": "SI"}
    # Combine properties settings into one dictionary
    fdtd_props = OrderedDict({**fdtd_geometry_props, **fdtd_mesh_props, **fdtd_boundary_props})

    fdtd.addfdtd(properties = fdtd_props)

    # Set up sources (dipole cloud) and monitors (bandstructure)
    # These are both Analysis Groups available from the object library
    dipole_geometry_props = {"n dipoles": 3, "lattice type": 3, "z span": az, "ax" : ax, "ay": ay, "az" : az, "a": az, "x": 0, "y": 0, "z": 0}
    dipole_frequency_props = {"f1": f1, "f2": f2, "kx": 0.5, "ky": 0, "kz": 0}
    dipole_props = OrderedDict({**dipole_geometry_props, **dipole_frequency_props})

    fdtd.addobject("dipole_cloud", properties = dipole_props)

    bandstructure_geometry_props = {"n monitors": 10, "x": 0, "x span" : ax, "y": 0, "y span" : ay, "z": 0, "z span" : az}
    bandstructure_frequency_props = {"f1": f1, "f2": f2}
    bandstructure_props = OrderedDict({**bandstructure_geometry_props, **bandstructure_frequency_props})
    fdtd.addobject("bandstructure", properties = bandstructure_props)

    # zoom CAD view around simulation region
    fdtd.select("FDTD")
    fdtd.setview("extent")

    fdtd.save(filename)
    print("File saved to folder as: " + filename)

# +
# Open the file and run a single simulation. Visualize the spectrum. 

with lumapi.FDTD(filename, hide = False) as fdtd:
    print("Simulation running...")
    fdtd.run()
    print("Run completed. Analyzing and plotting results...")
    fdtd.runanalysis()

    # Plot results
    single_spectrum = fdtd.getresult("bandstructure","spectrum")
    spectrum = single_spectrum["fd"]
    frequencies = single_spectrum['f']

    plt.plot(frequencies,spectrum)
    plt.title("Single Simulation Spectrum")
    plt.xlabel("Frequency")
    plt.show()
# -

# <img src="images/single_spectrum.png" width="600">

# Part 2: Set up and run sweeps to extract resonant frequencies and plot the bandstructure 

# +
# Normalization factor for SI units; see note above. 
norm_x = 2*np.pi/ax
norm_y = 2*np.pi/ay
norm_z = 2*np.pi/az

# The total number of simulations will be num_points ^ 3
num_points = 3

# Define a function to add the sweeps
def add_bandstructure_sweep(sweep_name, x_start, x_stop, y_start, y_stop, z_start, z_stop):
    fdtd.addsweep()
    fdtd.setsweep("sweep", "name", sweep_name)
    fdtd.setsweep(sweep_name, "type", "Ranges")
    fdtd.setsweep(sweep_name, "number of points", num_points)

    # set the sweep properties
    props_kx = {"Name":"kx","Parameter":"::model::FDTD::kx","Type":"Number", "Start": x_start, "Stop": x_stop }
    fdtd.addsweepparameter(sweep_name,props_kx)
    props_ky = {"Name":"ky","Parameter":"::model::FDTD::ky","Type":"Number", "Start": y_start, "Stop": y_stop}
    fdtd.addsweepparameter(sweep_name,props_ky)
    props_kz = {"Name":"kz","Parameter":"::model::FDTD::kz","Type":"Number", "Start": z_start, "Stop": z_stop}
    fdtd.addsweepparameter(sweep_name,props_kz)

    # define results 

# Add Gamma-X sweep
add_bandstructure_sweep("Gamma-X", 0*norm_x, 0.5*norm_x, 0*norm_y, 0*norm_y, 0*norm_z, 0*norm_z)


# +
# Normalization factor for SI units; see note above. 
norm_x = 2*np.pi/ax
norm_y = 2*np.pi/ay
norm_z = 2*np.pi/az

# Add Gamma-X sweep

fdtd.addsweep()
fdtd.setsweep("sweep", "name", "Gamma-X")
fdtd.setsweep("Gamma-X", "type", "Ranges")
fdtd.setsweep("Gamma-X", "number of points", 20)

# set the sweep properties
props_kx = {"Name":"kx","Parameter":"::model::FDTD::kx","Type":"Number", "Start": 0*norm_x,"Stop":0.5*norm_x }
fdtd.addsweepparameter("Gamma-X",props_kx)
props_ky = {"Name":"ky","Parameter":"::model::FDTD::ky","Type":"Number", "Start": 0*norm_y,"Stop":0*norm_y }
fdtd.addsweepparameter("Gamma-X",props_ky)
props_kz = {"Name":"kz","Parameter":"::model::FDTD::kz","Type":"Number", "Start": 0*norm_z,"Stop":0*norm_z }
fdtd.addsweepparameter("Gamma-X",props_kz)

# define results 
result_fs = {"Name":"fs","Result":"::model::bandstructure::fs"}
fdtd.addsweepresult("Gamma-X", result_fs)
result_spectrum = {"Name":"fs","Result":"::model::bandstructure::spectrum"}
fdtd.addsweepresult("Gamma-X", result_spectrum);

# Add X-M sweep

fdtd.addsweep()
fdtd.setsweep("sweep", "name", "X-M")
fdtd.setsweep("X-M", "type", "Ranges")
fdtd.setsweep("X-M", "number of points", 20)

# set the sweep properties
props_kx = {"Name":"kx","Parameter":"::model::FDTD::kx","Type":"Number", "Start": 0.5*norm_x,"Stop":0.5*norm_x }
fdtd.addsweepparameter("X-M",props_kx)
props_ky = {"Name":"ky","Parameter":"::model::FDTD::ky","Type":"Number", "Start": 0*norm_y,"Stop":0.5*norm_y }
fdtd.addsweepparameter("X-M",props_ky)
props_kz = {"Name":"kz","Parameter":"::model::FDTD::kz","Type":"Number", "Start": 0*norm_z,"Stop":0*norm_z }
fdtd.addsweepparameter("X-M",props_kz)

# define results 
result_fs = {"Name":"fs","Result":"::model::bandstructure::fs"}
fdtd.addsweepresult("X-M", result_fs)
result_spectrum = {"Name":"fs","Result":"::model::bandstructure::spectrum"}
fdtd.addsweepresult("X-M", result_spectrum);

# Add M-R sweep

fdtd.addsweep()
fdtd.setsweep("sweep", "name", "M-R")
fdtd.setsweep("M-R", "type", "Ranges")
fdtd.setsweep("M-R", "number of points", 20)

# set the sweep properties
props_kx = {"Name":"kx","Parameter":"::model::FDTD::kx","Type":"Number", "Start": 0.5*norm_x,"Stop":0.5*norm_x }
fdtd.addsweepparameter("M-R",props_kx)
props_ky = {"Name":"ky","Parameter":"::model::FDTD::ky","Type":"Number", "Start": 0.5*norm_y,"Stop":0.5*norm_y }
fdtd.addsweepparameter("M-R",props_ky)
props_kz = {"Name":"kz","Parameter":"::model::FDTD::kz","Type":"Number", "Start": 0*norm_z,"Stop":0.5*norm_z }
fdtd.addsweepparameter("M-R",props_kz)

# define results 
result_fs = {"Name":"fs","Result":"::model::bandstructure::fs"}
fdtd.addsweepresult("M-R", result_fs)
result_spectrum = {"Name":"fs","Result":"::model::bandstructure::spectrum"}
fdtd.addsweepresult("M-R", result_spectrum);

# +
# Run all the sweeps - this may take a few minutes
fdtd.runsweep() 

# If you have previously run the sweeps, you can load them using this line instead:
#fdtd.loadsweep()


# +
# Retrieve and analyze data from the sweeps
fs_all = np.zeros((50, 60)); # 50 is the number of frequencies, and 60 bandstructure points = 20 points per sweep x 3 sweeps

sweepname = "Gamma-X";
resonance = fdtd.getsweepresult(sweepname, "fs") # Results are returned as Python dict
resonance_fs = resonance["fs"]
fs_all[0:50, 0:20] = resonance_fs

sweepname = "X-M";
resonance = fdtd.getsweepresult(sweepname, "fs") # Results are returned as Python dict
resonance_fs = resonance["fs"]
fs_all[0:50, 20:40] = resonance_fs

sweepname = "M-R";
resonance = fdtd.getsweepresult(sweepname, "fs") # Results are returned as Python dict
resonance_fs = resonance["fs"]
fs_all[0:50, 40:60] = resonance_fs

# -



k = np.linspace(1,60,60)
c= 3*10**8
for f in range(0,50):
    plt.scatter(k,fs_all[f]*ax/c)
plt.xlabel("k (Gamma-X-M-R-Gamma")
plt.ylabel("Resonant Frequency f (Hz*a/c)")
plt.show()

# <img src="images/bandstructure.png" width="600">