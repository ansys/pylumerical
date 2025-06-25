.. _ref_passing_data:

Passing data
=============

When driving Lumerical's tools from the Python API, a connection is established between the environments, but they do not share a workspace. 
Instead, as variables are passed back and forth as exact copies. When variables are passed back and forth, they are also translated between Lumerical types and Python types. 
This article describes how basic datatypes are translated between the Python environment and the Lumerical product, performance considerations, and best practices associated with it.

For more information on how to work with datasets, which are composed of these basic datatypes, for processing of simulation results and handling of Lumerical datasets, see the article on :doc:`Accessing simulation results <accessing_simulation_results>`.

+----------------+-----------------------+
| Lumerical      | Python                |
+================+=======================+
| String         | :class:`str`          |
+----------------+-----------------------+
| Real           | :class:`float`        |
+----------------+-----------------------+
| Complex        | :class:`numpy.ndarray`|
+----------------+-----------------------+
| `Matrix`_      | :class:`numpy.ndarray`|
+----------------+-----------------------+
| `Cell array`_  | :class:`list`         |
+----------------+-----------------------+
| `Struct`_      | :class:`dict`         |
+----------------+-----------------------+
| `Dataset`_     | :class:`dict`         |
+----------------+-----------------------+

.. _Matrix: https://optics.ansys.com/hc/en-us/articles/360034929613-matrix-Script-command
.. _Cell array: https://optics.ansys.com/hc/en-us/articles/360034929913-cell-Script-command
.. _Struct: https://optics.ansys.com/hc/en-us/articles/360034409574-struct-Script-command
.. _Dataset: https://optics.ansys.com/hc/en-us/articles/360034409554-Introduction-to-Lumerical-datasets

Python to Lumerical conversions
--------------------------------

When a variable is sent from the Python workspace to Lumerical products, such as when setting parameters, or when using Lumerical scripting functions for further post processing, the following rules are followed.

String
^^^^^^

String values passed from Python are directly converted into string values in the Lumerical workspace.

Real number
^^^^^^^^^^^^

Any real numbers passed from Python into Lumerical are converted into float. Since the Lumerical workspace does not support integer types, any integer types are also converted into float.

Complex number
^^^^^^^^^^^^^^

Passing complex numbers from Python into Lumerical requires it to be encapsulated in a single element numpy array. In Python, the complex variable “j” should be used.

Numpy array
^^^^^^^^^^^^^

Numpy arrays from Python are converted into matrices in Lumerical, complex-valued numpy arrays are supported.

List
^^^^

Lists from Python, which can contain any of the basic types mentioned in this section, are converted into cell arrays in the Lumerical scripting workspace.

Dict
^^^^

Dictionaries from Python, which can contain any of the basic types mentioned in this section, are converted into structures in Lumerical. The order of the dictionary is not preserved.

Other types
^^^^^^^^^^^^

All other types, except those mentioned above, are not supported and will result in an error if it is attempted to be passed into Lumerical through the Python API.

Lumerical to Python conversions
--------------------------------

When retrieving a variable from the Lumerical product to the Python workspace, such as when obtaining simulation results from simulation objects and monitors, or when retrieving return values from a Lumerical scripting function, the following rules are followed.

String
^^^^^^

When a string is retrieved from Lumerical, it will be returned to the Python environment as a string.

Real number
^^^^^^^^^^^^

The value of any real number returned to the Python workspace from Lumerical will be float. Since Lumerical does not support integers, even if a value is passed into Lumerical as integer, it will be retrieved as float.

Complex number
^^^^^^^^^^^^^^

Complex numbers from Lumerical will be automatically converted to a 1x1 numpy array, with the complex number being the only element in the array.

For example, the following script creates a Lumerical scripting function that returns a complex value and checks its type, length, and value in Python.

.. code-block:: python
    
    fdtd = lumapi.FDTD()
    fdtd.eval("function return_complex(){return 1+1i;}")
    complex_value = fdtd.return_complex()
    print(f'Returned value is of type {type(complex_value)}, length {complex_value.size} with value {complex_value[0]}')

Returns

.. code-block::
    
    Returned value is of type , length 1 with value [1.+1.j]

.. note::
    
    In Lumerical, the complex variable “i” is used, whereas in Python, the complex variable “j” is used.

Matrix
^^^^^^^

Matrices from the Lumerical product will be returned as numpy arrays of the same size. These arrays also support complex data as its elements.

Struct
^^^^^^

Structures from the Lumerical workspace will be returned to Python as a dictionary, with each field turned into an attribute. These dictionaries are indexed by fields and are not ordered.

For example, the following script creates a Lumerical scripting function that returns a structure checks its type and contents in Python.

.. code-block:: python
    
    fdtd = lumapi.FDTD()
    fdtd.eval('function return_struct(){return {"name":"MyStruct","real value": 1e-6, "complex value": 1+1i, "matrix": matrix(2,2)};}')
    struct_returned = fdtd.return_struct()

    print(f"The type of the returned value is {type(struct_returned)}, the values within are: \n")
    for key,value in struct_returned.items():
        print(f"Field - {key}, Value - {value}, Type - {type(value)} \n")

Returns

.. code-block::
    
    The type of the returned value is <class 'dict'>, the values within are: 
    Field - complex value, Value - [[1.+1.j]], Type - <class 'numpy.ndarray'>
    Field - matrix, Value - [[0. 0.] [0. 0.]], Type - <class 'numpy.ndarray'>
    Field - name, Value - MyStruct, Type - <class 'str'>
    Field - real value, Value - 1e-06, Type - <class 'float'>

Cell array
^^^^^^^^^^^^^

When cell arrays are retrieved from Lumerical, they are converted into Python lists. Elements of these lists can contain any of the basic data types.

For example, the following script creates a Lumerical function that creates a cell array with a string, a matrix, and a structure that has another cell array as its element, returns it to the Python workspace, and checks each element.

.. code-block:: python
    
    fdtd = lumapi.FDTD()
    fdtd.eval('function return_cell(){mycell = cell(3); mycell{1}="Hello World"; mycell{2} = matrix(2,2); mycell{3} = {"name":"Lumerical", "value":cell(3)}; return mycell;}')
    cell_returned = fdtd.return_cell()

Returns

.. code-block::
    
    The type of the returned value is <class 'list'>, the values within are:

    Value - Hello World, Type - <class 'str'>

    Value - [[0. 0.] [0. 0.]], Type - <class 'numpy.ndarray'>

    Value - {'name': 'Lumerical', 'value': [0.0, 0.0, 0.0]}, Type - <class 'dict'>

Explicit transfer functions
-----------------------------

Two explicit transfer functions, :py:meth:`ansys.lumerical.core.FDTD.getv` and :py:meth:`ansys.lumerical.core.FDTD.putv` are available to manually retrieve variables from the Lumerical workspace and placing them into the workspace, respectively. 
While these can be useful in a small number of circumstances, it is recommended to avoid using these functions, as changes to variables in one workspace does not automatically synchronize with the other, and interactions with simulation objects, including entering inputs and retrieving outputs, can usually be done with Python methods themselves.

.. note::

    :py:meth:`ansys.lumerical.core.FDTD.getv` and :py:meth:`ansys.lumerical.core.FDTD.putv` is common to all products, and is available in :class:`ansys.lumerical.core.MODE`, :class:`ansys.lumerical.core.DEVICE`, and :class:`ansys.lumerical.core.INTERCONNECT` as well.

Transfer speed
-----------------

Typically, this transfer does not present an issue in terms of fidelity, nor does it typically present a bottleneck in terms of speed. 
However, when working with very large datasets it may be important to take this into consideration if efficiency is imperative.

Best practices
-----------------

* If you are creating a large number of variables or repeatedly sending and retrieving data in a loop with many API calls, it could be more efficient to do so inside the Lumerical script environment by using the :py:meth:`ansys.lumerical.core.FDTD.eval` command such that this all happens in one operation.
