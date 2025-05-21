"""A test for starting a MODE session and verifying the connection using the Lumerical API."""

import ansys.lumerical.core as lumapi  # Import the lumapi module


def test_MODE_start_session():
    """
    Test the functionality of starting a MODE session and adding a rectangle with specified properties.

    This test performs the following steps:
    1. Starts a MODE session with the `hide` parameter set to True.
    2. Adds a rectangle with the name "test_rect" and an x span of 3e-6.
    3. Queries the value of the "x span" property of the rectangle.
    4. Asserts that the queried value matches the set value (3e-6).
    The test ensures that the rectangle is added correctly and that the property value can be accurately retrieved.
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
