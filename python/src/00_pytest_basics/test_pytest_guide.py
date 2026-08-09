"""=============================================================================
                  COMPREHENSIVE PYTEST MASTERCLASS & GUIDE
=============================================================================
This file serves as an executable reference guide for modern, industry-standard
pytest patterns, ranging from basic assertions to advanced enterprise techniques.

Run with live stdout output:
    uv run pytest -s src/00_pytest_basics/test_pytest_guide.py

Select tests by marker:
    uv run pytest -m slow
    uv run pytest -m "not slow"
=============================================================================
"""

import sys
import time
from pathlib import Path
from typing import Generator

import pytest

sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    pytest.main(["-s", "-v", __file__])


# =============================================================================
# 1. BASIC ASSERTIONS & EXCEPTION TESTING
# =============================================================================

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero is not allowed!")
    return a / b


def test_basic_assertions():
    """Pytest uses standard Python `assert` statements—no need for self.assertEqual!"""
    result = divide(10, 2)
    assert result == 5.0
    assert isinstance(result, float)
    assert result > 0


def test_exception_handling():
    """Use `pytest.raises` to assert that specific exceptions are thrown,
    and optionally verify the exception message with `match` regex.
    """
    with pytest.raises(ValueError, match="Division by zero"):
        divide(10, 0)


# =============================================================================
# 2. PARAMETRIZATION (DRY - Don't Repeat Yourself)
# =============================================================================

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 2, 5.0),
        (20, 4, 5.0),
        (9, 3, 3.0),
        (-10, 2, -5.0),
        (0, 5, 0.0),
    ],
    ids=["standard", "even_division", "square_root_like", "negative_num", "zero_numerator"]
)
def test_divide_parametrized(a: float, b: float, expected: float):
    """Parametrization runs the same test function with different input sets.
    The `ids` parameter gives clear, readable labels in test reports!
    """
    assert divide(a, b) == expected


# =============================================================================
# 3. FIXTURES: SETUP, TEARDOWN, SCOPES, AND YIELD
# =============================================================================
# Fixtures manage setup (before test) and teardown/cleanup (after test).
# Scopes: 'function' (default), 'class', 'module', 'session'

@pytest.fixture(scope="function")
def sample_user_data() -> dict:
    """Function-scoped fixture: Executed freshly before every single test."""
    return {"id": 101, "username": "alice", "role": "admin"}


@pytest.fixture(scope="module")
def database_connection() -> Generator[str, None, None]:
    """Module-scoped fixture with Teardown using `yield`.
    Code before `yield` = Setup.
    Code after `yield`  = Cleanup/Teardown.
    """
    print("\n[SETUP] Connecting to In-Memory Database...")
    db = "Connected_DB_Instance"
    
    yield db  # Test receives this value

    print("\n[TEARDOWN] Closing Database Connection...")


def test_user_fixture(sample_user_data):
    """Fixtures are injected automatically by parameter name matching!"""
    assert sample_user_data["username"] == "alice"
    assert sample_user_data["role"] == "admin"


def test_db_fixture(database_connection):
    assert database_connection == "Connected_DB_Instance"


# =============================================================================
# 4. MONKEYPATCHING & MOCKING (Simulating external dependencies)
# =============================================================================

class ExternalAPIService:
    def fetch_user_balance(self, user_id: int) -> int:
        # Simulate an expensive network call
        time.sleep(5)
        raise TimeoutError("Real API is down!")


def get_user_status(service: ExternalAPIService, user_id: int) -> str:
    balance = service.fetch_user_balance(user_id)
    return "VIP" if balance > 1000 else "Standard"


def test_mocking_external_service(monkeypatch):
    """`monkeypatch` is a built-in pytest fixture to safely mock attributes,
    dict items, environment variables, or methods during testing.
    """
    # Define fake replacement function
    def mock_fetch_user_balance(self, user_id: int) -> int:
        return 2500  # Instantly returns mock value

    # Override real method with mock
    monkeypatch.setattr(ExternalAPIService, "fetch_user_balance", mock_fetch_user_balance)

    service = ExternalAPIService()
    status = get_user_status(service, user_id=101)
    
    assert status == "VIP"


# =============================================================================
# 5. CUSTOM MARKERS & SKIPPING TESTS
# =============================================================================
# You can define custom tags (e.g., @pytest.mark.slow, @pytest.mark.integration).

@pytest.mark.skip(reason="Legacy feature deprecated in v2.0")
def test_skipped_test():
    assert 1 == 2  # Will never be executed


@pytest.mark.skipif(sys.platform == "win32", reason="Linux/Mac specific behavior")
def test_unix_only_feature():
    assert True


@pytest.mark.slow
def test_expensive_computation():
    """Custom marker for slow tests. Run with `pytest -m slow`."""
    time.sleep(0.1)
    assert True


# =============================================================================
# 6. CAPTURING STDOUT & WARNS
# =============================================================================

def log_greeting(name: str) -> None:
    print(f"Hello, {name}!")


def test_stdout_capture(capsys):
    """`capsys` captures console outputs (`print` / `sys.stdout`)."""
    log_greeting("Bob")
    captured = capsys.readouterr()
    assert "Hello, Bob!" in captured.out


# =============================================================================
# 7. TEMPORARY FILES & DIRECTORIES (`tmp_path`)
# =============================================================================

def test_temporary_directory(tmp_path: Path):
    """`tmp_path` provides a unique, temporary pathlib.Path instance for file I/O operations."""
    test_file = tmp_path / "sample.txt"
    test_file.write_text("Hello Pytest World!", encoding="utf-8")

    assert test_file.exists()
    assert test_file.read_text(encoding="utf-8") == "Hello Pytest World!"