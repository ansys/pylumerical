.. _ref_script_commands_as_methods:

Script commands as methods
==========================

At the most basic level, the Lumerical Python API can be used to directly invoke Lumerical script commands and interact with the product as the Lumerical Scripting Language would.

This article will describe the basic use case for using scripting commands as methods, and common best practices.

Built-in scripting commands
----------------------------

Overview
^^^^^^^^^^

Almost all script commands in the Lumerical Scripting Language can be used as methods on your session object in Python. The lumapi methods and the Lumerical script commands share the same name and can be called directly on the session once it's been created.

For more information on the Lumerical Scripting Language, please see:

* `Lumerical Scripting Learning Track on Ansys Innovation Courses (AIC) <https://courses.ansys.com/index.php/courses/ansys-lumerical-scripting/>`__

* `Lumerical Scripting Language - Alphabetical list <https://optics.ansys.com/hc/en-us/articles/360034923553>`__

* `Lumerical Scripting Language - By category <https://optics.ansys.com/hc/en-us/articles/360037228834>`__

Two simple examples are show below. In the first example, the Lumerical commands `getfdtdindex <https://optics.ansys.com/hc/en-us/articles/360034409694-getfdtdindex-Script-command>`__ and `stackrt <https://optics.ansys.com/hc/en-us/articles/360034406254-stackrt-Script-command>`__ is used in conjunction with typical math and plotting libraries in Python to simulate and visualize the transmission of a gold thin film illuminated by a plane wave. 
In the second example, a simple simulation with a gaussian source and a frequency domain monitor is set up and executed.

**Example**

For more information on how to import lumapi for PyLumerical, see :doc:`Installation and getting started for PyLumerical <installation>`.

.. code-block:: python
    
    import lumapi #Ensure lumapi has already been added to path
    import numpy as np
    import matplotlib.pyplot as plt

    with lumapi.FDTD() as fdtd:
        lambda_range = np.linspace(300e-9, 1100e-9, 500)
        c=2.99792458e8
        f_range = c/lambda_range
        au_index = fdtd.getfdtdindex("Au (Gold) - CRC", f_range, np.min(f_range), np.max(f_range)) #Use the getfdtdindex command to obtain the correct complex index for gold
        

        stackRT_result = fdtd.stackrt(np.transpose(au_index), np.array([10e-9]), f_range) #Use the stackrt command to calculate the transmission and reflection
    #Visualize using matplotlib
    fig, ax = plt.subplots()
    ax.plot(lambda_range*1e9, stackRT_result["Ts"], label="Transmission")
    ax.set_xlabel("Wavelength [nm]")
    ax.set_ylabel("Transmission")
    ax.legend()
    plt.show()

**Example**

.. code-block:: python

    import os,sys
    import numpy as np
    sys.path.append("C:\\Program Files\\Lumerical\\v251\\api\\python\\") # locate lumapi files
    import lumapi
    import matplotlib.pyplot as plt


    with lumapi.FDTD() as fdtd: 
    
        # Set up simulation region
        fdtd.addfdtd()
        fdtd.set("x",0)
        fdtd.set("x span",8e-6)
        fdtd.set("y",0)
        fdtd.set("y span",8e-6)
        fdtd.set("z",0.25e-6)
        fdtd.set("z span",0.5e-6)
    
        # Set up source
        fdtd.addgaussian()
        fdtd.set("injection axis","z")
        fdtd.set("direction","forward")
        fdtd.set("x",0)
        fdtd.set("x span",16e-6)
        fdtd.set("y",0)
        fdtd.set("y span",16e-6)
        fdtd.set("z",0.2e-6)
        fdtd.set("use scalar approximation",1)
        fdtd.set("waist radius w0",2e-6)
        fdtd.set("distance from waist",0)
        fdtd.setglobalsource("wavelength start",1e-6)
        fdtd.setglobalsource("wavelength stop",1e-6)
    
        # Set up monitor
        fdtd.addpower()
        fdtd.set("monitor type","2D Z-normal")
        fdtd.set("x",0)
        fdtd.set("x span",16e-6)
        fdtd.set("y",0)
        fdtd.set("y span",16e-6)
        fdtd.set("z",0.3e-6)
    
        # Run simulation
        fdtd.save("fdtd_tutorial.fsp")
        fdtd.run()

Constructor script commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many Lumerical script commands are used to add simulation objects such simulation regions or geometric regions. These commands typically start with “add”, for example, `addrect <https://optics.ansys.com/hc/en-us/articles/360034404214-addrect-Script-command>`__ or `addfdtd <https://optics.ansys.com/hc/en-us/articles/360034924173-addfdtd-Script-command>`__.

In the Lumerical Python API, simulation objects can be created in many different ways. 
At a fundamental level, objects can be created and have their properties set like how it is done in a Lumerical script using `set <https://optics.ansys.com/hc/en-us/articles/360034928773-set-Script-command>`__ and `setnamed <https://optics.ansys.com/hc/en-us/articles/360034928793-setnamed-Script-command>`__.

In addition, the lumapi also supports assigning properties to object in a pythonic way, either by creating a dictionary and assigning it to the properties attribute during initialization or using keyword arguments directly. 
When constructing objects using these methods, some properties may need to be initialized in order or may overwrite other properties. Therefore, it is recommended to use an ordered dictionary to ensure that these properties are set as intended.

The examples below show various methods on object construction. 
For more information regarding adding and manipulating simulation objects, including best practices, see the article on :doc:`Working with simulation objects <working_with_simulation_objects>`. 
Property names where a space is present (e.g. “x span”) is replaced by an underscore when using keyword arguments (e.g. “x_span”).

**Example**

These examples create a 3D FDTD region centered at the origin and with a span of 1μm.

Firstly, using the Lumerical script commands:

.. code-block:: python

    fdtd = lumapi.FDTD()
    fdtd.addfdtd()
    fdtd.set("x",0)
    fdtd.set("y",0)
    fdtd.set("z",0)
    fdtd.set("x span",1e-6)
    fdtd.set("y span",1e-6)
    fdtd.set("z span",1e-6)

The following code creates the FDTD region uses an ordered dictionary to set its properties.

.. code-block:: python

    from collections import OrderedDict #Ensure OrderedDict is imported
    #import other modules

    fdtd = lumapi.FDTD() 
    props = OrderedDict([("x", 0),("y",0), ("z", 0), ("x span", 1e-6), ("y span", 1e-6), ("z span", 1e-6)])
    fdtd.addfdtd(properties = props) 

The following code creates the FDTD region using keyword arguments

.. code-block:: python

    fdtd = lumapi.FDTD()
    fdtd.addfdtd(x=0,y=0,z=0,x_span=1e-6, y_span=1e-6, z_span=1e-6) #Note that the property names where a space was present is replaced by an underscore

For more information regarding adding and manipulating simulation objects, including other ways to interact with these objects and best practices see the article on :doc:`Working with simulation objects <working_with_simulation_objects>`.

Importing custom script commands
---------------------------------

In addition to default script commands, you can also take advantage of the auto-syncing function feature in lumapi and import functions that are pre-defined in a Lumerical script file (.lsf file). 
To import these functions, you can either execute the scripts while constructing the session (using the :doc:`script keyword argument <../api/interface_class>`), or manually evaluating the file using the :py:meth:`ansys.lumerical.core.FDTD.eval` method.

.. note::
    The :py:meth:`ansys.lumerical.core.FDTD.eval` is common to all products, and is available as :py:meth:`ansys.lumerical.core.MODE.eval`, :py:meth:`ansys.lumerical.core.DEVICE.eval`, and :py:meth:`ansys.lumerical.core.INTERCONNECT.eval`.

**Example**

The following two .lsf files contains custom functions.

MyFunctions.lsf

.. code-block::

    function helloWorld(){
    return "helloworld";
    }

    function customAdd(a,b){
    return a+b;
    }

MyFunctions2.lsf

.. code-block::

    function customMultiply(a,b){
    return a*b;
    }

The following script imports functions from both custom script files upon session creation.

.. code-block:: python

    with lumapi.FDTD(script = ["MyFunctions.lsf", "MyFunctions2.lsf"]) as fdtd:
    #From MyFunctions.lsf
    print(fdtd.helloWorld())
    print(fdtd.customAdd(1,2))
    #From MyFunctions2.lsf
    print(fdtd.customMultiply(4,5))

Returns

..code-block::

    helloworld
    3.0
    20.0

Non-Constructor Script Commands
---------------------------------

Script commands that do not create simulation objects where input arguments are required can only be used with positional arguments and is not compatible with keyword arguments.

For example the following code will result in an error, even though the `set <https://optics.ansys.com/hc/en-us/articles/360034928773-set-Script-command>`__ script command takes property and value as input arguments.

**Example**

.. code-block:: python

    fdtd.addfdtd()
    fdtd.set(property = "x span", value = 1e-6)

    #Results in an error

The correct usage would be the following.

.. code-block:: python

    fdtd.addfdtd()
    fdtd.set("x span", 1e-6)

This applies also to methods defined in other scripting files that are loaded by first evaluating the script file.

**Example**

A Lumerical script file named MyConstructor.lsf contains the following function definition.

.. code-block::

    function constructFDTDandRect(x_input,y_input,z_input){
    #This function creates an FDTD and a rectangle region with center coordinates at x, y, and z
    addfdtd;
    set("x",x_input);
    set("y",y_input);
    set("z",z_input);
    
    addrect;
    set("x",x_input);
    set("y",y_input);
    set("z",z_input);
    }

The following Python driver script causes an error, even though the function defined in the script file have arguments named x_input, y_input, and z_input.

.. code-block:: python

    fdtd = lumapi.FDTD()
    custom_code = open("MyConstructor.lsf", "r").read()#This assumes the current working directory has a file named “MyConstructor.lsf”. Use os.chdir to change the current working directory if needed.
    fdtd.eval(custom_code)
    fdtd.constructFDTDandRect(x_input =0,y_input = 0, z_input = 0)

    #Results in error

In contrast, the following driver script executes without error, and add both the FDTD region as well as the rectangle.

.. code-block:: python

    fdtd = lumapi.FDTD()
    custom_code = open("MyConstructor.lsf", "r").read()#This assumes the current working directory has a file named “MyConstructor.lsf”. Use os.chdir to change the current working directory if needed.
    fdtd.eval(custom_code)
    fdtd.constructFDTDandRect(0,0,0)


Unsupported methods
--------------------

While most script commands are available, there are a few categories of commands that are not available for use in the Python API. For example, certain reserved keywords (such as “c” for the speed of light) are unavailable in Python. 
If you requires access to these variables, it is best to either define them in Python, or to use the :py:meth:`ansys.lumerical.core.FDTD.eval` method. 
However, if the :py:meth:`ansys.lumerical.core.FDTD.eval` method is used, you should be mindful that the variables in the Python and Lumerical scripting environments are not automatically shared. 

.. note::
    The :py:meth:`ansys.lumerical.core.FDTD.eval` is common to all products, and is available as :py:meth:`ansys.lumerical.core.MODE.eval`, :py:meth:`ansys.lumerical.core.DEVICE.eval`, and :py:meth:`ansys.lumerical.core.INTERCONNECT.eval`.

**Operators**

Script operators that are used in the Lumerical Scripting Language cannot be overloaded and used “as-is” using the same syntax in Python, therefore, they are not available, and you should use alternatives in Python. The unavailable operators include:

* Algebraic–For example,  `*`_ , `/`_ , `+`_ , `-`_ , `^`_

* Logical–For example,  `>=`_ , `<`_ , `>`_ , `&`_ , `and`_ , `|`_ , `or`_ , `!`_ , `~`_

* The  ? (print, display) operator used to screen and query available results

.. _*: https://optics.ansys.com/hc/en-us/articles/360034930833

.. _/ : https://optics.ansys.com/hc/en-us/articles/360034930853

.. _+ : https://optics.ansys.com/hc/en-us/articles/360034410254

.. _- : https://optics.ansys.com/hc/en-us/articles/360034930873

.. _^ : https://optics.ansys.com/hc/en-us/articles/360034410274

.. _>= : https://optics.ansys.com/hc/en-us/articles/360034930933

.. _< : https://optics.ansys.com/hc/en-us/articles/360034410334

.. _> : https://optics.ansys.com/hc/en-us/articles/360034930953

.. _& : https://optics.ansys.com/hc/en-us/articles/360034930973

.. _and : https://optics.ansys.com/hc/en-us/articles/360034410354

.. _| : https://optics.ansys.com/hc/en-us/articles/360034410374

.. _or : https://optics.ansys.com/hc/en-us/articles/360034930993

.. _! : https://optics.ansys.com/hc/en-us/articles/360034931013

.. _~ : https://optics.ansys.com/hc/en-us/articles/360034931033


Local documentation
--------------------

For information on the lumapi methods from within the environment we support Python docstrings for Lumerical session objects. This is the simplest way to determine the available script commands, and syntax. 
This contains information that is similar to the `Alphabetical List of Script Commands <https://optics.ansys.com/hc/en-us/articles/360034923553>`__. 
You can view the docstring by using the Python built-in function "help" or most ways rich interactive Python shells display docstrings (e.g. IPython, Jupyter Notebook):

.. code-block::

    help(fdtd.addfdtd)
    Help on method addfdtd in module lumapi:
    addfdtd(self, *args) method of lumapi.FDTD instance
    Adds an FDTD solver region to the simulation environment.  The extent of
    the solver region determines the simulated volume/area in FDTD
    Solutions.
    +-----------------------------------+-----------------------------------+
    | Syntax                            | Description                       |
    +-----------------------------------+-----------------------------------+
    | o.addfdtd()                       | Adds an FDTD solver region to the |
    |                                   | simulation environment.           |
    |                                   |                                   |
    |                                   | This function does not return any |
    |                                   | data.                             |
    +-----------------------------------+-----------------------------------+
    See Also
    set(), run()
    https://kb.lumerical.com/en/ref_scripts_addfdtd.html