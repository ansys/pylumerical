# # Grating Coupler: ZBF2 Exportation
#
# Given a grating coupler design, this example demonstrates how to export its port data to Zemax ZBF2 format.
# This example will duplicate [this](https://optics.ansys.com/hc/en-us/articles/21008392675347-Integrated-microlens-and-grating-coupler-for-photonic-integrated-circuits)
# example in a much simpler way: `zbf2write` and `zbf2read` commands.
#
# This example is the **forth** part of the grating-coupler workflow:
# - Create a grating coupler: set up the base simulation and run it.
# - Optimize the grating coupler: improve the fiber position for better coupling efficiency.
# - Extract S-parameters: export S-parameters to INTERCONNECT.
# - Lumerical FDTD and Zemax connection: export monitor to ZBF2 and import ZBF2 as source.
#
# In this example, we will show:
# - How to export the port data to Zemax ZBF2 format
# - How to import a ZBF2 file as source
#
# We will only focus on exporting and importing the port data in Lumerical FDTD. The importing and exporting
# in Zemax will not be covered in this example.
#
# **Prerequisites**
#
# A valid Lumerical FDTD license is required.

# ### Import required modules and assign key parameters
#
# The grating coupler setup file can be obtained from following [Grating Coupler example](TODO: link)

# +
from pathlib import Path
from typing import OrderedDict

import matplotlib.pyplot as plt
import numpy as np

import ansys.lumerical.core as lumapi

# +
show_GUI = True
use_GPU_solver = True

# Path to load existing grating coupler setup file
fdtd_file_path = "your/path/to/grating_coupler_setup.fsp"
# Path to save the exported ZBF2 file
zbf2_write_path = "your/path/to/port1.zbf2"

# Unit conversion factors
um_to_m = 1e-6
m_to_um = 1e6

# Wavelength for single-frequency simulation
wavelength = 1.55 * um_to_m

# Speed of light defined in Lumerical
c = 299792458

# -
# ### Load FDTD simulation
#
# The grating coupler example setup has its port 1 as fiber port and port 2 as waveguide port.
# In this example, we will delete the fiber, put the port 1 inside the up cladding, and assign
# port 2 as the input port.
#
# We also need to set the global source to a single wavelength, as `zbf2write` only supports
# single frequency data.

# +
fdtd = lumapi.FDTD(hide=not show_GUI)
fdtd.load(fdtd_file_path)
fdtd.switchtolayout()

# Change global source to single wavelength
fdtd.setglobalsource("wavelength start", wavelength)
fdtd.setglobalsource("wavelength stop", wavelength)

# Change mesh accuracy from 1 to 2
fdtd.setnamed("FDTD", "mesh accuracy", 2)

# Select and delete the fiber structure group.
try:
    fdtd.unselectall()
    fdtd.select("fiber")
    fdtd.delete()  # Delete the fiber
except Exception:
    print("Fiber not found, skipping deletion.")

# Move the port 1 inside the up cladding, and flat
SiO2_TOX_z = fdtd.getnamed("SiO2 TOX", "z max")
port_1_properties = OrderedDict(
    {
        "z": SiO2_TOX_z - 0.1 * um_to_m,
        "theta": 0.0,
        "phi": 0.0,
        "rotation offset": 0.0,
    }
)
for key, value in port_1_properties.items():
    fdtd.setnamed("FDTD::ports::port 1", key, value)

# Change input port to specified port
fdtd.setnamed("FDTD::ports", "source port", "port 2")

# Save and run simulation
fdtd.save(str(Path(fdtd_file_path).with_name("grating_coupler_setup_zbf2.fsp")))
if use_GPU_solver:
    fdtd.run("FDTD", "GPU")
else:
    fdtd.run("FDTD", "CPU")
fdtd.save(str(Path(fdtd_file_path).with_name("grating_coupler_setup_zbf2.fsp")))

# -
# ### Extract result from port 1 and do zero-padding
#
# Zero-padding is recommended to keep more accurate spatial resolution when performing the
# zbf2 export. In this example we will export zbf2 data from both original field and two-times
# zero-padded field.


# +
def zero_padding_e(e: dict, times: int = 2) -> dict:
    """Zero-pad the E field by `times`, keeping the original field centered."""
    E_padded = e.copy()
    pad_width = []
    for key in ("x", "y"):
        coord = np.asarray(e[key])
        values = coord.reshape(-1)
        before = len(values) * times // 2
        after = len(values) * times - before
        padded_coord = np.concatenate(
            (
                values[0] - (values[3] - values[2]) * np.arange(before, 0, -1),  # use [3]-[2] instead of [1]-[0] to avoid smaller spacing at edge
                values,
                values[-1] + (values[-3] - values[-4]) * np.arange(1, after + 1),  # same
            )
        )
        E_padded[key] = padded_coord.reshape((-1,) + coord.shape[1:])
        pad_width.append((before, after))
    E_padded["E"] = np.pad(e["E"], pad_width + [(0, 0)] * 3)
    return E_padded


# +
port_name = "::model::FDTD::ports::port 1"
E_orig = fdtd.getresult(port_name, "E")
E_padded = zero_padding_e(e=E_orig, times=2)
zbf2_padded_write_path = zbf2_write_path.replace(".zbf2", "_2.zbf2")

# Print the shapes of the original E field components for verification.
print(
    f"E shape:{np.shape(E_orig['E'])}\n"
    f"f shape:{np.shape(E_orig['f'])}\n"
    f"x shape:{np.shape(E_orig['x'])}\n"
    f"y shape:{np.shape(E_orig['y'])}\n"
    f"z shape:{np.shape(E_orig['z'])}"
)


# Plot both fields
def plot_beams_ey2(
    orig_x: np.ndarray,
    orig_y: np.ndarray,
    orig_e: np.ndarray,
    padded_x: np.ndarray,
    padded_y: np.ndarray,
    padded_e: np.ndarray,
    title: str,
    x_label: str = "x (µm)",
    y_label: str = "y (µm)",
):
    """Plot the Ey intensity of the original and zero-padded E fields."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)
    for ax, x, y, field, sub_title in (
        (axes[0], orig_x, orig_y, orig_e, "Original field"),
        (axes[1], padded_x, padded_y, padded_e, "Zero-padded field"),
    ):
        mesh = ax.pcolormesh(
            x.flatten() / um_to_m,
            y.flatten() / um_to_m,
            np.abs(field.squeeze()[:, :, 1]).T ** 2,  # Ey intensity
            shading="nearest",
            cmap="turbo",
        )
        fig.colorbar(mesh, ax=ax, label="|Ey|^2")
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_aspect("equal")
        ax.set_title(sub_title)

    fig.suptitle(title)
    plt.show(block=False)


plot_beams_ey2(E_orig["x"], E_orig["y"], E_orig["E"], E_padded["x"], E_padded["y"], E_padded["E"], title="Port 1 |Ey|^2")

# -
# Port E field shape format: (x, y, z, f, 3), where the last dimensions correspond to Ex, Ey, Ez.
#
# <img src="images/origin_E_shape.png" width=250>
#
# <img src="images/port_fields.png" width=600>

# ### Export ZBF2 file
#
# Use `zbf2write` command to export the field data as `.zbf2` file. Please refer to
# [here](https://optics.ansys.com/hc/en-us/articles/52491782708755-zbf2write-Script-command) for
# more details.
#
# `rotation_matrix` will be included in the ZBF2 file metadata, representing the rotation of the beam.
# Because of the zero-padding, two ZBF2 files' beam propagation angle will be different. The larger
# the padding, the smaller the rotation angle deviation.


# +
def get_index(fdtd, name: str) -> float:
    """Get the refractive index of the specified component."""
    material = fdtd.getnamed(name, "material")
    if material == "<Object defined dielectric>":
        # Component defined with index
        index = fdtd.getnamed(name, "index")
    else:
        # Component defined with material
        f = c / wavelength  # frequency corresponding to the wavelength
        index = np.real(np.asarray(fdtd.getindex(material, f)).squeeze())
    return float(index)


port_position = np.array([fdtd.getnamed("FDTD::ports::port 1", axis) for axis in ("x", "y", "z")])

orig_zbf2 = {
    "beam": E_orig,
    "index": get_index(fdtd, "SiO2 TOX"),
    "position": port_position,
}
fdtd.zbf2write(zbf2_write_path, orig_zbf2)

zeropadded_zbf2 = {
    "beam": E_padded,
    "index": get_index(fdtd, "SiO2 TOX"),
    "position": port_position,
}
fdtd.zbf2write(zbf2_padded_write_path, zeropadded_zbf2)

# +
# Check the rotation angles of the two ZBF2 files
temp = fdtd.zbf2read(zbf2_write_path, 1, False)
rotation_angle = np.rad2deg(np.acos(temp["rotation_matrix"][0][0]))
print(f"Non-padding rotation angle: {rotation_angle:.4f}")

temp = fdtd.zbf2read(zbf2_padded_write_path, 1, False)
rotation_angle = np.rad2deg(np.acos(temp["rotation_matrix"][0][0]))
print(f"Zero-padded rotation angle: {rotation_angle:.4f}")

# -
# <img src="images/rotation_angles.png" width=250>

# ### Import ZBF2 file
#
# In practice, the ZBF2 file to import comes from Zemax OpticStudio. Here we re-import the file exported in Part 1
# as a stand-in. Please refer to [here](https://optics.ansys.com/hc/en-us/articles/52491623854867-zbf2read-Script-command)
# for more details.
#
# Ports and mode sources cannot take imported fields directly. Therefore, we
# 1. stop the ports from injecting; port 2 still records data, so it measures the coupling into the waveguide,
# 2. add an imported source at the ZBF2 position (port 1, whose index matches the ZBF2 index),
# 3. inject the beam downward toward the grating.


# +
def import_zbf2_and_set(fdtd, zbf2_file_path: str, source_name: str, save_file_path: str) -> np.ndarray:
    """Import a ZBF2 file and set the corresponding imported source in FDTD."""
    # Import the raw ZBF2 data with the rotation matrix applied
    zbf2_raw = fdtd.zbf2read(zbf2_file_path, 1, True)
    beam = zbf2_raw["beam"]
    position = zbf2_raw["position"]

    # Assign the imported beam to the source
    fdtd.select(source_name)
    fdtd.importdataset(beam)  # applies to the selected object

    fdtd.setnamed(source_name, "direction", "Backward")  # down toward the grating
    for axis, value in zip(("x", "y", "z"), np.asarray(position).ravel()):
        fdtd.setnamed(source_name, axis, value)

    # Save and run
    fdtd.save(save_file_path)
    fdtd.run()
    fdtd.save(save_file_path)

    # Collect the waveguide E field from port 2
    waveguide_E = fdtd.getresult("FDTD::ports::port 2", "E")

    return beam, waveguide_E


# +
fdtd.switchtolayout()
fdtd.setnamed("FDTD::ports", "source port", "")  # ports only record data now
fdtd.addimportedsource(name="zbf2_source")

# Set up each imported source and run simulations, this may take some time.
file_path = str(Path(fdtd_file_path).with_name("grating_coupler_orig_zbf2.fsp"))
orig_beam, orig_waveguide_beam = import_zbf2_and_set(fdtd=fdtd, zbf2_file_path=zbf2_write_path, source_name="zbf2_source", save_file_path=file_path)

fdtd.switchtolayout()
file_path = str(Path(fdtd_file_path).with_name("grating_coupler_padded_zbf2.fsp"))
padded_beam, padded_waveguide_beam = import_zbf2_and_set(
    fdtd=fdtd, zbf2_file_path=zbf2_padded_write_path, source_name="zbf2_source", save_file_path=file_path
)

# +
plot_beams_ey2(orig_beam["x"], orig_beam["y"], orig_beam["E"], padded_beam["x"], padded_beam["y"], padded_beam["E"], title="Imported |Ey|^2")

plot_beams_ey2(
    orig_waveguide_beam["y"],
    orig_waveguide_beam["z"],
    orig_waveguide_beam["E"],
    padded_waveguide_beam["y"],
    padded_waveguide_beam["z"],
    padded_waveguide_beam["E"],
    title="Waveguide |Ey|^2",
    x_label="y (µm)",
    y_label="z (µm)",
)

# -
# <img src="images/import_fields.png" width=600>
#
# <img src="images/waveguide_fields.png" width=600>
#
# Please note that the two monitors images (port 1's before export and waveguide's after import & simulation)
# are in global coordinate systems, yet the importsource's local coordinate system is used for the imported
# beam, making its x- and y-axes symmetric about zero.

# +
# Close the simulation properly.
if not show_GUI:
    fdtd.close()
