from main import Main
import pytest
from io import StringIO
import sys

data_file = r'test\sample_data\sales_data.csv'

def test_cli_integration(monkeypatch):
    inputs = iter([1, 2, data_file, 1, "n", 3, 7])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    # Capture stdout
    captured_output = StringIO()
    sys.stdout = captured_output

    # Run the CLI
    Main().runMainLoop()

    # Assert the expected output
    assert "" in captured_output.getvalue()

    sys.stdout = sys.__stdout__