import pytest
from dash import Dash
from app import app 


def test_header_is_present(dash_duo):
    dash_duo.start_server(app)
    header = dash_duo.find_element("h2")   # header is inside <h2>
    assert header is not None
    assert header.text.strip().lower() == "pink morsel visualizer"  # exact match


def test_visualization_is_present(dash_duo):
    dash_duo.start_server(app)
    graph = dash_duo.find_element("#sales-graph")  # check Graph by ID
    assert graph is not None



def test_region_picker_is_present(dash_duo):
    dash_duo.start_server(app)
    picker = dash_duo.find_element("#region-filter")  # RadioItems by ID
    assert picker is not None
    
    # Get all labels inside the radio buttons
    options = [opt.text.strip().lower() for opt in dash_duo.find_elements("#region-filter label")]
    expected = ["north", "east", "south", "west", "all"]
    
    assert options == expected
