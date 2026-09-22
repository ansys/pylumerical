# # Grating Coupler
#
# Define a grating coupler that connects a single-mode fiber on a photonic chip surface to an integrated waveguide.
#
# This example is part of the grating-coupler workflow:
# - Create a grating coupler: set up the base simulation and run it.
# - Optimize the grating coupler: improve the grating geometry for better coupling efficiency.
# - Extract S-parameters: export S-parameters to Interconnect.
# - Lumerical FDTD and Zemax Interconnect: export the field to ZBF for import into Zemax.
#
# In this example, we will show:
# - How to set up a structure group
# - How to set up a custom object
# - How to copy an object
# - How to edit the properties of multiple objects
#
# ## Prerequisites
#
# Valid FDTD and MODE licenses are required.
#
# ### Perform required imports

from collections import OrderedDict
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np

import ansys.lumerical.core as lumapi

#
# ### Assign key parameters

# +

show_GUI = True
file_name = "./grating_coupler_setup.fsp"

# Unit
um_to_m = 1e-6

# Materials
MATERIAL_SIO2 = "SiO2 (Glass) - Palik"
MATERIAL_SI = "Si (Silicon) - Palik"

# FDTD region
fdtd_region = OrderedDict(
    {
        "dimension": "3D",
        "x": -5 * um_to_m,
        "x span": 42 * um_to_m,  # x min = -26um, x max = 16um
        "y": 0,
        "y span": 20 * um_to_m,  # y min = -10um, y max = 10um
        "z min": -1.2 * um_to_m,
        "z max": 1.3 * um_to_m,
        "x min bc": "PML",
        "x max bc": "PML",
        "y min bc": "Anti-Symmetric",
        "y max bc": "PML",
        "z min bc": "PML",
        "z max bc": "PML",
        "pml profile": 1,  # standard
        "pml layers": 8,
    }
)

# Global source (wavelength range)
source_properties = OrderedDict(
    {
        "set wavelength": 1,
        "wavelength start": 1.5 * um_to_m,
        "wavelength stop": 1.6 * um_to_m,
        "optimize for short pulse": 1,
    }
)

# Global monitor (frequency points)
monitor_properties = OrderedDict(
    {
        "use source limits": 1,
        "frequency points": 50,
    }
)

# Simulation items
# SiO2 TOX (top oxide)
sio2_tox = OrderedDict(
    {
        "name": "SiO2 TOX",
        "x": 0.0,
        "x span": 120 * um_to_m,
        "y": 0.0,
        "y span": 120 * um_to_m,
        "z min": 0.0,
        "z max": 0.7 * um_to_m,
        "material": MATERIAL_SIO2,
        "override mesh order from material database": 1,  # enable custom mesh order for better accuracy
        "mesh order": 3,
        "override color opacity from material database": 1,  # optional, enable custom opacity for better visualization
        "alpha": 0.25,
    }
)
# SiO2 BOX (buried oxide)
sio2_box = OrderedDict(
    {
        "name": "SiO2 BOX",
        "x": 0.0,
        "x span": 120 * um_to_m,
        "y": 0.0,
        "y span": 120 * um_to_m,
        "z min": -1 * um_to_m,
        "z max": 0,
        "material": MATERIAL_SIO2,
    }
)
# Si substrate
si_substrate = OrderedDict(
    {
        "name": "Si substrate",
        "x": 0.0,
        "x span": 120 * um_to_m,
        "y": 0.0,
        "y span": 120 * um_to_m,
        "z min": -4 * um_to_m,
        "z max": -1 * um_to_m,
        "material": MATERIAL_SI,
    }
)

# --- Monitors ---
xz_monitor = OrderedDict(
    {
        "name": "xz_monitor",
        "monitor type": "2D Y-normal",
        "x min": -26 * um_to_m,
        "x max": 16 * um_to_m,
        "y": 0,
        "z min": -1.2 * um_to_m,
        "z max": 1.3 * um_to_m,
        "override global monitor settings": 1,
        "use source limits": 1,
        "frequency points": 1,
    }
)
movie_monitor = OrderedDict(
    {
        "name": "movie",
        "monitor type": "2D Z-normal",
        "x min": -27.5 * um_to_m,
        "x max": 17.5 * um_to_m,
        "y": 0,
        "y span": 23 * um_to_m,
        "horizontal resolution": 320,
        "scale": 1,
    }
)
index_monitor = OrderedDict(
    {
        "name": "monitor",
        "monitor type": "2D Y-normal",
        "x": -5 * um_to_m,
        "x span": 42 * um_to_m,
        "y": 0,
        "z min": -1.2 * um_to_m,
        "z max": 1.3 * um_to_m,
    }
)

# +
# Set up the parameters for the grating and fiber structures.

# --- Grating structure group ---
grating_variables = {
    "target length": 25 * um_to_m,
    "h total": 0.22 * um_to_m,
    "etch depth": 0.1 * um_to_m,
    "duty cycle": 0.3992,
    "pitch": 0.6713 * um_to_m,
    "radius": 25 * um_to_m,
    "y span": 15 * um_to_m,
    "L extra": 10 * um_to_m,
    "waveguide width": 0.5 * um_to_m,
    "material": MATERIAL_SI,
    "m": 1.15,
    "waveguide length": 10 * um_to_m,
}

# --- Fiber structure group ---
fiber_variables = {
    "core diameter": 9 * um_to_m,
    "cladding diameter": 50 * um_to_m,
    "z span": 20 * um_to_m,
    "theta": 10.0,  # deg, fiber tilt
    "core index": 1.44427,
    "cladding index": 1.43482,
}

# -

# ### Step 1: Set up simple objects


# +
def set_up_simple_objects(
    lum_obj,
    fdtd_region: OrderedDict,
    source_properties: Dict,
    monitor_properties: Dict,
    rect_objects: tuple[OrderedDict],
    xz_monitor: OrderedDict,
    movie_monitor: OrderedDict,
    index_monitor: OrderedDict,
    file_name: str,
) -> None:
    """
    Set up a simple FDTD simulation with the given objects and monitors.

    Parameters
    ----------
    lum_obj: Lumerical FDTD object
    fdtd_region: OrderedDict containing FDTD region properties
    source_properties: Dict containing global source properties
    monitor_properties: Dict containing global monitor properties
    rect_objects: tuple of OrderedDicts containing rectangular object properties
    xz_monitor: OrderedDict containing XZ plane monitor properties
    movie_monitor: OrderedDict containing movie monitor properties
    index_monitor: OrderedDict containing index monitor properties
    """
    # Start from an empty project
    lum_obj.switchtolayout()
    lum_obj.deleteall()

    # --- 1. FDTD region ---
    lum_obj.addfdtd(properties=fdtd_region)

    # --- 2. Global source / monitor settings ---
    for key, value in source_properties.items():
        lum_obj.setglobalsource(key, value)

    for key, value in monitor_properties.items():
        lum_obj.setglobalmonitor(key, value)

    # --- 3. Cladding / substrate stack ---
    for obj in rect_objects:
        lum_obj.addrect(properties=obj)

    # --- 4. Monitors ---
    lum_obj.adddftmonitor(properties=xz_monitor)  # DFT (frequency-domain) monitor
    lum_obj.addmovie(properties=movie_monitor)  # movie monitor
    lum_obj.addindex(properties=index_monitor)  # index monitor

    lum_obj.save(file_name)


# Open Lumerical FDTD window
fdtd = lumapi.FDTD(hide=not show_GUI)

set_up_simple_objects(
    lum_obj=fdtd,
    fdtd_region=fdtd_region,
    source_properties=source_properties,
    monitor_properties=monitor_properties,
    rect_objects=(sio2_tox, sio2_box, si_substrate),
    xz_monitor=xz_monitor,
    movie_monitor=movie_monitor,
    index_monitor=index_monitor,
    file_name=file_name,
)

# -
# <img src="images/setup1_basic.png" width="600">

# ### Step 2: Set up structure groups: grating

# +
# Calculate intermediate parameters
n_periods = int(grating_variables["target length"] / grating_variables["pitch"])
fill_width = float(grating_variables["pitch"] * grating_variables["duty cycle"])
etch_width = float(grating_variables["pitch"] * (1 - grating_variables["duty cycle"]))
L = float(n_periods * grating_variables["pitch"] + etch_width)
theta = np.arcsin(0.5 * grating_variables["y span"] / grating_variables["radius"]) * 180 / np.pi

obj_list = []
obj_type_list = []

# Define each object.
# Waveguide
waveguide = OrderedDict(
    {
        "name": "waveguide",
        "x min": -grating_variables["waveguide length"],
        "x max": 0,
        "y": 0,
        "y span": grating_variables["waveguide width"],
        "z min": 0,
        "z max": grating_variables["h total"],
    }
)
obj_list.append(waveguide)
obj_type_list.append("rect")

# Taper section
x_span = grating_variables["radius"] * np.cos(theta * np.pi / 180)
L_taper = x_span
w1 = grating_variables["waveguide width"] / 2
w2 = grating_variables["y span"] / 2
x0 = L_taper / 2
alpha = (w1 - w2) / L_taper ** grating_variables["m"]
equation = f"{alpha} * ({x0} - x)^{grating_variables['m']} + {w2}"
taper_section = OrderedDict(
    {
        "name": "taper",
        "x min": 0,
        "x max": grating_variables["radius"] * np.cos(theta * np.pi / 180),
        "z min": 0,
        "z max": grating_variables["h total"],
        "y span": grating_variables["y span"],
        "equation 1": equation,
        "equation units": "m",
    }
)
obj_list.append(taper_section)
obj_type_list.append("custom")

# Input section
input_section = OrderedDict(
    {
        "name": "input section",
        "inner radius": grating_variables["radius"] * np.cos(theta * np.pi / 180),
        "outer radius": grating_variables["radius"],
        "x": 0,
        "y": 0,
        "z min": 0,
        "z max": grating_variables["h total"],
        "theta start": -theta,
        "theta stop": theta,
    }
)
obj_list.append(input_section)
obj_type_list.append("ring")

# Add each grating period
for i in range(n_periods):
    grating_item = OrderedDict(
        {
            "name": f"ring{i}",  # start from 0
            "x": 0,
            "y": 0,
            "z min": grating_variables["h total"] - grating_variables["etch depth"],
            "z max": grating_variables["h total"],
            "theta start": -theta,
            "theta stop": theta,
            "inner radius": grating_variables["radius"] + grating_variables["pitch"] * i + etch_width,
            "outer radius": grating_variables["radius"] + grating_variables["pitch"] * (i + 1),
        }
    )
    obj_list.append(grating_item)
    obj_type_list.append("ring")


#  +
# Function to add objects to a group in the FDTD simulation
def add_objs_to_group(
    lum_obj, group_name: str, obj_list: list[OrderedDict], obj_type_list: list[str], file_name: str, name_in_group: list[str] = []
) -> list[str]:
    """
    Add objects to a specified group in the FDTD simulation.

    Parameters
    ----------
    lum_obj: The FDTD simulation object.
    group_name (str): The name of the group to add objects to.
    obj_list (list[OrderedDict]): A list of object properties.
    obj_type_list (list[str]): A list of object types corresponding to the objects in obj_list.
    file_name (str): The name of the file to save the simulation to.
    name_in_group (list[str], optional): A list to store the names of objects in the group. Defaults to an empty list.

    Returns
    -------
    list[str]: The updated list of names of objects in the group.
    """
    # Switch to layout mode
    lum_obj.switchtolayout()

    # Add objects
    for obj, obj_type in zip(obj_list, obj_type_list):
        match obj_type:
            case "rect":
                lum_obj.addrect(properties=obj)
            case "custom":
                lum_obj.addcustom(properties=obj)
            case "ring":
                lum_obj.addring(properties=obj)
            case "circle":
                lum_obj.addcircle(properties=obj)
            case _:
                raise ValueError(f"Unsupported object type: {obj_type}")

        lum_obj.addtogroup(group_name)
        name_in_group.append(f"{group_name}::{obj['name']}")

    # Save
    lum_obj.save(file_name)

    return name_in_group


grating_names = add_objs_to_group(lum_obj=fdtd, group_name="grating", obj_list=obj_list, obj_type_list=obj_type_list, file_name=file_name)

# +
# This example shows how to copy an item and modify a few of its properties.
# Lower layer beneath the grating
if grating_variables["etch depth"] < grating_variables["h total"]:
    lower_layer = OrderedDict(
        {
            "name": "lower layer",
            "inner radius": grating_variables["radius"],
            "outer radius": grating_variables["radius"] + L,
            "z min": 0,
            "z max": grating_variables["h total"] - grating_variables["etch depth"],
        }
    )

    fdtd.select("grating::input section")
    fdtd.copy()
    for key, value in lower_layer.items():
        fdtd.set(key, value)

    # The new item is already in the group because it was copied from a grouped item.
    grating_names.append("grating::lower layer")

# Output section
output_section = OrderedDict(
    {
        "name": "output section",
        "inner radius": grating_variables["radius"] + L,
        "outer radius": grating_variables["radius"] + L + grating_variables["L extra"],
        "z min": 0,
        "z max": grating_variables["h total"],
    }
)
fdtd.select("grating::input section")
fdtd.copy()
for key, value in output_section.items():
    fdtd.set(key, value)
grating_names.append("grating::output section")

fdtd.save(file_name)

# +
# This example shows how to set properties for multiple structures.
shared_properties = OrderedDict(
    {
        "material": grating_variables["material"],
    }
)
for structure_name in grating_names:
    # `setnamed` can only set one property at a time
    for key, value in shared_properties.items():
        fdtd.setnamed(structure_name, key, value)
    # Move each item
    current_x = fdtd.getnamed(structure_name, "x")
    fdtd.setnamed(structure_name, "x", current_x - grating_variables["radius"])

fdtd.save(file_name)

# -
# <img src="images/setup2_grating.png" width="600">

# ### Step 3: Set up structure group: fiber

# +
# Calculate intermediate parameters
core_radius = float(fiber_variables["core diameter"] / 2)
cladding_radius = float(fiber_variables["cladding diameter"] / 2)
fiber_theta_rad = np.deg2rad(fiber_variables["theta"])
L = float(fiber_variables["z span"] / np.cos(fiber_theta_rad))

core = OrderedDict(
    {
        "name": "core",
        "radius": core_radius,
        "x": 0,
        "y": 0,
        "z": 0,
        "z span": L,
        "material": "<Object defined dielectric>",  # object-defined material
        "index": float(fiber_variables["core index"]),  # refractive index
        "first axis": "y",
        "rotation 1": float(fiber_variables["theta"]),
        "override mesh order from material database": 1,  # enable custom mesh order for better accuracy
        "mesh order": 4,
    }
)

cladding = OrderedDict(
    {
        "name": "cladding",
        "radius": cladding_radius,
        "material": "<Object defined dielectric>",
        "index": float(fiber_variables["cladding index"]),
        "x": 0,
        "y": 0,
        "z": 0,
        "z span": L,
        "first axis": "y",
        "rotation 1": float(fiber_variables["theta"]),
        "override mesh order from material database": 1,  # enable custom mesh order for better accuracy
        "mesh order": 5,
        "override color opacity from material database": 1,  # optional, enable custom opacity for better visualization
        "alpha": 0.35,
    }
)

add_objs_to_group(lum_obj=fdtd, group_name="fiber", obj_list=[core, cladding], obj_type_list=["circle", "circle"], file_name=file_name)

fdtd.setnamed("fiber", "x", 2.74533 * um_to_m)
fdtd.save(file_name)

# -
# <img src="images/setup3_fiber.png" width="600">

# ### Step 4: Set up the ports as sources
#
# Use a standard dictionary `{}` rather than `OrderedDict({})` when defining ports, because ports are treated as structures inside Lumerical.

# +
# Assign parameter
tox_offset = 0.65 * um_to_m

# Get values of existing structures
fiber_x_pos = fdtd.getnamed("fiber", "x")
fiber_y_pos = fdtd.getnamed("fiber", "y")
fiber_z_pos = fdtd.getnamed("fiber", "z")
tox_z_pos = fdtd.getnamed("SiO2 TOX", "z")


def get_diameter(name: str) -> float:
    """Get the radius, calculate the diameter, and return it. Returns None if an error occurs."""
    try:
        radius = fdtd.getnamed(name, "radius")
        diameter = 2 * radius
        return diameter
    except Exception as e:
        print(f"Error getting diameter for {name}: {e}")
        return None


# Calculate intermediate
port_x_pos = fiber_x_pos + tox_offset * np.sin(fiber_theta_rad)
port_z_pos = tox_z_pos + fiber_z_pos + tox_offset * np.cos(fiber_theta_rad)
port_offset = 4.0 * get_diameter(name="fiber::core") * np.tan(fiber_theta_rad)

port_1 = {
    "name": "port 1",
    "injection axis": "z-axis",
    "direction": "Backward",
    "x": port_x_pos,
    "x span": 20 * um_to_m,
    "y": fiber_y_pos,
    "y span": 20 * um_to_m,
    "z": port_z_pos,
    "theta": float(fiber_variables["theta"]),
    "rotation offset": port_offset,
}

port_2 = {
    "name": "port 2",
    "injection axis": "x-axis",
    "direction": "Forward",
    "x": -25.5 * um_to_m,
    "y": 0,
    "y span": 2.5 * um_to_m,
    "z": 0.05 * um_to_m,
    "z span": 2.25 * um_to_m,
}

fdtd.addport(port_1)
fdtd.addport(port_2)

fdtd.save(file_name)

# -
# <img src="images/setup4_final.png" width="600">

# ### Step 5: Run the simulation and plot the results
#
# The simulation may take approximately 20 minutes to complete.

# +
# Run the simulation and save the results
fdtd.run()
fdtd.save(file_name)


# +
# Extract data from monitors
def extract_result_xz_mesh(results, key: str):
    """Extract x, z mesh and the specified field from the results dictionary."""
    x_um = np.asarray(results["x"]).squeeze() * 1e6
    z_um = np.asarray(results["z"]).squeeze() * 1e6
    x_mesh, z_mesh = np.meshgrid(x_um, z_um)
    value = np.asarray(results[key]).squeeze()
    return x_mesh, z_mesh, value


xz_result = fdtd.getresult("xz_monitor", "E")
x_mesh, z_mesh, E = extract_result_xz_mesh(xz_result, "E")
Ey_abs = np.abs(E[:, :, 1].transpose())

index_result = fdtd.getresult("monitor", "index")
idx_x_mesh, idx_z_mesh, index_y = extract_result_xz_mesh(index_result, "index_y")
index_y_real = np.real(index_y.transpose())

# +
# plot
fig, axes = plt.subplots(2, 1, figsize=(12, 4), constrained_layout=True)

ey_plot = axes[0].pcolormesh(x_mesh, z_mesh, Ey_abs, shading="auto", cmap="viridis")
ey_colorbar = fig.colorbar(ey_plot, ax=axes[0], pad=0.01)
ey_colorbar.set_label("amplitude (a.u.)", rotation=270, labelpad=-35)
axes[0].set_title("|Ey|")
axes[0].set_aspect("equal")
axes[0].set_xlabel("x (um)")
axes[0].set_ylabel("z (um)")

index_plot = axes[1].pcolormesh(idx_x_mesh, idx_z_mesh, index_y_real, shading="auto", cmap="viridis")
index_colorbar = fig.colorbar(index_plot, ax=axes[1], pad=0.01)
index_colorbar.set_label("n", rotation=270, labelpad=-35)
axes[1].set_title("Index (y)")
axes[1].set_aspect("equal")
axes[1].set_xlabel("x (um)")
axes[1].set_ylabel("z (um)")

plt.show(block=False)

# -
# <img src="images/grating_coupler_results.png" width="600">

# +
# Close the simulation properly.
if not show_GUI:
    fdtd.close()
