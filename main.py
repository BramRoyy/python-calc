from __future__ import annotations

import ast
from dataclasses import dataclass
from tkinter import Event, StringVar

import customtkinter as ctk

OPS = "+-*/"
MAX = 128


@dataclass(frozen=True, slots=True)
class State:
    expr: str = ""
    err: bool = False
    done: bool = False


def view(state: State) -> str:
    if state.err:
        return state.expr
    if state.expr:
        return state.expr
    return "0"


def fmt(num: float) -> str:
    if num.is_integer():
        return str(int(num))
    return f"{num:g}"


def calc(text: str) -> float:
    tree = ast.parse(text, mode="eval")

    def run(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return run(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool):
                raise ValueError("invalid constant")
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise ValueError("invalid constant")
        if isinstance(node, ast.BinOp):
            left = run(node.left)
            right = run(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            raise ValueError("invalid operator")
        if isinstance(node, ast.UnaryOp):
            val = run(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +val
            if isinstance(node.op, ast.USub):
                return -val
            raise ValueError("invalid unary")
        raise ValueError("invalid syntax")

    return run(tree)


def span(expr: str) -> tuple[int, int] | None:
    if not expr:
        return None
    if expr[-1] in OPS:
        return None
    idx = len(expr) - 1
    while idx >= 0 and expr[idx] not in OPS:
        idx -= 1
    start = idx + 1
    if start > 0 and expr[start - 1] == "-":
        if start == 1 or expr[start - 2] in OPS:
            start -= 1
    return (start, len(expr))


def push(expr: str, tok: str, maxn: int) -> str:
    if len(expr) + len(tok) > maxn:
        return expr
    return expr + tok


def append(state: State, tok: str, maxn: int = MAX) -> State:
    if state.err:
        state = State()
    if state.done:
        state = State()
    if tok == ".":
        if not state.expr:
            return State("0.", False, False)
        if state.expr[-1] in OPS:
            return State(push(state.expr, "0.", maxn), False, False)
        pos = span(state.expr)
        if pos:
            cur = state.expr[pos[0] : pos[1]]
            if "." in cur:
                return state
        return State(push(state.expr, tok, maxn), False, False)
    return State(push(state.expr, tok, maxn), False, False)


def op(state: State, tok: str, maxn: int = MAX) -> State:
    if state.err:
        return state
    if not state.expr:
        if tok == "-":
            return State("-", False, False)
        return state
    if state.expr[-1] in OPS:
        return State(state.expr[:-1] + tok, False, False)
    return State(push(state.expr, tok, maxn), False, False)


def back(state: State) -> State:
    if state.err:
        return State()
    if not state.expr:
        return state
    return State(state.expr[:-1], False, False)


def clear(state: State) -> State:
    return State()


def reset(state: State) -> State:
    return State()


def toggle(state: State) -> State:
    if state.err:
        return State()
    pos = span(state.expr)
    if not pos:
        return state
    start = pos[0]
    end = pos[1]
    cur = state.expr[start:end]
    if cur.startswith("-"):
        return State(state.expr[:start] + cur[1:] + state.expr[end:], False, False)
    return State(state.expr[:start] + "-" + cur + state.expr[end:], False, False)


def solve(state: State) -> State:
    if state.err:
        return state
    if not state.expr:
        return state
    try:
        return State(fmt(calc(state.expr)), False, True)
    except ZeroDivisionError:
        return State("Error: division by zero", True, False)
    except SyntaxError, ValueError:
        return State("Error", True, False)


def press(state: State, tok: str, maxn: int = MAX) -> State:
    if tok in "0123456789.":
        return append(state, tok, maxn)
    if tok in OPS:
        return op(state, tok, maxn)
    if tok == "=":
        return solve(state)
    if tok == "CE":
        return clear(state)
    if tok == "C":
        return reset(state)
    if tok == "⌫":
        return back(state)
    if tok == "+/-":
        return toggle(state)
    return state


class App:
    def __init__(self) -> None:
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.win = ctk.CTk()
        self.win.title("Python Calc (POC)")
        self.win.geometry("360x520")
        self.win.resizable(False, False)

        self.state = State()
        self.var = StringVar(value=view(self.state))

        box = ctk.CTkFrame(self.win)
        box.pack(fill="both", expand=True, padx=16, pady=16)

        self.entry = ctk.CTkEntry(
            box, textvariable=self.var, justify="right", height=56
        )
        self.entry.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 12))
        self.entry.configure(state="readonly")

        rows = [
            ["CE", "C", "⌫", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["+/-", "0", ".", "="],
        ]

        for rid in range(6):
            box.grid_rowconfigure(rid, weight=1)
        for cid in range(4):
            box.grid_columnconfigure(cid, weight=1)

        for rid, row in enumerate(rows, start=1):
            for cid, tok in enumerate(row):
                btn = ctk.CTkButton(
                    box,
                    text=tok,
                    command=lambda key=tok: self.tap(key),
                    height=56,
                )
                if tok == "=":
                    btn.configure(fg_color="#1f6aa5")
                btn.grid(row=rid, column=cid, sticky="nsew", padx=4, pady=4)

        self.win.bind_all("<Key>", self.key)

    def draw(self) -> None:
        self.var.set(view(self.state))

    def tap(self, tok: str) -> None:
        self.state = press(self.state, tok)
        self.draw()

    def key(self, event: Event) -> str | None:
        key = event.keysym
        ch = event.char
        if ch and ch in "0123456789.+-*/":
            self.state = press(self.state, ch)
            self.draw()
            return "break"
        if key in {"Return", "KP_Enter"}:
            self.state = press(self.state, "=")
            self.draw()
            return "break"
        if key == "BackSpace":
            self.state = press(self.state, "⌫")
            self.draw()
            return "break"
        if key == "Escape":
            self.state = press(self.state, "C")
            self.draw()
            return "break"
        return None

    def run(self) -> None:
        self.win.mainloop()


def main() -> None:
    App().run()


if __name__ == "__main__":
    main()
