.. _ref_session_management:

Session management
==================

Starting a local session
-------------------------

The Python API interacts with Lumerical products through sessions. The simplest way to create a session is by calling the relevant constructor for the Lumerical product and storing it in an object. These constructors construct objects derived from the :doc:`Lumerical class <../api/interface_class>`.

**Example**

.. code-block:: python

    #Starting a local Lumerical FDTD session

    fdtd = lumapi.FDTD()

**Parameters**

+----------------------------------------+------------------+
| **Product**                            | **Derived Class**|
+========================================+==================+
| Ansys Lumerical FDTD™                  | FDTD             |
+----------------------------------------+------------------+
| Ansys Lumerical MODE™                  | MODE             |
+----------------------------------------+------------------+
| Ansys Lumerical Multiphysics™          | DEVICE           |
+----------------------------------------+------------------+
| Ansys Lumerical INTERCONNECT™          | INTERCONNECT     |
+----------------------------------------+------------------+

You can also create multiple sessions, even if they're for the same product.

**Example**

.. code-block:: python

    #Starting two Lumerical MODE sessions one one Lumerical Multiphysics session
    mode1 = lumapi.MODE()
    mode2 = lumapi.MODE()
    device = lumapi.DEVICE()

Each of the product's constructor supports various parameters and keyword arguments. For more information, see :doc:`API reference <../api/index>`.


**Example**

.. code-block:: python

    #Loads and runs script.lsf while hiding the application window

    inc = lumapi.INTERCONNECT(filename="script.lsf", hide=True)

Starting a remote session using the interop server
--------------------------------------------------

Since the 2023 R1.2 release, you can use PyLumerical remotely on a Linux machine running the interop server (see :doc:`Interop server <interop_server>`  to configure and run the interop server). To use the remote API, you must use an additional parameter ``remoteArgs`` when starting a session to specify the IP address and port to use to connect to the interop server. 
This port must be the starting port defined for the interop server.

This parameter is a :class:`dict` with 2 fields, ``hostname`` and ``port``.

**Example**

.. code-block:: python

    #Start a remote Lumerical FDTD session
    remoteArgs = { "hostname": "192.168.215.129",
                 "port": 8989 }
    fdtd = lumapi.FDTD(hide=True, remoteArgs=remoteArgs)

Advanced session management
----------------------------

Wrapping the session in a function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In Python, you can use functions if you need to run numerous similar instances. For example, when sweeping over some optional parameters. For more information on how Lumerical sessions return results, see :doc:`Passing data <passing_data>` and :doc:`Working with simulation objects <working_with_simulation_objects>`.

**Example**

.. code-block:: python

    def myFunction(someOptionalParameter):
        fdtd = lumapi.FDTD()
        ...
        return importantResult

Using the "with" context manager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PyLumerical support Python "with" statement by giving well-defined entrance and exit behavior to Lumerical session objects in Python. If there are any errors within the "with" code block, the session still closes successfully, unlike in a function. Any error message you typically see in a Lumerical script environment is also displayed in the Python exception.

**Example**

.. code-block:: python

    with lumapi.FDTD(hide=True) as fdtd:
        fdtd.addfdtd()
        fdtd.setnamed("bad name") ## you will see
    LumApiError: "in setnamed, no items matching the name 'bad name' can be found."
        ...
    ## fdtd still successfully closes

Passing in command line arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Starting a session using PyLumerical is identical to running the solutions command line executable, as seen in these articles - `Windows <https://optics.ansys.com/hc/en-us/articles/360024812334-Running-simulations-using-the-Windows-command-prompt>`__ / `Linux <https://optics.ansys.com/hc/en-us/articles/360024974033-Running-simulations-using-terminal-on-Linux>`__. 
When starting a session using Python, use the ``serverArgs`` parameter to specify command line arguments.

**Example**

.. code-block:: python

    fdtd = lumapi.FDTD(serverArgs = {
                        'use-solve':True,
                        'platform':'offscreen',
                        'threads': '2’}
                )


The Python code above is equivalent to running the following command:

.. code-block::
    fdtd-solutions -threads 2 -platform offscreen -use-solve


Closing the session
--------------------

.. vale off

When the variables local to the function or context manager go out of scope, they are automatically deleted. Lumerical sessions automatically closes when all variable references pointing to it are deleted. 

.. vale on
The Lumerical session also automatically terminate after the python script reaches the end.

Python automatically deletes variables as they removed from scope, so most of the time you don't need to close a session manually. However, you can also do so explicitly using the following command.

.. code-block:: python

    inc.close() #inc is the name of the active session
