.. _ref_working_with_simulation_objects:

Working with simulation objects
===============================

At a basic level, simulation objects can be interacted with in the same way the Lumerical Script Language can be used to interact with the object. 
However, specific Pythonic approaches can also be used to interact with them.

This article describes unique ways to interact with simulation objects, such as structures, sources, and monitors, using the Python API. 
For more information on how to use script commands in the Python API, see the article on :doc:`Script commands as methods <script_commands_as_methods>`.

Creating simulation objects
----------------------------

When adding a simulation object into Lumerical products using the lumapi, the values of properties at creation can be set like using a constructor in programming. 
There are multiple ways of assigning the properties of objects when you create them.

Assigning properties with an ordered dict
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Python :class:`dict` can also be used as a constructor to the object by assigning it to the attribute properties. 
In Python, :class:`dict` ordering is not guaranteed, so if there are properties that depend on other properties, an :class:`collections.OrderedDict` is necessary. 
For example, in the example below, 'override global monitor settings' must be true before 'frequency points' can be set. 
Using an :class:`collections.OrderedDict` is the safest way to ensure that all settings are processed.

**Example**

.. code-block:: python

    from collections import OrderedDict
    import lumapi
    fdtd = lumapi.FDTD()
    props = OrderedDict([("name", "power"),("override global monitor settings", True),("x", 0.),("y", 0.4e-6),
                        ("monitor type", "linear x"),("frequency points", 10.0)])
    fdtd.addpower(properties=props)

If you do not have properties where ordering is important, you can use a regular :class:`dict`.

.. code-block::python

    props = {"name": "power",
         "x" : 0.0,
         "y" : 0.4e-6,
          "monitor type" : "linear x"}
    fdtd.addpower(properties=props)

Assigning properties with keyword arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Properties can also be assigned upon construction using keyword arguments. 
The property names are the same as those in the Lumerical products. 
Properties with space in their name have spaces replaced by underscores.

When using keyword arguments, the order of assignment is not guaranteed. 
Therefore, if the order of assignment is important, it is recommended to use an :class:`collections.OrderedDict`.

**Example**

.. code-block:: python

    fdtd = lumapi.FDTD()
    fdtd.addfdtd(dimension="2D", x=0.0e-9, y=0.0e-9, x_span=3.0e-6, y_span=1.0e-6)


Assigning properties with “set”
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to the two methods above, you can also use the traditional Lumerical scripting method `set <https://optics.ansys.com/hc/en-us/articles/360034928773-set-Script-command>`__ or `setnamed <https://optics.ansys.com/hc/en-us/articles/360034928793-setnamed-Script-command>`__ to directly set the properties after the object is created.

**Example**

.. code-block:: python

    fdtd = lumapi.FDTD()
    fdtd.addfdtd() #After the object is added, it is automatically selected, hence, fdtd.set will set dimensions to that object
    fdtd.set("x",0)
    fdtd.set("x span", 3e-6)

Linked properties
^^^^^^^^^^^^^^^^^^

In Lumerical, some object properties are linked and affect each other. 
For example, in a geometry object (such as the rectangle), the dimension can either be set using ``x span`` and ``x``, or ``x min`` and ``x max``. 
When setting properties that are linked, unexpected changes may occur to the object.

**Example**

.. code-block:: python

    with lumapi.FDTD() as fdtd:
    rect1 = fdtd.addrect(name = "rect1", x = 0, x_span = 1e-6, x_min = -1e-6, x_max = 1e-6)
    print(f"{rect1.x_span=}")

Returns

.. code-block:: python

    rect1.x_span=2e-06 #Note that this is different than what was set earlier from the x_span argument

Manipulating Simulation Objects
--------------------------------

When adding a new object to a Lumerical product session, a Python object representing that simulation object is returned. 
Manipulating the returned object will make changes to the corresponding object in the Lumerical product.

Direct Attribute Access
^^^^^^^^^^^^^^^^^^^^^^^^

Like normal Python objects, Lumerical simulation object attributes can be accessed directly as seen below. 
The following code adds a rectangle and changes its dimensions.

**Example**

.. code-block:: python
    rectangle = fdtd.addrect(x = 2e-6, y = 0.0, z = 0.0)
    rectangle.x = -1e-6
    rectangle.x_span = 10e-6


Dict-Like Access
^^^^^^^^^^^^^^^^^

Parameters of the representative object can also be accessed like a Python dict. 
An example of the dict-like access of parameters in an FDTD rectangle object is shown below.

**Example**

.. code-block:: python

    rectangle = fdtd.addrect(x = 2e-6, y = 0.0, z = 0.0)
    rectangle["x"] = -1e-6
    rectangle["x span"] = 10e-6

Duplicate names
^^^^^^^^^^^^^^^^^

.. warning::
    Duplicate names of simulation object cause an undefined behavior in the script. 

As shown in the script and animation below, if two rectangle objects are named “Rect1,” manipulating them causes unknown behaviour, even if the Python variable assigned to them are different.

In these cases, a warning is outputted to inform you of the duplication.

**Example**

.. code-block:: python

    fdtd = lumapi.FDTD()
    rect_bot =fdtd.addrect(name = "Rect1",x_span = 1e-6, z_span = 0.25e-6, z=0) #Create a bottom rectangle, Rect1
    rect_top = fdtd.addrect(name = "Rect2", x_span = 1e-6, z_span = 0.25e-6, z=0.5e-6) #Create a top rectange, Rect 2

    rect_top["x span"] = 2e-6 #expand the top rectangle

    rect_top["name"] = "Rect1" #Rename the top rectangle to Rect 1

    rect_top["y span"] = 2e-6 #Attempt to modify the top rectangle again..
    rect_top["x span"] = 4e-6
    #Note that the BOTTOM rectangle is modified because of the same name

.. image:: ../_static/duplicate_object_animation.gif
   :alt: Duplicate object animation
   :align: center

Parent and Children Objects
----------------------------

The tree of objects in a Lumerical product can be traversed using the parent or children of an object.

**Example**

.. code-block:: python

    #Create 3 rectangles and list their names
    device = lumapi.DEVICE()

    aRect = device.addrect(name="rectA")
    bRect = device.addrect(name="rectB")
    cRect = device.addrect(name="rectC")

    model = aRect.getParent()

    print(f'There are {len(model.getChildren())} children in the model. Their names are:')
    for child in model.getChildren():
        print(f'{child["name"]}') 