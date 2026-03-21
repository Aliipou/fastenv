"""Tests for fastenv core module."""
import os
import tempfile
import pytest
from fastenv.core import EnvFile, EnvVar


def make_env_file(content: str) -> str:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False)
    f.write(content)
    f.close()
    return f.name


def test_load_basic():
    path = make_env_file("KEY=value\nOTHER=123\n")
    env = EnvFile.load(path)
    assert "KEY" in env.vars
    assert env.vars["KEY"].value == "value"
    assert env.vars["OTHER"].value == "123"
    os.unlink(path)


def test_load_strips_quotes():
    path = make_env_file('QUOTED="hello world"\nSINGLE=\'test\'\n')
    env = EnvFile.load(path)
    assert env.vars["QUOTED"].value == "hello world"
    assert env.vars["SINGLE"].value == "test"
    os.unlink(path)


def test_load_ignores_comments():
    path = make_env_file("# This is a comment\nKEY=val\n")
    env = EnvFile.load(path)
    assert "KEY" in env.vars
    assert len(env.vars) == 1
    os.unlink(path)


def test_load_captures_comment():
    path = make_env_file("# My key description\nKEY=val\n")
    env = EnvFile.load(path)
    assert env.vars["KEY"].comment == "My key description"
    os.unlink(path)


def test_load_ignores_empty_lines():
    path = make_env_file("\nKEY=val\n\n")
    env = EnvFile.load(path)
    assert len(env.vars) == 1
    os.unlink(path)


def test_diff_only_in_a():
    a_path = make_env_file("A=1\nB=2\n")
    b_path = make_env_file("B=2\n")
    a, b = EnvFile.load(a_path), EnvFile.load(b_path)
    diff = EnvFile.diff(a, b)
    assert any("A" in line and "+" in line for line in diff)
    os.unlink(a_path); os.unlink(b_path)


def test_diff_only_in_b():
    a_path = make_env_file("A=1\n")
    b_path = make_env_file("A=1\nB=2\n")
    diff = EnvFile.diff(EnvFile.load(a_path), EnvFile.load(b_path))
    assert any("B" in line and "-" in line for line in diff)
    os.unlink(a_path); os.unlink(b_path)


def test_diff_value_change():
    a_path = make_env_file("WORKERS=4\n")
    b_path = make_env_file("WORKERS=16\n")
    diff = EnvFile.diff(EnvFile.load(a_path), EnvFile.load(b_path))
    assert any("~" in line and "WORKERS" in line for line in diff)
    os.unlink(a_path); os.unlink(b_path)


def test_diff_no_changes():
    path = make_env_file("A=1\nB=2\n")
    env = EnvFile.load(path)
    assert EnvFile.diff(env, env) == []
    os.unlink(path)


def test_to_dict():
    path = make_env_file("A=1\nB=hello\n")
    env = EnvFile.load(path)
    assert env.to_dict() == {"A": "1", "B": "hello"}
    os.unlink(path)
