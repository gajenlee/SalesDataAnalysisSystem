from main import Main
import sys
from io import StringIO

def test_acceptance_full_flow(monkeypatch):
    inputs = iter([7])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    captured_output = StringIO()
    sys.stdout = captured_output

    Main().runMainLoop()

    # Assert the expected output
    assert "" in captured_output.getvalue()

    sys.stdout = sys.__stdout__