import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pytest
from singly_linked_list import SinglyLinkedList

# uv run pytest
if __name__ == "__main__":
    pytest.main([__file__])

# --- FIXTURES ---

@pytest.fixture
def empty_list():
    """Returns a fresh empty SinglyLinkedList."""
    return SinglyLinkedList()


@pytest.fixture
def filled_list():
    """Returns a SinglyLinkedList with 3 elements: [10, 20, 30]."""
    sll = SinglyLinkedList()
    sll.append(10)
    sll.append(20)
    sll.append(30)
    return sll


# --- INITIALIZATION & BASIC STATE TESTS ---

def test_initialization(empty_list):
    assert empty_list.getSize() == 0
    assert empty_list.head is None
    assert empty_list.tail is None


# --- PREPEND & APPEND TESTS ---

def test_prepend(empty_list):
    empty_list.prepend(20)
    assert empty_list.getSize() == 1
    assert empty_list.head.val == 20
    assert empty_list.tail.val == 20

    empty_list.prepend(10)
    assert empty_list.getSize() == 2
    assert empty_list.head.val == 10
    assert empty_list.tail.val == 20
    assert empty_list.get(0) == 10
    assert empty_list.get(1) == 20


def test_append(empty_list):
    empty_list.append(10)
    assert empty_list.getSize() == 1
    assert empty_list.head.val == 10
    assert empty_list.tail.val == 10

    empty_list.append(20)
    assert empty_list.getSize() == 2
    assert empty_list.head.val == 10
    assert empty_list.tail.val == 20
    assert empty_list.get(0) == 10
    assert empty_list.get(1) == 20


# --- INSERTION TESTS ---

@pytest.mark.parametrize("index, val, expected", [
    (0, 5, [5, 10, 20, 30]),      # Insert at Head
    (1, 15, [10, 15, 20, 30]),    # Insert in Middle
    (2, 25, [10, 20, 25, 30]),    # Insert in Middle
    (3, 40, [10, 20, 30, 40]),    # Insert at Tail (index == size)
])
def test_insert_positions(filled_list, index, val, expected):
    filled_list.insert(index, val)
    assert filled_list.getSize() == len(expected)
    for i, expected_val in enumerate(expected):
        assert filled_list.get(i) == expected_val


def test_insert_pointers_update(filled_list):
    # Test head pointer update via insert
    filled_list.insert(0, 1)
    assert filled_list.head.val == 1

    # Test tail pointer update via insert
    filled_list.insert(4, 99)
    assert filled_list.tail.val == 99


# --- REMOVAL TESTS ---

@pytest.mark.parametrize("remove_index, expected_removed, expected_remaining", [
    (0, 10, [20, 30]),  # Remove Head
    (1, 20, [10, 30]),  # Remove Middle
    (2, 30, [10, 20]),  # Remove Tail
])
def test_remove_positions(filled_list, remove_index, expected_removed, expected_remaining):
    removed = filled_list.remove(remove_index)
    assert removed == expected_removed
    assert filled_list.getSize() == len(expected_remaining)
    for i, expected_val in enumerate(expected_remaining):
        assert filled_list.get(i) == expected_val


def test_remove_until_empty(empty_list):
    empty_list.append(100)
    removed = empty_list.remove(0)
    assert removed == 100
    assert empty_list.getSize() == 0
    assert empty_list.head is None
    assert empty_list.tail is None


def test_remove_tail_pointer_update(filled_list):
    filled_list.remove(2)  # Remove Tail (30)
    assert filled_list.tail.val == 20


# --- REVERSE TESTS ---

def test_reverse_filled_list(filled_list):
    filled_list.reverse()
    assert filled_list.get(0) == 30
    assert filled_list.get(1) == 20
    assert filled_list.get(2) == 10
    assert filled_list.head.val == 30
    assert filled_list.tail.val == 10


def test_reverse_single_and_empty_list(empty_list):
    # Empty list reversal
    empty_list.reverse()
    assert empty_list.head is None
    assert empty_list.tail is None

    # Single element list reversal
    empty_list.append(42)
    empty_list.reverse()
    assert empty_list.head.val == 42
    assert empty_list.tail.val == 42


# --- BOUNDS & EXCEPTION EDGE CASES ---

@pytest.mark.parametrize("invalid_index", [-1, 3, 10])
def test_get_out_of_bounds(filled_list, invalid_index):
    with pytest.raises(IndexError, match="Index out of bounds"):
        filled_list.get(invalid_index)


@pytest.mark.parametrize("invalid_index", [-1, 4, 10])
def test_insert_out_of_bounds(filled_list, invalid_index):
    with pytest.raises(IndexError, match="Index out of bounds"):
        filled_list.insert(invalid_index, 99)


@pytest.mark.parametrize("invalid_index", [-1, 3, 10])
def test_remove_out_of_bounds(filled_list, invalid_index):
    with pytest.raises(IndexError, match="Index out of bounds"):
        filled_list.remove(invalid_index)


# --- ADDITIONAL EDGE CASES & ERROR HANDLING ---

def test_remove_from_empty_list(empty_list):
    """Test removing from an empty list raises IndexError."""
    with pytest.raises(IndexError, match="Index out of bounds"):
        empty_list.remove(0)


def test_remove_single_element_resets_tail(empty_list):
    """Test that removing the only element resets both head and tail to None."""
    empty_list.append(42)
    removed = empty_list.remove(0)
    assert removed == 42
    assert empty_list.getSize() == 0
    assert empty_list.head is None
    assert empty_list.tail is None


def test_insert_into_empty_list_sets_head_and_tail(empty_list):
    """Test inserting at index 0 on empty list updates head and tail."""
    empty_list.insert(0, 99)
    assert empty_list.getSize() == 1
    assert empty_list.head.val == 99
    assert empty_list.tail.val == 99