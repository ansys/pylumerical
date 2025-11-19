# %% [markdown]
# ### FDTD Nanowire Example
# 
# This example demonstrates how to define an FDTD workflow as a python function. It will then load theory data from a csv file and it will then plot the results using matplot.
# [Nanowire Example](https://optics.ansys.com/hc/en-us/articles/360034416574-Using-the-Python-API-in-the-nanowire-application-example)

# %%
#Import the required modules
import ansys.lumerical.core as lumapi
import numpy as np
import matplotlib.pyplot as plt

#Define an FDTD function
def runNanowireSimulation(profile_monitor_wavelength=1e-6):
    """ This function makes is convenient to reconstruct the simulation,
        while changing a few key properties, a brand new FDTD will start
        and close within this function
    """
    fdtd = lumapi.FDTD()
    fdtd.addcircle()
    fdtd.addfdtd()
    fdtd.addmesh()
    fdtd.addtfsf()

    fdtd.addobject("cross_section")
    fdtd.set("name", "scat")
    fdtd.addobject("cross_section")
    fdtd.set("name", "total")

    fdtd.addtime()
    fdtd.set("name", "time")

    fdtd.adddftmonitor()
    fdtd.set("name", "profile")

    configuration = (
        ("source", (("polarization angle", 0.),
                    ("injection axis", "y"),
                    ("x", 0.),
                    ("y", 0.),
                    ("x span", 100.0e-9),
                    ("y span", 100.0e-9),
                    ("wavelength start", 300.0e-9),
                    ("wavelength stop", 400.0e-9))),

        ("mesh", (("dx", 0.5e-9),
                  ("dy", 0.5e-9),
                  ("x", 0.),
                  ("y", 0.),
                  ("x span", 110.0e-9),
                  ("y span", 110.0e-9))),

        ("FDTD", (("simulation time", 200e-15), # in seconds
                  ("dimension", "2D"),
                  ("x",0.0e-9),
                  ("y",0.),
                  ("z",0.),
                  ("x span", 800.0e-9),
                  ("y span", 800.0e-9),
                  ("mesh refinement", "conformal variant 1"))),

        ("circle", (("x", 0.0e-9),
                    ("y", 0.0e-9),
                    ("z", 0.0e-9),
                    ("radius", 25.0e-9), # in meters
                    ("material", "Ag (Silver) - Palik (0-2um)"))),

        ("scat", (("x", 0.),
                  ("y", 0.),
                  ("z", 0.),
                  ("x span", 110.0e-9),
                  ("y span", 110.0e-9))),

        ("total", (("x", 0.),
                   ("y", 0.),
                   ("z", 0.),
                   ("x span", 90.0e-9),
                   ("y span", 90.0e-9))),

        ("time", (("x", 28.0e-9),
                  ("y", 26.0e-9))),

        ("profile", (("x", 0.),
                     ("y", 0.),
                     ("x span", 90e-9),
                     ("y span", 90e-9),
                     ("override global monitor settings", True),
                     ("use source limits", False),
                     ("frequency points", 1),
                     ("wavelength center", float(profile_monitor_wavelength)),
                     ("wavelength span", 0.))),
    )

    for obj, parameters in configuration:
       for k, v in parameters:
           fdtd.setnamed(obj, k, v)

    fdtd.setnamed("profile", "wavelength center", float(profile_monitor_wavelength))

    fdtd.setglobalmonitor("frequency points", 100) # setting the global frequency resolution

    fdtd.save("nanowire_test")
    fdtd.run("FDTD","CPU")

    return fdtd.getresult("scat", "sigma"), fdtd.getresult("total", "sigma"), fdtd.getresult("profile", "E")



# %% [markdown]
# ## Plot results

# %%
import os

# run the simulation once, to determine resonance wavelength
## and get cross-sections from analysis objects
sigmascat, sigmaabs, _ = runNanowireSimulation()

lam_sim = sigmascat['lambda'][:,0]
f_sim = sigmascat['f'][:,0]
sigmascat = sigmascat['sigma']
sigmaabs  = sigmaabs['sigma']
sigmaext = -sigmaabs + sigmascat

#load cross section theory from text file
nw_theory = np.genfromtxt(os.path.join(os.path.realpath(os.path.dirname(__file__)),"assets/nanowire_theory.csv"), delimiter=",")
nw_theory.shape

lam_theory = nw_theory[:,0]*1.e-9

r23 = nw_theory[:,1:4]*2*23*1e-9  #flipping data
r24 = nw_theory[:,4:7]*2*24*1e-9
r25 = nw_theory[:,7:10]*2*25*1e-9
r26 = nw_theory[:,10:13]*2*26*1e-9
r27 = nw_theory[:,13:16]*2*27*1e-9

for i in range(0, 3):
    r23[:,i] = np.interp(lam_sim, lam_theory, r23[:,i])
    r24[:,i] = np.interp(lam_sim, lam_theory, r24[:,i])
    r25[:,i] = np.interp(lam_sim, lam_theory, r25[:,i])
    r26[:,i] = np.interp(lam_sim, lam_theory, r26[:,i])
    r27[:,i] = np.interp(lam_sim, lam_theory, r27[:,i])

# compare FDTD to theory
plt.plot(lam_sim, sigmaext*1e9, label='sigmaext')
plt.plot(lam_sim, -sigmaabs*1e9)
plt.plot(lam_sim, sigmascat*1e9)
plt.plot(lam_sim, r25*1e9)
plt.xlabel('wavelength (nm)')
plt.ylabel('cross section (nm)')

plt.show()

plt.plot(lam_sim, sigmaext*1e9, label='sigmaext')
plt.plot(lam_sim, -sigmaabs*1e9)
plt.plot(lam_sim, sigmascat*1e9)
plt.plot(lam_sim, r24*1e9)
plt.plot(lam_sim, r26*1e9)
plt.xlabel('wavelength (nm)')
plt.ylabel('cross section (nm)')

plt.show()

## run the simulation again using the resonance wavelength
_, _, E = runNanowireSimulation(profile_monitor_wavelength=lam_sim[np.argmax(sigmascat)])

## show the field intensity profile
Ey = E["E"][:,:,0,0,1]
plt.pcolor(np.transpose(abs(Ey)**2), vmax=5, vmin=0)
plt.xlabel("x (nm)")
plt.ylabel("y (nm)")
plt.xticks(range(Ey.shape[0])[::25], [int(v) for v in E["x"][:,0][::25]*1e9])
plt.yticks(range(Ey.shape[1])[::25], [int(v) for v in E["y"][:,0][::25]*1e9])
plt.colorbar()
plt.show()



