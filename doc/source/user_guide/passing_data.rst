.. _ref_passing_data:

Passing data
=============

.. vale off

..
    Intentional use of passive voice here
When driving Lumerical's tools using PyLumerical, the Lumerical environment is connected with the Python environment, but they don't share a workspace. 

.. vale on
Instead, PyLumerical passes variables between the Lumerical and Python environments as exact copies. During the transition, PyLumerical translates variables between Lumerical types and Python types. 
This article describes how PyLumerical translates basic data types between the Python environment and the Lumerical product, performance considerations, and best practices associated with it.

For more information on how to work with datasets, which includes these basic data types and typically contain simulation results, see the article on :doc:`Accessing simulation results <accessing_simulation_results>`.

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

When you send a variable from the Python workspace to Lumerical products, such as when setting parameters, or when using Lumerical scripting functions for further post processing, PyLumerical uses the following rules.

String
^^^^^^

String values passed from Python are directly converted into string values in the Lumerical workspace.

Real number
^^^^^^^^^^^^

PyLumerical converts real numbers from Python into float values in Lumerical. Since the Lumerical workspace doesn't support integer types, any integer types are also converted into float.

Complex number
^^^^^^^^^^^^^^

You must encapsulate complex numbers in a single element numpy array before passing them from Python into Lumerical. In Python, the complex variable is “j”, whereas in Lumerical, it's “i”.

Numpy array
^^^^^^^^^^^^^

PyLumerical converts numpy arrays from Python into matrices in Lumerical, and it supports complex-valued numpy arrays.

List
^^^^

PyLumerical converts lists from Python, which can contain any of the basic types mentioned in this section, into cell arrays in the Lumerical scripting workspace.

Dict
^^^^

PyLumerical converts dictionaries from Python, which can contain any of the basic types mentioned in this section, into structures in Lumerical. The order of the dictionary isn't preserved.

Other types
^^^^^^^^^^^^

All other types, except those mentioned above, aren't supported and results in an error if your script attempts to pass them into the Lumerical workspace.

Lumerical to Python conversions
--------------------------------

When retrieving a variable from the Lumerical product to the Python workspace, such as when obtaining simulation results from simulation objects and monitors, or when retrieving return values from a Lumerical scripting function, PyLumerical uses the following rules.

String
^^^^^^

When PyLumerical retrieves a string from Lumerical, it returns the variable into the Python environment as a string.

Real number
^^^^^^^^^^^^

When PyLumerical retrieves any real number from Lumerical, it returns the value into the Python environment as a float. Since Lumerical doesn't support integers, even if you previously passed a variable into Lumerical as integer, PyLumerical still retrieves it as float.

Complex number
^^^^^^^^^^^^^^

PyLumerical automatically converts complex numbers into a 1x1 numpy array in the Python environment, with the complex number being the only element in that array.

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
    
    In Lumerical, the complex variable is “i”, whereas in Python, the complex variable is “j”.

Matrix
^^^^^^^

PyLumerical retrieves matrices as numpy arrays of the same size. These arrays also support complex data as their elements.

Struct
^^^^^^

PyLumerical converts structures from Lumerical into Python dictionaries, with each field turned into an attribute. The keys of the dictionary are field names, and it's order from Lumerical isn't preserved.

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

PyLumerical retrieves Lumerical cell arrays as Python lists. Elements of these lists can contain any of the basic data types.

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

Two explicit transfer functions, :py:meth:`ansys.lumerical.corTD.getv` and :py:meth:`ansys.lumerical.core.FDTD.putv` are available to manually retrieve variables from the Lumerical workspace and placing them into the workspace, respectively. 
While these can be useful in a small number of circumstances, avoid using these functions unless it's necessary, as changes to variables in one workspace doesn't automatically synchronize with the other. Usually, you can use Python methods to interact with simulation objects, including entering inputs and retrieving outputs.

.. note::

    :py:meth:`ansys.lumerical.core.FDTD.getv` and :py:meth:`ansys.lumerical.core.FDTD.putv` is common to all products, and is available in :class:`ansys.lumerical.core.MODE`, :class:`ansys.lumerical.core.DEVICE`, and :class:`ansys.lumerical.core.INTERCONNECT` as well.

Transfer speed
-----------------

Typically, this transfer doesn't present an issue in terms of fidelity, nor does it typically present a bottleneck in terms of speed. 
However, when working with very large datasets it may be important to take this into consideration if efficiency is imperative.

Best practices
-----------------

* If you are creating a large number of variables or repeatedly sending and retrieving data in a loop with many API calls, it could be more efficient to do so inside the Lumerical script environment by using the :py:meth:`ansys.lumerical.core.FDTD.eval` command such that this all happens in one operation.
