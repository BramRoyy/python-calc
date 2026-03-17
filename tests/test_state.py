from main import MAX, State, press, view


def fold(seq: list[str], maxn: int = MAX) -> State:
    state = State()
    for tok in seq:
        state = press(state, tok, maxn)
    return state


def test_digit_after_solve_starts_new_expr() -> None:
    got = fold(["2", "+", "3", "=", "7"])
    assert got.expr == "7"
    assert got.done is False


def test_operator_after_solve_continues_from_result() -> None:
    got = fold(["2", "+", "3", "=", "*", "2", "="])
    assert got.expr == "10"
    assert got.done is True


def test_digit_after_error_clears_error_first() -> None:
    got = fold(["9", "/", "0", "=", "8"])
    assert got.expr == "8"
    assert got.err is False


def test_operator_replacement() -> None:
    got = fold(["2", "+", "*"])
    assert got.expr == "2*"


def test_decimal_duplication_prevention() -> None:
    got = fold(["1", ".", ".", "2"])
    assert got.expr == "1.2"


def test_backspace_to_empty() -> None:
    got = fold(["7", "⌫"])
    assert got.expr == ""
    assert view(got) == "0"


def test_toggle_sign_current_token() -> None:
    got = fold(["2", "+", "3", "+/-"])
    assert got.expr == "2+-3"
    got = fold(["2", "+", "3", "+/-", "+/-"])
    assert got.expr == "2+3"


def test_expr_length_guard() -> None:
    got = fold(["9"] * (MAX + 5), maxn=MAX)
    assert len(got.expr) == MAX
