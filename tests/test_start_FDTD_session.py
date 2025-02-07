import ansys.lumerical.core as lumapi  # Import the lumapi module

def test_start_FDTD_session():
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

