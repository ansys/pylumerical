import numpy as np
import ansys.lumerical.core.lumopt2 as lmpt
import math

# Parameters
n_wg      = math.sqrt(12.25)  # Silicon (waveguide) refractive index
n_bg      = math.sqrt(2.25)   # Silicon oxide background
wg_width  = 0.5e-6            # Waveguide width (500nm)
wg_height = 0.22e-6           # Waveguide height (220nm)

# Wavelength range for optimization (O-band telecom)
wavelengths = np.linspace(1200e-9, 1400e-9, 21)

# Design region parameters
bend_radius     = 1.0e-6
bend_start      = wg_width/2+bend_radius
dist_to_wall    = 0.4e-6                        # Distance from wall to start of the bend (lead waveguides)
fdtd_min_x      =-(bend_start + dist_to_wall)
fdtd_max_x      = 2*wg_width

fdtd_min_y      =-2*wg_width
fdtd_max_y      = bend_start + dist_to_wall

fdtd_span_z     = 1.6e-6

mode_width      = 4 * wg_width
mode_height     = fdtd_span_z

fdtd_buffer = 0.2e-6  # Extra buffer around optimization region for FDTD simulation

mesh_size = 25e-9  # FDTD mesh size for optimization region


# Create base simulation setup "conformal variant 0" or "precise volume average"}
def generate_base_sim(fdtd):
    fdtd.addfdtd({"x min":fdtd_min_x-fdtd_buffer, "x max":fdtd_max_x+fdtd_buffer, "y min":fdtd_min_y-fdtd_buffer,
                "y max":fdtd_max_y+fdtd_buffer, "z span":fdtd_span_z+2*fdtd_buffer, "index": n_bg,
                "mesh accuracy": 3, "mesh refinement": "precise volume average"})
    
    # Input waveguides (horizontal - extending beyond crossing region)
    fdtd.addrect({"name": "wg_in",  "index": n_wg, "x min": 2*fdtd_min_x, "x max":-bend_start, "y":0, "y span":wg_width, "z span": wg_height})
    fdtd.addrect({"name": "wg_out", "index": n_wg, "y min": bend_start, "y max": 2*fdtd_max_y, "x":0, "x span":wg_width, "z span": wg_height})

    # Ports
    fdtd.addport({"name": "port_in"})
    fdtd.set("injection axis","x")
    fdtd.set({"x":-bend_start-dist_to_wall/2., "y":0, "y span":mode_width, "z span":mode_height, "direction":"Forward", "frequency dependent profile":False})

    fdtd.addport({"name": "port_out"})
    fdtd.set("injection axis","y")
    fdtd.set({"y": bend_start+dist_to_wall/2., "x":0, "x span":mode_width, "z span":mode_height, "direction":"Backward", "frequency dependent profile":False})

    # Source and monitor properties
    fdtd.setglobalsource("wavelength start", wavelengths[0])
    fdtd.setglobalsource("wavelength stop", wavelengths[-1])
    fdtd.setglobalmonitor("frequency points", len(wavelengths))
    fdtd.setglobalmonitor("use wavelength spacing", True)
    fdtd.setnamed("FDTD::ports","override global monitor settings",False)

## OPTIMIZATION REGION ##

# Define the optimization region for the L-bend. Inside this region, the geometry can change during optimization. The FDTD simulation will be set up to cover this region with appropriate boundary conditions and ports.
optimization_region = lmpt.Box(x_min=fdtd_min_x, x_max=fdtd_max_x,
                               y_min=fdtd_min_y, y_max=fdtd_max_y,
                               z_min=-wg_height/2.0, z_max=wg_height/2.0,
                               mesh_size=mesh_size)

## CLOSED CURVE - BASE GEOMETRY ##

# L-bend curve definition
# The two cubic segments (2 and 6) form the two parametric sidewalls of the
# bend: segment 2 is the outer wall and segment 6 is the inner wall.  Both
# segments map to themselves under reflection across the y = -x diagonal, so
# the symmetric example can constrain control points on each segment to be
# mirror partners of each other.
path = [ (lmpt.Segment([ fdtd_min_x,              wg_width/2],             'linear')),  # Segment 1
         (lmpt.Segment([-wg_width/2-bend_radius,  wg_width/2],             'cubic')),   # Segment 2 (outer sidewall, parametric)
         (lmpt.Segment([-wg_width/2,              wg_width/2+bend_radius], 'linear')),  # Segment 3
         (lmpt.Segment([-wg_width/2,              fdtd_max_y],             'linear')),  # Segment 4
         (lmpt.Segment([ wg_width/2,              fdtd_max_y],             'linear')),  # Segment 5
         (lmpt.Segment([ wg_width/2,              wg_width/2+bend_radius], 'cubic')),   # Segment 6 (inner sidewall, parametric)
         (lmpt.Segment([-wg_width/2-bend_radius, -wg_width/2],             'linear')),  # Segment 7
         (lmpt.Segment([ fdtd_min_x,             -wg_width/2],             'linear')),  # Segment 8
       ]

# Create base geometry using ClosedCurve
closed_curve = lmpt.ClosedCurve(path, optimization_region=optimization_region, index=n_wg, z_min=-wg_height/2.0, z_max= wg_height/2.0)
closed_curve.plot() # Visualize the base geometry


## CLOSED CURVE - PARAMETRIZATION ##
num_pts_per_curve = 2                      # Number of control points to optimize for each of the two curved segments

# Each control point is allowed to slide along the local outward normal between
# bounds[0] and bounds[1].  The asymmetric range gives the optimizer more room
# to bow the silicon outward (positive direction) than to carve into it.
bounds = (-200e-9, 400e-9)
segments_to_parametrize = [lmpt.Parametrize(segment_index=2, num_added_vertices=num_pts_per_curve, bounds=bounds, movement='normal'),  # Outer sidewall
                           lmpt.Parametrize(segment_index=6, num_added_vertices=num_pts_per_curve, bounds=bounds, movement='normal')]  # Inner sidewall
closed_curve.make_segments_parametric(segments_to_parametrize)

closed_curve.plot() # Visualize the geometry with parametric segments and control points

## FIGURE OF MERIT ##

# Define a broadband figure of merit: maximize the average transmission across
# the full O-band sweep defined above.  Using all simulated wavelengths (rather
# than picking a single point) makes the optimization realistic and matches the
# multi-wavelength sweep already configured for the FDTD source/monitors.
port_out = lmpt.PortResults('port_out', metric='transmission', wavelengths=wavelengths)
l_bend_fom = lmpt.Fom(port_out, fct=lmpt.PNorm(p=2,target=1.0))

## PROJECT SETUP ##

# Create an FDTD session
fdtd_session = lmpt.FdtdSession(show_fdtd_cad=False)

# Create the project
project = lmpt.Project(setup=generate_base_sim, parametrization=closed_curve, fom=l_bend_fom, fdtd_session=fdtd_session)
project.visualize_fom()

# Use Nelder-Mead optimizer (gradient-free).  With only 4 parameters the
# simplex method converges quickly and avoids the cost of an adjoint sweep.
optimizer = lmpt.ScipyOptimizer(method='Nelder-Mead', max_iter=40)

# Create a graphical visualizer callback for real-time plotting
# Compose the figure from a FOM trace, the live geometry, and a transmission
# spectrum at the output port.
visualizer = lmpt.GraphicalVisualizer(
    figsize=(14, 6),
    layout=(1, 3),
    panels=[ lmpt.FomPanel(),
             lmpt.GeometryPanel(),
             lmpt.MonitorPanel( monitor_name='FDTD::ports::port_out',
                                result_name='T',
                                operation='abs',
                           title='Output transmission',
        ),
    ],
)

# Create optimization object, add in visualizer and a file logger from before
optimization = lmpt.Optimization(
    project=project,
    optimizer=optimizer,
    callbacks=[visualizer, lmpt.FileLogger()],
)

# RUN #
result = optimization.run()

# Save final design for further processing
best_params, best_fom = result
project.save_project("L_bend_optimization_final.fsp",params=best_params)
