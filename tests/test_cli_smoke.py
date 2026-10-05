"""
Smoke tests for CLI commands in scripts/acc.py
"""
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
ACC_SCRIPT = ROOT_DIR / "scripts" / "acc.py"


def run_acc(*args):
    cmd = [sys.executable, str(ACC_SCRIPT)] + list(args)
    return subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, encoding="utf-8")


def test_cli_help():
    res = run_acc()
    assert res.returncode == 0
    assert "Academic PKM CLI" in res.stdout


def test_cli_doctor():
    res = run_acc("doctor")
    assert res.returncode == 0
    assert "Academic PKM Doctor" in res.stdout
    assert "Python" in res.stdout
    assert "Data Lake" in res.stdout


def test_cli_bib_audit():
    res = run_acc("bib-audit")
    assert res.returncode == 0
    assert "Auditando acervo de referências" in res.stdout


def test_cli_catalog():
    res = run_acc("catalog")
    assert res.returncode == 0
    assert "Sincronizando catálogo" in res.stdout


def test_cli_providers():
    res = run_acc("providers")
    assert res.returncode == 0
    assert "Provedores Acadêmicos" in res.stdout
