import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


import pytest
from dynamic_array import DynamicArray

# uv run pytest
if __name__ == "__main__":
    pytest.main([__file__])

# --- FIXTURES ---

@pytest.fixture
def empty_array():
    """Returns an empty array with initial capacity of 2."""
    return DynamicArray(capacity=2)


@pytest.fixture
def filled_array():
    """Returns an array populated with 3 elements: [10, 20, 30] (capacity=4)."""
    arr = DynamicArray(capacity=2)
    arr.pushback(10)
    arr.pushback(20)
    arr.pushback(30)
    return arr


# --- INITIALIZATION TESTS ---

def test_initialization():
    arr = DynamicArray(capacity=5)
    assert arr.getSize() == 0
    assert arr.getCapacity() == 5

def test_initialization_minimum_capacity():
    # Tests capacity fallback when passing <= 0
    arr = DynamicArray(capacity=0)
    assert arr.getCapacity() == 1


# --- GET & SET TESTS ---

def test_get_and_set(filled_array):
    assert filled_array.get(0) == 10
    assert filled_array.get(1) == 20
    
    filled_array.set(1, 99)
    assert filled_array.get(1) == 99


# --- PUSHBACK & UPSIZING TESTS ---

def test_pushback_triggers_upsize(empty_array):
    empty_array.pushback(1)
    empty_array.pushback(2)
    assert empty_array.getCapacity() == 2
    
    # Exceeding capacity triggers 2x upsize
    empty_array.pushback(3)
    assert empty_array.getCapacity() == 4
    assert empty_array.getSize() == 3
    assert empty_array.get(2) == 3


# --- POPBACK & DOWNSIZING TESTS ---

def test_popback_basic(filled_array):
    val = filled_array.popback()
    assert val == 30
    assert filled_array.getSize() == 2

def test_popback_triggers_downsize():
    arr = DynamicArray(capacity=2)
    # Grow to capacity 8
    for i in range(5):
        arr.pushback(i)
    assert arr.getCapacity() == 8

    # Pop elements until size <= 25% of capacity (2 out of 8)
    arr.popback()  # size = 4
    arr.popback()  # size = 3
    assert arr.getCapacity() == 8

    # Size drops to 2 (<= 25% of 8) -> Downsize to 4
    arr.popback()
    assert arr.getSize() == 2
    assert arr.getCapacity() == 4

def test_popback_empty_raises_exception(empty_array):
    with pytest.raises(IndexError, match="pop from empty DynamicArray"):
        empty_array.popback()


# --- INSERTION TESTS ---

@pytest.mark.parametrize("index, val, expected", [
    (0, 5, [5, 10, 20, 30]),   # Insert at beginning
    (1, 15, [10, 15, 20, 30]), # Insert in middle
    (3, 40, [10, 20, 30, 40]), # Insert at current end (size index)
])
def test_insert_positions(filled_array, index, val, expected):
    filled_array.insert(index, val)
    assert filled_array.getSize() == len(expected)
    for i, expected_val in enumerate(expected):
        assert filled_array.get(i) == expected_val


# --- REMOVAL TESTS ---

@pytest.mark.parametrize("remove_index, expected_removed, expected_remaining", [
    (0, 10, [20, 30]), # Remove first element
    (1, 20, [10, 30]), # Remove middle element
    (2, 30, [10, 20]), # Remove last element
])
def test_remove_positions(filled_array, remove_index, expected_removed, expected_remaining):
    removed = filled_array.remove(remove_index)
    assert removed == expected_removed
    assert filled_array.getSize() == len(expected_remaining)
    for i, expected_val in enumerate(expected_remaining):
        assert filled_array.get(i) == expected_val

def test_remove_triggers_downsize():
    arr = DynamicArray(capacity=8)
    for i in range(5):
        arr.pushback(i)
    
    # Remove elements to reach size 2 (<= 25% of 8) -> Downsize to 4
    arr.remove(0)
    arr.remove(0)
    arr.remove(0)
    assert arr.getSize() == 2
    assert arr.getCapacity() == 4


# --- BOUNDS & EXCEPTION EDGE CASES ---

@pytest.mark.parametrize("invalid_index", [-1, 3, 10])
def test_get_out_of_bounds(filled_array, invalid_index):
    with pytest.raises(IndexError, match="Index out of bounds"):
        filled_array.get(invalid_index)

@pytest.mark.parametrize("invalid_index", [-1, 3, 10])
def test_set_out_of_bounds(filled_array, invalid_index):
    with pytest.raises(IndexError, match="Index out of bounds"):
        filled_array.set(invalid_index, 99)

@pytest.mark.parametrize("invalid_index", [-1, 4, 10])
def test_insert_out_of_bounds(filled_array, invalid_index):
    with pytest.raises(IndexError, match="Index out of bounds"):
        filled_array.insert(invalid_index, 99)

@pytest.mark.parametrize("invalid_index", [-1, 3, 10])
def test_remove_out_of_bounds(filled_array, invalid_index):
    with pytest.raises(IndexError, match="Index out of bounds"):
        filled_array.remove(invalid_index)