import ansys.lumerical.core as lumapi  # Import the lumapi module

def test_start_FDTD_session():
    """
    Test the starting of an FDTD session and variable manipulation.
    This test performs the following steps:
    1. Starts an FDTD session with the `hide` parameter set to True.
    2. Adds a variable with a specified name and value to the FDTD session.
    3. Modifies the variable by adding an offset value using the `eval` method.
    4. Reads back the modified variable value.
    5. Asserts that the modified value is equal to the expected value (original value + offset).
    The test ensures that variables can be correctly set, modified, and retrieved within an FDTD session.
    """
    # Start an FDTD session
    with lumapi.FDTD(hide=True) as fdtd:
        # Add a variable
        variable_name = "test_variable"
        variable_value = 42
        fdtd.putv(variable_name, variable_value)

        offset_value = 3
        fdtd.eval(f"{variable_name} =  {offset_value} + {variable_value};")
        
        # Read back the variable value
        read_value = fdtd.getv(variable_name)

        # Check if the set value and read value are the same
        assert variable_value + offset_value == read_value

def test_start_MODE_session():
    """
    Test the starting of a MODE session and adding a rectangle with specified properties.
    This test function performs the following steps:
    1. Starts a MODE session with the `hide` parameter set to True.
    2. Adds a rectangle with specified properties (`name` and `x span`).
    3. Queries the value of the `x span` property of the added rectangle.
    4. Asserts that the queried value matches the set value.
    Raises:
        AssertionError: If the queried `x span` value does not match the set value.
    """
    # Start a MODE session
    with lumapi.MODE(hide=True) as mode:
        # Add a rectangle
        rect_properties = {
            "name": "test_rect",
            "x span": 3e-6
        }
        mode.addrect(rect_properties)
        
        # Query the value of the property
        x_span_value = mode.getnamed("test_rect", "x span")
        
        # Check if the set value and read value are the same
        assert x_span_value == 3e-6

