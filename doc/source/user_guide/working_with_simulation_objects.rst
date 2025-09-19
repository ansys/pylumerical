.. _ref_working_with_simulation_objects:

Working with simulation objects
===============================

At a basic level, you can interact with simulation objects in the same way as when you use the Lumerical Script Language.
However, Lumerical scripting language interacts primarily with the currently selected object, which may not be clear from the Python code alone.
Therefore, PyLumerical also provides you with ways to interact with all objects that fits better with the Python coding style.

This article describes various ways to interact with simulation objects, such as structures, sources, and monitors.
For more information on how to use script commands in PyLumerical, see the article on :doc:`Script commands as methods <script_commands_as_methods>`.

Creating simulation objects
----------------------------

When adding a simulation object into Lumerical products using PyLumerical, you can set the values of properties at creation.
There are multiple ways of assigning the properties of objects when you create them.

Assigning properties with an ordered dict
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also use a Python :class:`dict` as a constructor to the object by assigning it to the attribute properties.
In Python, :class:`dict` ordering isn't guaranteed, so if there are properties that depend on other properties, an :class:`collections.OrderedDict` is necessary.
For example, in the example below, 'override global monitor settings' must be true before you can set 'frequency points'.
Using an :class:`collections.OrderedDict` is the safest way to ensure that PyLumerical processes all settings as intended.

**Example**

.. code-block:: python

    from collections import OrderedDict
    import ansys.lumerical.core as lumapi
    fdtd = lumapi.FDTD()
    props = OrderedDict([("name", "power"),("override global monitor settings", True),("x", 0.),("y", 0.4e-6),
                        ("monitor type", "linear x"),("frequency points", 10.0)])
    fdtd.addpower(properties=props)

If you don't have properties where ordering is important, you can use a regular :class:`dict`.

.. code-block::python

    props = {"name": "power",
         "x" : 0.0,
         "y" : 0.4e-6,
          "monitor type" : "linear x"}
    fdtd.addpower(properties=props)

Assigning properties with keyword arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


You can also assign properties upon construction using keyword arguments.
The property names are the same as those in the Lumerical products.
Properties with space in their name have spaces replaced by underscores.

When using keyword arguments, the order of assignment isn't guaranteed.
Therefore, if the order of assignment is important, use an :class:`collections.OrderedDict` instead.

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
    fdtd.addfdtd() # After the object is added, it is automatically selected, hence, fdtd.set will set dimensions to that object
    fdtd.set("x",0)
    fdtd.set("x span", 3e-6)

Linked properties
^^^^^^^^^^^^^^^^^^

In Lumerical, some object properties affect each other.
For example, in a geometry object, such as the rectangle, you can either set the dimension using ``x span`` and ``x``, or ``x min`` and ``x max``.
When you set linked properties, unexpected changes may occur to the object.

**Example**

.. code-block:: python

    with lumapi.FDTD() as fdtd:
        rect1 = fdtd.addrect(name = "rect1", x = 0, x_span = 1e-6, x_min = -1e-6, x_max = 1e-6)
        print(f"{rect1.x_span=}")

Returns

.. code-block:: python

    rect1.x_span=2e-06 # Note that this is different than what was set earlier from the x_span argument

Manipulating simulation objects
--------------------------------

When adding a new object to a Lumerical product session, PyLumerical returns a Python object representing that simulation object.
Manipulating the returned object makes changes to the corresponding object in the Lumerical product.

Direct attribute access
^^^^^^^^^^^^^^^^^^^^^^^^

Like normal Python objects, you can access Lumerical simulation object attributes as seen below.
The following code adds a rectangle and changes its dimensions.

**Example**

.. code-block:: python

    rectangle = fdtd.addrect(x = 2e-6, y = 0.0, z = 0.0)
    rectangle.x = -1e-6
    rectangle.x_span = 10e-6


Dict-like access
^^^^^^^^^^^^^^^^^

You can access parameters of the object like a Python dict.
The following example shows dict-like access of parameters in an FDTD rectangle object.

**Example**

.. code-block:: python

    rectangle = fdtd.addrect(x = 2e-6, y = 0.0, z = 0.0)
    rectangle["x"] = -1e-6
    rectangle["x span"] = 10e-6

Duplicate names
^^^^^^^^^^^^^^^^^

.. warning::
    Duplicate names of simulation object cause an undefined behavior in the script.

As shown in the script and animation below, if you have two rectangle objects named “Rect1,” manipulating them causes unknown behaviour, even if the Python variable assigned to them are different.

In these cases, PyLumerical gives a warning to inform you of the duplication.

**Example**

.. code-block:: python

    fdtd = lumapi.FDTD()
    rect_bot =fdtd.addrect(name = "Rect1",x_span = 1e-6, z_span = 0.25e-6, z=0) #Create a bottom rectangle, Rect1
    rect_top = fdtd.addrect(name = "Rect2", x_span = 1e-6, z_span = 0.25e-6, z=0.5e-6) #Create a top rectangle, Rect 2

    rect_top["x span"] = 2e-6 # expand the top rectangle

    rect_top["name"] = "Rect1" # Rename the top rectangle to Rect 1

    rect_top["y span"] = 2e-6 # Attempt to modify the top rectangle again..
    rect_top["x span"] = 4e-6
    # Note that the BOTTOM rectangle is modified because of the same name

.. image:: ../_static/images/duplicate_object_animation.gif
   :alt: Duplicate object animation
   :align: center

Parent and children objects
----------------------------

You can traverse the tree of objects in a Lumerical product using the parent or children of an object.

**Example**

.. code-block:: python

    # Create 3 rectangles and list their names
    device = lumapi.DEVICE()

    aRect = device.addrect(name="rectA")
    bRect = device.addrect(name="rectB")
    cRect = device.addrect(name="rectC")

    model = aRect.getParent()

    print(f'There are {len(model.getChildren())} children in the model. Their names are:')
    for child in model.getChildren():
        print(f'{child["name"]}')
