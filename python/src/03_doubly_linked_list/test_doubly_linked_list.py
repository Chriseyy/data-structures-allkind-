import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pytest
from doubly_linked_list import DoublyLinkedList

if __name__ == "__main__":
    pytest.main([__file__])


# --- FIXTURES ---

@pytest.fixture
def empty_list():
    return DoublyLinkedList()


@pytest.fixture
def filled_list():
    dll = DoublyLinkedList()
    dll.append(10)
    dll.append(20)
    dll.append(30)
    return dll  # [10, 20, 30]


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
    assert empty_list.head.prev is None
    assert empty_list.head.next is None

    empty_list.prepend(10)
    assert empty_list.getSize() == 2
    assert empty_list.head.val == 10
    assert empty_list.tail.val == 20
    assert empty_list.head.next.val == 20
    assert empty_list.tail.prev.val == 10


def test_append(empty_list):
    empty_list.append(10)
    assert empty_list.getSize() == 1
    assert empty_list.head.val == 10
    assert empty_list.tail.val == 10

    empty_list.append(20)
    assert empty_list.getSize() == 2
    assert empty_list.head.val == 10
    assert empty_list.tail.val == 20
    assert empty_list.tail.prev.val == 10
    assert empty_list.head.next.val == 20


# --- GET METHOD OPTIMIZATION TESTS (FORWARD & BACKWARD TRAVERSAL) ---

def test_get_forward_and_backward_traversal(empty_list):
    # Construct longer list: [0, 10, 20, 30, 40, 50]
    for i in range(6):
        empty_list.append(i * 10)

    # Test indices close to head (forward search)
    assert empty_list.get(0) == 0
    assert empty_list.get(1) == 10
    assert empty_list.get(2) == 20

    # Test indices close to tail (backward search)
    assert empty_list.get(3) == 30
    assert empty_list.get(4) == 40
    assert empty_list.get(5) == 50


# --- INSERTION TESTS & POINTER INTEGRITY ---

@pytest.mark.parametrize("index, val, expected", [
    (0, 5, [5, 10, 20, 30]),      # Head
    (1, 15, [10, 15, 20, 30]),    # Middle
    (2, 25, [10, 20, 25, 30]),    # Middle
    (3, 40, [10, 20, 30, 40]),    # Tail
])
def test_insert_positions(filled_list, index, val, expected):
    filled_list.insert(index, val)
    assert filled_list.getSize() == len(expected)
    for i, exp in enumerate(expected):
        assert filled_list.get(i) == exp


def test_insert_pointer_integrity(filled_list):
    filled_list.insert(1, 15)  # [10, 15, 20, 30]
    
    # Forward check
    assert filled_list.head.val == 10
    assert filled_list.head.next.val == 15
    assert filled_list.head.next.next.val == 20
    assert filled_list.head.next.next.next.val == 30

    # Backward check
    assert filled_list.tail.val == 30
    assert filled_list.tail.prev.val == 20
    assert filled_list.tail.prev.prev.val == 15
    assert filled_list.tail.prev.prev.prev.val == 10


# --- REMOVAL TESTS & CORNER CASES ---

@pytest.mark.parametrize("remove_index, expected_removed, expected_remaining", [
    (0, 10, [20, 30]),  # Remove Head
    (1, 20, [10, 30]),  # Remove Middle
    (2, 30, [10, 20]),  # Remove Tail
])
def test_remove_positions(filled_list, remove_index, expected_removed, expected_remaining):
    removed = filled_list.remove(remove_index)
    assert removed == expected_removed
    assert filled_list.getSize() == len(expected_remaining)
    for i, exp in enumerate(expected_remaining):
        assert filled_list.get(i) == exp


def test_remove_until_empty(empty_list):
    empty_list.append(99)
    val = empty_list.remove(0)
    assert val == 99
    assert empty_list.getSize() == 0
    assert empty_list.head is None
    assert empty_list.tail is None


def test_remove_pointer_integrity(filled_list):
    filled_list.remove(1)  # Remove 20 -> [10, 30]
    assert filled_list.head.next.val == 30
    assert filled_list.tail.prev.val == 10
    assert filled_list.head.next.prev.val == 10
    assert filled_list.tail.prev.next.val == 30


# --- REVERSE TESTS ---

def test_reverse_filled_list(filled_list):
    filled_list.reverse()  # [30, 20, 10]
    assert filled_list.get(0) == 30
    assert filled_list.get(1) == 20
    assert filled_list.get(2) == 10

    # Verify head/tail and internal prev/next pointers after reverse
    assert filled_list.head.val == 30
    assert filled_list.tail.val == 10
    assert filled_list.head.prev is None
    assert filled_list.tail.next is None
    assert filled_list.head.next.val == 20
    assert filled_list.head.next.prev.val == 30


def test_reverse_empty_and_single_element_list(empty_list):
    # Empty
    empty_list.reverse()
    assert empty_list.head is None
    assert empty_list.tail is None

    # Single element
    empty_list.append(42)
    empty_list.reverse()
    assert empty_list.head.val == 42
    assert empty_list.tail.val == 42
    assert empty_list.head.prev is None
    assert empty_list.tail.next is None


# --- BOUNDS & EXCEPTION TESTS ---

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


def test_remove_empty_list(empty_list):
    with pytest.raises(IndexError, match="Index out of bounds"):
        empty_list.remove(0)