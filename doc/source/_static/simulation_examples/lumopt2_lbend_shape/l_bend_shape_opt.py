"""L-bend shape optimization.

Shape optimization of a 90-degree waveguide bend imported from GDS into a
layer builder object. The starting design is the 1 um radius bend used as the
starting point of the parametric L-bend example.

Prerequisites:
- Valid Lumerical FDTD license with Lumerical 2027 R1 release or newer.
"""

# ## Imports

from pathlib import Path

import numpy as np

import ansys.lumerical.core.lumopt2 as lmpt

# ## Material, simulation, geometry

# ### Input files

# The input waveguide enters from the left along y = 0 and the output waveguide leaves
# upward along x = 0. The GDS only contains a short piece of each waveguide,
# ending at x = -1.65 um and y = 1.65 um.

example_dir = Path(__file__).resolve().parent
gds_path = example_dir / "l_bend_pylumerical_start.gds"
lbr_path = example_dir / "lbend_process.lbr"
layer_name = "Layer_0"

# ### Waveguide parameters

wg_width = 0.5e-6
wg_height = 0.22e-6
wg_index = 3.5  # Matches the waveguide index in the process file
gds_wg_end = 1.65e-6  # Where the GDS waveguide ends meet the fixed waveguides
lead_length = 3e-6  # Long enough to pass through the FDTD boundary

# ### Wavelength

wavelengths = np.linspace(1.20e-6, 1.40e-6, 11)

# ### Simulation parameters

fdtd_span_x = 5e-6
fdtd_span_y = 5e-6
fdtd_span_z = 2.0e-6
mesh_size = 25e-9

port_in_x = -2e-6
port_out_y = 2e-6
port_span = 2.0e-6  # Port width transverse to the waveguide

# ### Base simulation

# Set up the FDTD region, the fixed input/output waveguides, ports, and the
# GDS layer builder


def generate_base_sim(fdtd):
    """Build the FDTD region, fixed waveguides, ports, and the GDS layer builder."""
    fdtd.addfdtd(
        {
            "x": 0,
            "y": 0,
            "z": 0,
            "x span": fdtd_span_x,
            "y span": fdtd_span_y,
            "z span": fdtd_span_z,
            "index": 1.5,  # Oxide cladding, matches the process file
            "mesh type": "uniform",
            "dx": mesh_size,
            "dy": mesh_size,
            "dz": mesh_size,
            "mesh refinement": "conformal variant 0",
        }
    )

    # Fixed waveguides that extend the short GDS waveguide ends through the ports and the boundary
    fdtd.addrect(
        {
            "name": "wg_in",
            "index": wg_index,
            "x min": -gds_wg_end - lead_length,
            "x max": -gds_wg_end,
            "y": 0,
            "y span": wg_width,
            "z": 0,
            "z span": wg_height,
        }
    )
    fdtd.addrect(
        {
            "name": "wg_out",
            "index": wg_index,
            "x": 0,
            "x span": wg_width,
            "y min": gds_wg_end,
            "y max": gds_wg_end + lead_length,
            "z": 0,
            "z span": wg_height,
        }
    )

    fdtd.addport({"name": "port_in"})
    fdtd.set("injection axis", "x")
    fdtd.set({"direction": "Forward", "x": port_in_x, "y": 0, "y span": port_span, "z span": fdtd_span_z})

    fdtd.addport({"name": "port_out"})
    fdtd.set("injection axis", "y")
    fdtd.set({"direction": "Backward", "x": 0, "y": port_out_y, "x span": port_span, "z span": fdtd_span_z})

    fdtd.setglobalsource("wavelength start", wavelengths[0])
    fdtd.setglobalsource("wavelength stop", wavelengths[-1])
    fdtd.setglobalmonitor("frequency points", len(wavelengths))
    fdtd.setnamed("FDTD::ports", "override global monitor settings", False)

    # Layer builder
    fdtd.addlayerbuilder({"x": 0, "x span": 4e-6, "y": 0, "y span": 4e-6, "z": 0})
    fdtd.loadgdsfile(str(gds_path))
    fdtd.loadprocessfile(str(lbr_path))
    fdtd.setnamed("layer group", "gds position reference", "Centered at origin")
    # Loading the GDS moves the layer builder, reset to origin
    fdtd.setnamed("layer group", "x", 0)
    fdtd.setnamed("layer group", "y", 0)


# ### Optimization region

# Vertices strictly inside this box are movable.
# Leave a short stub on each side for the waveguide connection.

stub_length = 0.1e-6

optimization_region = lmpt.Box(
    x_min=-gds_wg_end + stub_length,
    x_max=fdtd_span_x / 2 - 0.25e-6,
    y_min=-fdtd_span_y / 2 + 0.25e-6,
    y_max=gds_wg_end - stub_length,
    z_min=-wg_height,
    z_max=wg_height,
    mesh_size=mesh_size,
)

# ## Figure of merit

# Maximize the transmission into the output port over all simulated wavelengths.

fom = lmpt.Transmission("port_out")

# ## Design rules

# Prevent corners from getting too sharp.

rules = lmpt.DesignRules(min_angle=90)

# ## Run optimization

result = lmpt.optimize_shape(
    gds=gds_path,
    setup=generate_base_sim,
    layer=layer_name,
    region=optimization_region,
    fom=fom,
    rules=rules,
    output_gds="l_bend_shape_opt_output.gds",
    max_iterations=10,
)
