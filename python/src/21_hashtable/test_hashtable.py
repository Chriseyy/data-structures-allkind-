import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import time
import random
import pytest
from hashtable import HashTable

if __name__ == "__main__":
    pytest.main(["-s", "-v", __file__])


@pytest.fixture
def empty_hash_table():
    return HashTable(initial_capacity=8)


# --- 1. BASIC CRUD OPERATIONS ---

def test_put_and_get(empty_hash_table):
    """Test inserting and retrieving key-value pairs."""
    empty_hash_table.put("apple", 5)
    empty_hash_table.put("banana", 10)

    assert empty_hash_table.get("apple") == 5
    assert empty_hash_table.get("banana") == 10
    assert empty_hash_table.size == 2


def test_update_existing_key(empty_hash_table):
    """Updating an existing key should overwrite value without increasing size."""
    empty_hash_table.put("key", 100)
    assert empty_hash_table.get("key") == 100
    assert empty_hash_table.size == 1

    empty_hash_table.put("key", 200)
    assert empty_hash_table.get("key") == 200
    assert empty_hash_table.size == 1


def test_remove_key(empty_hash_table):
    """Test deleting key-value pairs."""
    empty_hash_table.put("a", 1)
    empty_hash_table.put("b", 2)

    assert empty_hash_table.remove("a") is True
    assert empty_hash_table.get("a") is None
    assert empty_hash_table.contains("a") is False
    assert empty_hash_table.size == 1

    # Removing non-existent key
    assert empty_hash_table.remove("non_existent") is False


def test_contains_and_default_get(empty_hash_table):
    """Test contains check and default values on missing keys."""
    empty_hash_table.put("exists", "yes")

    assert empty_hash_table.contains("exists") is True
    assert empty_hash_table.contains("missing") is False

    assert empty_hash_table.get("missing") is None
    assert empty_hash_table.get("missing", default="NOT_FOUND") == "NOT_FOUND"


def test_storing_none_as_value(empty_hash_table):
    """Edge Case: Storing None as a valid value should be distinguished from missing key."""
    empty_hash_table.put("null_key", None)

    assert empty_hash_table.contains("null_key") is True
    assert empty_hash_table.get("null_key") is None


# --- 2. COLLISION HANDLING & RESIZING ---

def test_collision_handling():
    """Forcing multiple keys into the same bucket (Chaining test)."""
    ht = HashTable(initial_capacity=4)

    # Class with custom __hash__ returning constant to force collision
    class ForceCollisionKey:
        def __init__(self, val):
            self.val = val
        def __hash__(self):
            return 42
        def __eq__(self, other):
            return self.val == other.val

    k1, k2, k3 = ForceCollisionKey("a"), ForceCollisionKey("b"), ForceCollisionKey("c")

    ht.put(k1, 100)
    ht.put(k2, 200)

    assert ht.get(k1) == 100
    assert ht.get(k2) == 200
    assert ht.size == 2


def test_dynamic_resizing_and_rehousing():
    """Test that table automatically doubles capacity when load factor > 0.75."""
    ht = HashTable(initial_capacity=4, load_factor_threshold=0.75)
    assert ht.capacity == 4

    # Inserting 3 items (3 / 4 = 0.75 load factor) -> No resize yet
    ht.put("k1", 1)
    ht.put("k2", 2)
    ht.put("k3", 3)
    assert ht.capacity == 4

    # Inserting 4th item (4 / 4 = 1.0 > 0.75) -> Triggers resize to capacity 8!
    ht.put("k4", 4)
    assert ht.capacity == 8
    assert ht.size == 4

    # All items must still be retrievable after rehousing
    for i in range(1, 5):
        assert ht.get(f"k{i}") == i


# --- 3. KEYS, VALUES & BENCHMARK ---

def test_keys_and_values_retrieval(empty_hash_table):
    """Test keys() and values() helper methods."""
    data = {"a": 1, "b": 2, "c": 3}
    for k, v in data.items():
        empty_hash_table.put(k, v)

    assert sorted(empty_hash_table.keys()) == ["a", "b", "c"]
    assert sorted(empty_hash_table.values()) == [1, 2, 3]


def test_benchmark_hash_table_vs_list_search():
    """Benchmark: Compares O(1) HashTable lookup vs O(n) List Linear Search on 10,000 items."""
    n = 10000
    ht = HashTable(initial_capacity=16)
    data_list = []

    for i in range(n):
        key = f"user_{i}"
        ht.put(key, i)
        data_list.append((key, i))

    target_key = f"user_{n - 1}"

    # Measure HashTable Get O(1)
    start = time.perf_counter()
    val_ht = ht.get(target_key)
    ht_time_ms = (time.perf_counter() - start) * 1000

    # Measure List Linear Search O(n)
    start = time.perf_counter()
    val_list = next(v for k, v in data_list if k == target_key)
    list_time_ms = (time.perf_counter() - start) * 1000

    print(f"\n\n{'='*65}")
    print(f"  HASH TABLE SEARCH BENCHMARK ({n} Items)")
    print(f"{'='*65}")
    print(f"HashTable Get O(1)  : {ht_time_ms:.5f} ms")
    print(f"List Linear Search O(n): {list_time_ms:.5f} ms")
    print(f"{'='*65}\n")

    assert val_ht == val_list == n - 1