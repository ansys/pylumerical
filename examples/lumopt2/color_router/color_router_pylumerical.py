# # Inverse design of a color router lens using lumopt2
#
# An example of using lumopt2 to conduct parametric optimization for a color router lens.
# The example uses a 3D FDTD simulation with pillars in air to route red, green, and blue light to different pixels,
# forming the basis of a color router.
#
# Prerequisites:
# - Valid Lumerical FDTD license with Lumerical 2026 R1.2 release or newer.

# <img src="images/color_router_schematics.png" width="80%">

# ## Imports

from collections import OrderedDict
from dataclasses import dataclass
import math
from typing import Any, ClassVar

import autograd.numpy as anp
from lumopt2.utils.panels import MonitorPanel, PanelState
import numpy as np

import ansys.lumerical.core as lumapi
import ansys.lumerical.core.lumopt2 as lmpt

# ## Definitions

# ### Base simulation class
# This class defines general setup for the structure, and utility functions for setting up different configurations.


class MetalensCis:
    """FDTD simulation geometry for a metasurface color router with pillars in air.

    A substrate is added but its index is set to 1.0.

    Defines the FDTD region, Gaussian source, field monitors,
    and pillar (cylinder) array for a four-channel (red, green1, green2,
    blue) color router. Configurator methods allow switching the global
    source wavelength via multi-configuration.
    """

    def __init__(
        self,
        bg_index,
        pixel_size,
        sub_depth,
        focal_length,
        meta_height,
        meta_size,
        meta_pitch,
        red_wavelength,
        blue_wavelength,
        green1_wavelength,
        green2_wavelength,
        mesh_dx=0.025e-6,
        mesh_dy=0.025e-6,
        mesh_dz=0.025e-6,
        pva_level=4,
        meta_index=None,
        meta_material=None,
        field_width=None,
        field_zmin=None,
        field_zmax=None,
        fdtd_zmin=None,
        symmetry=False,
        sub_index=None,
        sub_material=None,
    ):
        self.bg_index = bg_index
        self.sub_index = sub_index
        self.sub_material = sub_material

        self.pixel_size = pixel_size
        self.sub_depth = sub_depth
        self.focal_length = focal_length
        self.meta_height = meta_height

        self.meta_size = meta_size
        self.meta_pitch = meta_pitch
        self.field_width = field_width
        self.field_zmin = field_zmin
        self.field_zmax = field_zmax
        self.meta_index = meta_index
        self.meta_material = meta_material

        self.red_wavelength = red_wavelength
        self.blue_wavelength = blue_wavelength
        self.green1_wavelength = green1_wavelength
        self.green2_wavelength = green2_wavelength
        self.mesh_dx = mesh_dx
        self.mesh_dy = mesh_dy
        self.mesh_dz = mesh_dz
        self.pva_level = pva_level
        self.fdtd_zmin = fdtd_zmin

        self.symmetry = symmetry

    def generate_base_sim(self, fdtd):
        """Build the base FDTD simulation.

        Adds the FDTD solver region, backward Gaussian source, field regions
        for each color channel and the normalization area, DFT monitors,
        and the pillar cylinder array. The source wavelength is
        set to ``red_wavelength`` by default; use the ``*_configurator``
        methods to switch wavelengths for each simulation config.

        Parameters
        ----------
        fdtd : lumapi.FDTD
            Open FDTD session to populate.

        Returns
        -------
        tuple[int, int]
            ``(num_cyl_x, num_cyl_y)`` - number of cylinders along each axis.
        """
        fdtd.redrawoff()

        fdtd.setglobalsource("center wavelength", self.red_wavelength)
        fdtd.setglobalsource("wavelength span", 0)
        fdtd.setglobalsource("optimize for short pulse", False)

        fdtd.setglobalmonitor("sample spacing", "uniform")  # Necessary?
        fdtd.setglobalmonitor("use wavelength spacing", True)
        fdtd.setglobalmonitor("use source limits", True)
        fdtd.setglobalmonitor("frequency points", 1)

        ## SETUP FDTD
        fdtd_xspan = self.pixel_size * 1.25
        fdtd_yspan = self.pixel_size * 1.25
        fdtd_zmax = self.focal_length + self.meta_height + 1.0e-6
        if self.fdtd_zmin is None:
            fdtd_zmin = -self.sub_depth - 0.5e-6
        else:
            fdtd_zmin = self.fdtd_zmin
        if self.symmetry:
            xmin_bc = "Anti-Symmetric"
            ymin_bc = "Symmetric"
        else:
            xmin_bc = "PML"
            ymin_bc = "PML"

        fdtd.addfdtd(
            {
                "dimension": "3D",
                "index": self.bg_index,
                "x": 0,
                "x span": fdtd_xspan,
                "y": 0,
                "y span": fdtd_yspan,
                "z min": fdtd_zmin,
                "z max": fdtd_zmax,
                "mesh type": "uniform",
                "dx": self.mesh_dx,
                "dy": self.mesh_dy,
                "dz": self.mesh_dz,
                "x min bc": xmin_bc,
                "x max bc": "PML",
                "y min bc": ymin_bc,
                "y max bc": "PML",
                "z min bc": "PML",
                "z max bc": "PML",
                "mesh refinement": "precise volume average",
                "meshing refinement": self.pva_level,
                "simulation time": 4e-12,
            }
        )

        ## SETUP SOURCE (Gaussian source)
        fdtd.addgaussian(
            {
                "injection axis": "z-axis",
                "direction": "Backward",
                "polarization angle": 0,
                "x": 0,
                "x span": fdtd_xspan,
                "y": 0,
                "y span": fdtd_yspan,
                "z": self.focal_length + self.meta_height + 0.5e-6,
                "waist radius w0": self.pixel_size / 2,
                "distance from waist": 0.0e-6,
                "override global source settings": False,
            }
        )

        ## SETUP FIELD REGIONS
        if self.field_width is None:
            field_width = self.pixel_size
        else:
            field_width = self.field_width
        if self.field_zmin is None:
            field_zmin = -self.sub_depth
        else:
            field_zmin = self.field_zmin
        if self.field_zmax is None:
            field_zmax = 0.0e-6
        else:
            field_zmax = self.field_zmax
        if math.isclose(field_zmin, field_zmax, rel_tol=1e-9, abs_tol=1e-10):
            field_type = "2D Z-normal"
        else:
            field_type = "3D"

        fdtd.addfieldregion(
            {
                "name": "fom_red",
                "monitor type": field_type,
                "x": -self.pixel_size / 4,
                "x span": field_width,
                "y": -self.pixel_size / 4,
                "y span": field_width,
                "z min": field_zmin,
                "z max": field_zmax,
                "nuttall window pulse": False,
                "override global monitor settings": False,  # important!
            }
        )
        fdtd.addfieldregion(
            {
                "name": "fom_blue",
                "monitor type": field_type,
                "x": self.pixel_size / 4,
                "x span": field_width,
                "y": self.pixel_size / 4,
                "y span": field_width,
                "z min": field_zmin,
                "z max": field_zmax,
                "nuttall window pulse": False,
                "override global monitor settings": False,  # important!
            }
        )
        fdtd.addfieldregion(
            {
                "name": "fom_green1",
                "monitor type": field_type,
                "x": -self.pixel_size / 4,
                "x span": field_width,
                "y": self.pixel_size / 4,
                "y span": field_width,
                "z min": field_zmin,
                "z max": field_zmax,
                "nuttall window pulse": False,
                "override global monitor settings": False,  # important!
            }
        )
        fdtd.addfieldregion(
            {
                "name": "fom_green2",
                "monitor type": field_type,
                "x": self.pixel_size / 4,
                "x span": field_width,
                "y": -self.pixel_size / 4,
                "y span": field_width,
                "z min": field_zmin,
                "z max": field_zmax,
                "nuttall window pulse": False,
                "override global monitor settings": False,  # important!
            }
        )
        fdtd.addfieldregion(
            {
                "name": "fom_norm",
                "monitor type": field_type,
                "x": 0.0,
                "x span": self.pixel_size,
                "y": 0.0,
                "y span": self.pixel_size,
                "z min": field_zmin,
                "z max": field_zmax,
                "nuttall window pulse": False,
                "override global monitor settings": False,  # important!
            }
        )

        ## SETUP Monitors for power density at the bottom of the pixel

        fdtd.adddftmonitor(
            {"name": "P_norm", "monitor type": "2D Z-normal", "x": 0, "x span": self.pixel_size, "y": 0, "y span": self.pixel_size, "z": field_zmin}
        )

        fdtd.adddftmonitor(
            {
                "name": "P_Q1",
                "monitor type": "2D Z-normal",
                "x": self.pixel_size / 4,
                "x span": self.pixel_size / 2,
                "y": self.pixel_size / 4,
                "y span": self.pixel_size / 2,
                "z": field_zmin,
            }
        )

        fdtd.adddftmonitor(
            {
                "name": "P_Q2",
                "monitor type": "2D Z-normal",
                "x": -self.pixel_size / 4,
                "x span": self.pixel_size / 2,
                "y": self.pixel_size / 4,
                "y span": self.pixel_size / 2,
                "z": field_zmin,
            }
        )

        fdtd.adddftmonitor(
            {
                "name": "P_Q3",
                "monitor type": "2D Z-normal",
                "x": -self.pixel_size / 4,
                "x span": self.pixel_size / 2,
                "y": -self.pixel_size / 4,
                "y span": self.pixel_size / 2,
                "z": field_zmin,
            }
        )

        fdtd.adddftmonitor(
            {
                "name": "P_Q4",
                "monitor type": "2D Z-normal",
                "x": self.pixel_size / 4,
                "x span": self.pixel_size / 2,
                "y": -self.pixel_size / 4,
                "y span": self.pixel_size / 2,
                "z": field_zmin,
            }
        )

        ## SETUP XZ FIELD MONITOR
        fdtd.adddftmonitor(
            {
                "name": "XZ_field",
                "enabled": False,
                "monitor type": "2D Y-normal",
                "x": 0,
                "x span": fdtd_xspan,
                "y": self.pixel_size / 4,
                "z min": fdtd_zmin,
                "z max": fdtd_zmax,
                "output power": False,
            }
        )

        ## SETUP XZ FIELD MONITOR
        fdtd.adddftmonitor(
            {
                "name": "XY_field",
                "enabled": False,
                "monitor type": "2D Z-normal",
                "x": 0,
                "x span": fdtd_xspan,
                "y": 0,
                "y span": fdtd_yspan,
                "z": field_zmax,
                "output power": False,
            }
        )

        ## SETUP SUBSTRATE
        if self.sub_index is None:  # Material name must have been provided
            if self.sub_material is None:
                raise ValueError("sub_material and sub_index were not provided")
            else:
                sub_material = self.sub_material
        else:  # Material index must have been provided
            if self.sub_material is None:
                sub_material = "<Object defined dielectric>"
            else:
                raise ValueError("sub_material and sub_index were not provided")

        fdtd.addrect(
            {
                "name": "substrate",
                "material": sub_material,
                "x": 0,
                "x span": self.pixel_size * 3,
                "y": 0,
                "y span": self.pixel_size * 3,
                "z min": -self.sub_depth - 1.0e-6,
                "z max": 0.0e-6,
            }
        )
        if sub_material == "<Object defined dielectric>":
            fdtd.set("index", self.sub_index)

        ## SETUP PILLARS
        if self.meta_index is None:  # Material name must have been provided
            if self.meta_material is None:
                raise ValueError("meta_material and meta_index were not provided")
            else:
                meta_material = self.meta_material
        else:  # Material index must have been provided
            if self.meta_material is None:
                meta_material = "<Object defined dielectric>"
            else:
                raise ValueError("meta_material and meta_index were not provided")

        # group_name = 'metasurface'
        # fdtd.addgroup({'name': group_name})

        if self.symmetry:
            num_cyl_x = math.floor((self.meta_size / 2 - self.meta_pitch / 2) / self.meta_pitch) + 1
            num_cyl_y = math.floor((self.meta_size / 2 - self.meta_pitch / 2) / self.meta_pitch) + 1
            ix_origin = 0
            iy_origin = 0
        else:
            num_cyl_x_pos = math.floor((self.meta_size / 2 - self.meta_pitch / 2) / self.meta_pitch)
            num_cyl_y_pos = math.floor((self.meta_size / 2 - self.meta_pitch / 2) / self.meta_pitch)
            num_cyl_x = 2 * num_cyl_x_pos + 1
            num_cyl_y = 2 * num_cyl_y_pos + 1
            ix_origin = -num_cyl_x_pos
            iy_origin = -num_cyl_y_pos

        for iy in range(num_cyl_y):
            for ix in range(num_cyl_x):
                idx = iy * num_cyl_x + ix
                fdtd.addcircle(
                    {
                        "name": f"cyl{idx}",
                        "material": meta_material,
                        "x": (ix + ix_origin) * self.meta_pitch,
                        "y": (iy + iy_origin) * self.meta_pitch,
                        "z min": self.focal_length,
                        "z max": self.focal_length + self.meta_height,
                        "radius": self.meta_pitch / 4,
                    }
                )
                if meta_material == "<Object defined dielectric>":
                    fdtd.set("index", self.meta_index)
                # fdtd.addtogroup(group_name)

        fdtd.redrawon()

        return num_cyl_x, num_cyl_y

    def red_configurator(self, fdtd):
        """Set the global source to the red wavelength."""
        fdtd.setglobalsource("center wavelength", self.red_wavelength)

    def blue_configurator(self, fdtd):
        """Set the global source to the blue wavelength."""
        fdtd.setglobalsource("center wavelength", self.blue_wavelength)

    def green1_configurator(self, fdtd):
        """Set the global source to the green1 wavelength."""
        fdtd.setglobalsource("center wavelength", self.green1_wavelength)

    def green2_configurator(self, fdtd):
        """Set the global source to the green2 wavelength."""
        fdtd.setglobalsource("center wavelength", self.green2_wavelength)


# ### Visualization utility classes
# These classes help to define the custom visualizer during optimization.


# +
@dataclass
class ConfigMonitorPanel(MonitorPanel):
    """MonitorPanel that loads a specific ProjectConfig before rendering.

    Loads config_key's forward simulation, renders, then restores the
    previous session loaded-state so subsequent panels are unaffected.
    """

    config_key: Any = None

    # Suppress the visualizer's blanket load_forward_results() call so it
    # doesn't overwrite the session state before each panel's update() runs.
    requires_forward_results: ClassVar[bool] = False

    def update(self, ax, fig, project, state: PanelState) -> None:
        """Load config_key's forward results, render, then restore session state.

        Overrides MonitorPanel.update to load the forward results for
        self.config_key before rendering, then restores the FDTD session's
        _loaded_state so subsequent panels are unaffected.
        """
        fdtd_session = getattr(project, "fdtd_session", None)
        if fdtd_session is None:
            self._render_error(ax, "No FDTD session attached.")
            return

        # Save the session's loaded-file pointer before touching it so that
        # any subsequent panels see the same cached state as if this panel
        # never ran.
        saved_loaded_state = fdtd_session._loaded_state
        try:
            project.load_forward_results(config_key=self.config_key)
            self._render(ax, fig, fdtd_session)
        except Exception as exc:
            self._render_error(ax, str(exc))
        finally:
            fdtd_session._loaded_state = saved_loaded_state


# -

# ### Utility functions
# These utility functions help with FoM definition.
# Here the FoM uses a soft minimum and soft maximum to define a optimization
# landscape that is differentiable and smooth to traverse for the minimizer.


def softmin(x, beta=10.0, axis=-1):
    """Differentiable soft minimum via log-sum-exp.

    Parameters
    ----------
    x : array-like
        Input array.
    beta : float, optional
        Sharpness; larger values produce a tighter approximation of ``min``.
    axis : int, optional
        Axis along which to reduce.

    Returns
    -------
    array-like
        Soft minimum of *x* along *axis*.
    """
    # stable log-sum-exp along 'axis'
    m = anp.max(-beta * x, axis=axis, keepdims=True)
    lse = m + anp.log(anp.sum(anp.exp(-beta * x - m), axis=axis, keepdims=True))
    out = -(1.0 / beta) * anp.squeeze(lse, axis=axis)
    return out


def softmax(x, beta=10.0, axis=-1):
    """Differentiable soft maximum via log-sum-exp.

    Parameters
    ----------
    x : array-like
        Input array.
    beta : float, optional
        Sharpness; larger values produce a tighter approximation of ``max``.
    axis : int, optional
        Axis along which to reduce.

    Returns
    -------
    array-like
        Soft maximum of *x* along *axis*.
    """
    # stable log-sum-exp along 'axis'
    m = anp.max(beta * x, axis=axis, keepdims=True)
    lse = m + anp.log(anp.sum(anp.exp(beta * x - m), axis=axis, keepdims=True))
    out = (1.0 / beta) * anp.squeeze(lse, axis=axis)
    return out


# ## Initialize simulation
# Define parameters and initialize the simulation

# +
# Create geometry
red_wavelength = 650e-9
green_wavelength = 520e-9
blue_wavelength = 450e-9

bg_index = 1.0  # Background material: air
sub_index = 1.0  # No substrate
pixel_size = 3.2e-6 + 3.2e-6 / 8
sub_depth = 4e-6
focal_length = 1.5e-6
meta_height = 1e-6
meta_size = 3.2e-6 + 2 * 3.2e-6 / 8
meta_pitch = 3.2e-6 / 8
meta_index = 2.4
field_width = pixel_size / 2.0 - 0.3e-6  # field_width = pixel_size/2. - 0.050e-6 #field_width = 1.2e-6
field_zmin = 0
field_zmax = 0
fdtd_zmin = -0.25e-6
mesh_dx = 0.025e-6
mesh_dy = 0.025e-6
mesh_dz = 0.025e-6
pva_level = 8
min_r = 0.05e-6  # in m
max_r = meta_pitch / 2 - min_r  # in m
# -

# + [markdown]
# Optimization region
# -

# +
optimization_region = lmpt.Box(
    x_span=meta_size, y_span=meta_size, z_min=focal_length, z_max=focal_length + meta_height, dx=mesh_dx, dy=mesh_dy, dz=mesh_dz
)
# -
# + [markdown]
# Setup the simulation using the class above.
# -
# +
meta_sim = MetalensCis(
    bg_index=bg_index,
    sub_index=sub_index,
    red_wavelength=red_wavelength,
    green1_wavelength=green_wavelength,
    green2_wavelength=green_wavelength,
    blue_wavelength=blue_wavelength,
    mesh_dx=mesh_dx,
    mesh_dy=mesh_dy,
    mesh_dz=mesh_dz,
    pva_level=pva_level,
    pixel_size=pixel_size,
    sub_depth=sub_depth,
    focal_length=focal_length,
    meta_height=meta_height,
    meta_size=meta_size,
    meta_pitch=meta_pitch,
    meta_index=meta_index,
    field_width=field_width,
    field_zmin=field_zmin,
    field_zmax=field_zmax,
    fdtd_zmin=fdtd_zmin,
    symmetry=False,
)
num_cyl_x, num_cyl_y = meta_sim.generate_base_sim(lumapi.FDTD(hide=True))
print(f"Number of cylinders: {num_cyl_x} x {num_cyl_y}")
# -
# + [markdown]
# Define the bounds array
# -
num_cyl = num_cyl_x * num_cyl_y
bounds = [(min_r, max_r)] * num_cyl

# ## Parametrization
# Define the parametrization such that the radius of each pillar is free parameter.


def param_func(params):
    """Map a flat parameter array to an ordered dict of cylinder radii.

    Parameters
    ----------
    params : array-like
        Sequence of radius values, one per cylinder.

    Returns
    -------
    OrderedDict
        Mapping of ``'cyl{idx}::radius'`` keys to the corresponding values
        in *params*.
    """
    return OrderedDict({f"cyl{idx}::radius": value for idx, value in enumerate(params)})


parametrization = lmpt.Parametrization(func=param_func, bounds=bounds, optimization_region=optimization_region, dp=5e-10)

# ## Figure of merit
# First, define project configurations, since each field region is single wavelength

# +
config_red = lmpt.ProjectConfig(configurator=meta_sim.red_configurator, filename_suffix="red")
config_green = lmpt.ProjectConfig(configurator=meta_sim.green1_configurator, filename_suffix="green1")
config_blue = lmpt.ProjectConfig(configurator=meta_sim.blue_configurator, filename_suffix="blue")
# -
# + [markdown]
# Then, define the field results for each wavelength. Normalize the intensity of each region by the total intensity falling on the entire area.
# Also define the cross-talk terms to help set up the FoM such that cross talk is minimized.
# -

# +
intensity_red = lmpt.FieldResults(monitor_name="fom_red", metric="intensity", wavelengths=red_wavelength, config=config_red)
intensity_red_cross_green1 = lmpt.FieldResults(monitor_name="fom_green1", metric="intensity", wavelengths=red_wavelength, config=config_red)
intensity_red_cross_green2 = lmpt.FieldResults(monitor_name="fom_green2", metric="intensity", wavelengths=red_wavelength, config=config_red)
intensity_red_cross_blue = lmpt.FieldResults(monitor_name="fom_blue", metric="intensity", wavelengths=red_wavelength, config=config_red)
red_norm = lmpt.FieldResults(monitor_name="fom_norm", metric="intensity", wavelengths=red_wavelength, config=config_red)

intensity_green1 = lmpt.FieldResults(monitor_name="fom_green1", metric="intensity", wavelengths=green_wavelength, config=config_green)
intensity_green2 = lmpt.FieldResults(monitor_name="fom_green2", metric="intensity", wavelengths=green_wavelength, config=config_green)
intensity_green_cross_red = lmpt.FieldResults(monitor_name="fom_red", metric="intensity", wavelengths=green_wavelength, config=config_green)
intensity_green_cross_blue = lmpt.FieldResults(monitor_name="fom_blue", metric="intensity", wavelengths=green_wavelength, config=config_green)
green_norm = lmpt.FieldResults(monitor_name="fom_norm", metric="intensity", wavelengths=green_wavelength, config=config_green)

intensity_blue = lmpt.FieldResults(monitor_name="fom_blue", metric="intensity", wavelengths=blue_wavelength, config=config_blue)
intensity_blue_cross_red = lmpt.FieldResults(monitor_name="fom_red", metric="intensity", wavelengths=blue_wavelength, config=config_blue)
intensity_blue_cross_green1 = lmpt.FieldResults(monitor_name="fom_green1", metric="intensity", wavelengths=blue_wavelength, config=config_blue)
intensity_blue_cross_green2 = lmpt.FieldResults(monitor_name="fom_green2", metric="intensity", wavelengths=blue_wavelength, config=config_blue)
blue_norm = lmpt.FieldResults(monitor_name="fom_norm", metric="intensity", wavelengths=blue_wavelength, config=config_blue)
# -

# + [markdown]
# Define the figure of merit custom function next.
# Each of the area is represented by
# $\frac{I}{1 + \text{softmax}\!\left(\sum_j I_{\text{crosstalk},j}\right)}$,
# where $I$ is the normalized intensity and the sum runs over all crosstalk channels.
# -


# +
def fom_softmin_ratios(x):
    """Compute the FoM as the soft minimum of cross-talk-penalized intensity ratios.

    Each color channel's contribution is the channel intensity normalized by
    the total pixel power, divided by one plus the soft maximum of all
    cross-talk intensities (also normalized). The overall FoM is the soft
    minimum of these four per-channel values (red, green1, green2, blue).

    Parameters
    ----------
    x : tuple
        Fifteen scalar intensity values in the order expected by :data:`fom`.

    Returns
    -------
    float
        Scalar figure of merit.
    """
    (
        intensity_red,
        intensity_green1,
        intensity_green2,
        intensity_blue,
        intensity_red_cross_green1,
        intensity_red_cross_green2,
        intensity_red_cross_blue,
        intensity_green_cross_red,
        intensity_green_cross_blue,
        intensity_blue_cross_red,
        intensity_blue_cross_green1,
        intensity_blue_cross_green2,
        red_norm,
        green_norm,
        blue_norm,
    ) = x

    red_fom = (intensity_red / red_norm) / (
        1.0 + softmax(anp.array([intensity_red_cross_green1, intensity_red_cross_green2, intensity_red_cross_blue]), beta=10.0, axis=0) / red_norm
    )
    green1_fom = (2.0 * intensity_green1 / green_norm) / (
        1.0 + softmax(anp.array([intensity_green_cross_red, intensity_green2, intensity_green_cross_blue]), beta=10.0, axis=0) / green_norm
    )
    green2_fom = (2.0 * intensity_green2 / green_norm) / (
        1.0 + softmax(anp.array([intensity_green_cross_red, intensity_green1, intensity_green_cross_blue]), beta=10.0, axis=0) / green_norm
    )
    blue_fom = (intensity_blue / blue_norm) / (
        1.0 + softmax(anp.array([intensity_blue_cross_green1, intensity_blue_cross_green2, intensity_blue_cross_red]), beta=10.0, axis=0) / blue_norm
    )

    return softmin(anp.array([red_fom, green1_fom, green2_fom, blue_fom]), beta=10.0, axis=0)


# -

# + [markdown]
# Finally, call the fom function to create the fom
# -
# +
fom = lmpt.Fom(
    [
        intensity_red,
        intensity_green1,
        intensity_green2,
        intensity_blue,
        intensity_red_cross_green1,
        intensity_red_cross_green2,
        intensity_red_cross_blue,
        intensity_green_cross_red,
        intensity_green_cross_blue,
        intensity_blue_cross_red,
        intensity_blue_cross_green1,
        intensity_blue_cross_green2,
        red_norm,
        green_norm,
        blue_norm,
    ],
    fct=fom_softmin_ratios,
)
# -

# ## Project
# Define the runner and set up project object.

# +
runner = lmpt.LocalRunner(resource="GPU")
fdtd_session = lmpt.FdtdSession(show_fdtd_cad=False)

project = lmpt.Project(setup=meta_sim.generate_base_sim, fdtd_session=fdtd_session, parametrization=parametrization, runner=runner, fom=fom)
# -
# + [markdown]
# Define a set of random initial parameters
# -
# +
np.random.seed(17)
params = np.random.rand(num_cyl) * (max_r - min_r) + min_r
# -

# ### Project validation
# You can use the commands below to validate the project setup and gradient computation before running.
# Only one of the command is enabled, but you can uncomment the others to test them as needed.

# +
project.visualize_geometry(params=params)  # Visualize the setup
# project.visualize_fom(params=params)  # Test figure of merit computation
# lmpt.validate_gradient(project=project, params=params, perturbation = 5e-10, indices=[1, 37, 80])  # Validate the gradient with finite differences
# Convergence test for finite difference gradient estimation
# lmpt.fd_sweep_perturbation(project=project, params=params, index=0, perturbation_values=np.logspace(-11, -8, 13))
# -

# ## Optimizer
# Set up the optimizer with L-BFGS-B method.

optimizer = lmpt.ScipyOptimizer(method="L-BFGS-B", bounds=bounds, gtol=1e-20)

# ## Callbacks
# We set up two visualizers to monitor the optimization progress.
# The first visualizer contains FoM and gradient information, with the second one showing the field intensity distribution for each wavelength.

# +
fom_and_gradient_visualizer = lmpt.GraphicalVisualizer()
field_visualizer = lmpt.GraphicalVisualizer(
    panels=[
        ConfigMonitorPanel(
            config_key=config_red,
            monitor_name="P_norm",
            result_name="E",
            operation="abs^2",
            title="Red (650 nm) - Intensity",
        ),
        ConfigMonitorPanel(
            config_key=config_green,
            monitor_name="P_norm",
            result_name="E",
            operation="abs^2",
            title="Green (520 nm) - Intensity",
        ),
        ConfigMonitorPanel(
            config_key=config_blue,
            monitor_name="P_norm",
            result_name="E",
            operation="abs^2",
            title="Blue (450 nm) - Intensity",
        ),
    ],
    figsize=(15, 5),
    layout=(1, 3),
    filename_prefix="field_configs",
)
callbacks = [fom_and_gradient_visualizer, field_visualizer]
# -

# + [markdown]
# The initial field visualizer is shown below. As seen from the figure, the initial random structure does not provide good
# routing for different colors, and most of the intensity is not in the intended area.
# <img src="images/initial_fields.png" width="80%">
# -

# ## Run optimization

# Define optimization session
optimization = lmpt.Optimization(project, optimizer, callbacks, store_all_simulations=False)
# Run the optimization
result = optimization.run(initial_params=params)

# ## Results
# Save the final results

# +
best_params, best_fom = result
project.save_project("color_router_final.fsp", params=best_params)
# -

# + [markdown]
# Result for the structure after 97 iterations is shown below, at which point the tolerance was reached.
# The final field distribution is also shown below. Compared to the initial results, each wavelength is more focused in their designated areas.
# <img src="images/final_plot.png" width="80%">
# <img src="images/final_fields.png" width="80%">
# -
