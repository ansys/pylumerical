# %% [markdown]
# ### Edge Coupler
# 
# This example demonstrates how to use EME and run propogation length sweep

# %%
import ansys.lumerical.core as lumapi
import matplotlib.pyplot as plt
import os

fname = os.path.join(os.path.realpath(os.path.dirname(__file__)),'assets/spot_size_converter.lms')
print(fname)
##Open the session without GUI
with lumapi.MODE(filename=fname,hide=False) as mode:
    ## Switch to layour before updating EME properties    
    mode.switchtolayout()
    
    #######################################
    ## Query geometry and can update
    mode.select("taper")
    taper_prop = mode.queryuserprop("taper")
    print(taper_prop['name'])
    
    ## This shows how to update the values
    mode.setnamed("taper","index",1.5)
    
    ######################################
    ## Update EME solver parameters    
    sc = mode.getnamed("EME","subcell method");
    
    print(sc)
    ## sub_cell is an array the length of the group span with 0 = none, and 1 = CVCS
    sc[1] = 1 #Ensure you have CVCS enabled in cell group 2
    mode.setnamed("EME","subcell method",sc); #update EME solver
    
    ######################################
    ##Run EME solver
    mode.run()

    ######################################
    ## Set propagation sweep settings
    mode.setemeanalysis("propagation sweep",1)
    mode.setemeanalysis("parameter","group span 2")
    mode.setemeanalysis("start",20e-6)
    mode.setemeanalysis("stop",200e-6)
    mode.setemeanalysis("number of points",201)
    
    # run propagation sweep tool
    mode.emesweep()
    
    # get propagation sweep result
    S = mode.getemesweep('S')
    
    plt.plot(S['group_span_2']*1e6,abs(S['s21'])**2)
    plt.title("Output Power")
    plt.xlabel("Length [um]")
    plt.ylabel("|S_21|^2")
    plt.show()
    input("Enter")


