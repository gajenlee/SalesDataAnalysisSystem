from main import Main
import pytest
from io import StringIO
import sys


def test_cli_integration(monkeypatch):
    inputs = iter([1, 2, './sample_data/sales_data.csv', 1, "n", 3, 7])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    # Capture stdout
    captured_output = StringIO()
    sys.stdout = captured_output

    # Run the CLI
    cli = Main()
    cli.runMainLoop()

    # Assert the expected output
    assert "" in captured_output.getvalue()

    sys.stdout = sys.__stdout__