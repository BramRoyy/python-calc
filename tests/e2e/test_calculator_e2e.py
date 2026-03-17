from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(sys.platform != "win32", reason="Windows only"),
    pytest.mark.timeout(30),
]


def esc(tok: str) -> str:
    if tok == "+":
        return "{+}"
    if tok == "*":
        return "{*}"
    if tok == "=":
        return "{ENTER}"
    if tok == "C":
        return "{ESC}"
    if tok == "⌫":
        return "{BACKSPACE}"
    return tok


def diag(win, root: Path, name: str) -> None:
    root.mkdir(parents=True, exist_ok=True)
    text = []
    for ctrl in win.descendants():
        try:
            val = ctrl.window_text()
            if val:
                text.append(val)
        except Exception:
            continue
    (root / f"{name}.txt").write_text("\n".join(text), encoding="utf-8")
    try:
        win.capture_as_image().save(root / f"{name}.png")
    except Exception:
        pass


def read(win) -> str:
    try:
        ctrl = win.child_window(class_name="Edit").wrapper_object()
        return str(ctrl.window_text())
    except Exception:
        ctrl = win.child_window(control_type="Edit").wrapper_object()
        val = ctrl.get_value()
        if val is None:
            return ctrl.window_text()
        return str(val)


def send(win, seq: list[str]) -> None:
    win.set_focus()
    win.type_keys("".join(esc(tok) for tok in seq), set_foreground=True, pause=0.02)


def wait(win, want: str, path: Path, name: str) -> None:
    end = time.monotonic() + 2.0
    while time.monotonic() < end:
        got = read(win)
        if got == want:
            return
        time.sleep(0.05)
    diag(win, path, name)
    assert read(win) == want


@pytest.fixture
def win() -> object:
    app_cls: Any = None
    try:
        from pywinauto import Application

        app_cls = Application
    except Exception as err:
        pytest.skip(f"pywinauto unavailable: {err}")
    if app_cls is None:
        pytest.skip("pywinauto unavailable")

    root = Path(__file__).resolve().parents[2]
    proc = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    app = app_cls(backend="win32")
    end = time.monotonic() + 10.0
    last = None
    while time.monotonic() < end:
        try:
            app.connect(process=proc.pid, timeout=1)
            got = app.window(title_re=r".*Python Calc \(POC\).*")
            got.wait("exists visible ready", timeout=3)
            yield got
            break
        except Exception as err:
            last = err
            time.sleep(0.1)
    else:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=2)
        pytest.skip(f"cannot attach app window in this session: {last}")
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=3)


def test_add(win, tmp_path: Path) -> None:
    send(win, ["C", "2", "+", "3", "="])
    wait(win, "5", tmp_path, "test_add")


def test_multiply(win, tmp_path: Path) -> None:
    send(win, ["C", "7", "*", "8", "="])
    wait(win, "56", tmp_path, "test_multiply")


def test_div_zero(win, tmp_path: Path) -> None:
    send(win, ["C", "9", "/", "0", "="])
    wait(win, "Error: division by zero", tmp_path, "test_div_zero")


def test_recover_after_error(win, tmp_path: Path) -> None:
    send(win, ["C", "9", "/", "0", "=", "7"])
    wait(win, "7", tmp_path, "test_recover_after_error")
