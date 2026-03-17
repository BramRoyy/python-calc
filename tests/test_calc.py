import pytest

from main import State, calc, fmt, solve


@pytest.mark.parametrize(
    ("text", "want"),
    [
        ("2+3", 5.0),
        ("9-4", 5.0),
        ("7*8", 56.0),
        ("9/3", 3.0),
        ("0.5+0.5", 1.0),
        ("-2*3", -6.0),
    ],
)
def test_calc_ok(text: str, want: float) -> None:
    assert calc(text) == want


def test_calc_zero_div() -> None:
    with pytest.raises(ZeroDivisionError):
        calc("9/0")


@pytest.mark.parametrize("text", ["", "2+", "a+1", "pow(2,3)", "[1]"])
def test_calc_invalid(text: str) -> None:
    with pytest.raises((SyntaxError, ValueError)):
        calc(text)


@pytest.mark.parametrize(
    ("num", "want"),
    [(5.0, "5"), (2.5, "2.5"), (10.25, "10.25")],
)
def test_fmt(num: float, want: str) -> None:
    assert fmt(num) == want


def test_solve_err_text_zero_div() -> None:
    got = solve(State("9/0", False, False))
    assert got.err is True
    assert got.expr == "Error: division by zero"


def test_solve_err_text_invalid() -> None:
    got = solve(State("2+", False, False))
    assert got.err is True
    assert got.expr == "Error"
