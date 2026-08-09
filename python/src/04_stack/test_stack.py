import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pytest
from stack import Stack

if __name__ == "__main__":
    pytest.main([__file__])


# --- FIXTURES ---

@pytest.fixture
def empty_stack():
    return Stack()


@pytest.fixture
def filled_stack():
    s = Stack()
    s.push(10)
    s.push(20)
    s.push(30)
    return s  # Top is 30 -> 20 -> 10


# --- INITIALIZATION & BASIC STATE TESTS ---

def test_initialization(empty_stack):
    assert empty_stack.getSize() == 0
    assert empty_stack.is_empty() is True
    assert empty_stack.top is None


# --- PUSH & LIFO BEHAVIOR TESTS ---

def test_push_single_element(empty_stack):
    empty_stack.push(10)
    assert empty_stack.getSize() == 1
    assert empty_stack.is_empty() is False
    assert empty_stack.peek() == 10
    assert empty_stack.top.val == 10


def test_push_multiple_elements(empty_stack):
    empty_stack.push(1)
    empty_stack.push(2)
    empty_stack.push(3)
    assert empty_stack.getSize() == 3
    assert empty_stack.peek() == 3


def test_lifo_order_strict(empty_stack):
    elements = [100, 200, 300, 400]
    for el in elements:
        empty_stack.push(el)

    for el in reversed(elements):
        assert empty_stack.pop() == el


# --- POP & PEEK ADVANCED TESTS ---

def test_pop_until_empty(filled_stack):
    assert filled_stack.pop() == 30
    assert filled_stack.getSize() == 2
    assert filled_stack.is_empty() is False

    assert filled_stack.pop() == 20
    assert filled_stack.getSize() == 1

    assert filled_stack.pop() == 10
    assert filled_stack.getSize() == 0
    assert filled_stack.is_empty() is True
    assert filled_stack.top is None


def test_peek_idempotence(filled_stack):
    # Multiple calls to peek() should return same value and not modify stack
    assert filled_stack.peek() == 30
    assert filled_stack.peek() == 30
    assert filled_stack.peek() == 30
    assert filled_stack.getSize() == 3


def test_interleaved_push_and_pop(empty_stack):
    empty_stack.push(1)
    empty_stack.push(2)
    assert empty_stack.pop() == 2

    empty_stack.push(3)
    assert empty_stack.peek() == 3
    assert empty_stack.pop() == 3
    assert empty_stack.pop() == 1
    assert empty_stack.is_empty() is True


# --- STRESS & LARGE DATASETS TESTS ---

def test_large_number_of_elements(empty_stack):
    n = 10000
    for i in range(n):
        empty_stack.push(i)

    assert empty_stack.getSize() == n
    assert empty_stack.peek() == n - 1

    for i in range(n - 1, -1, -1):
        assert empty_stack.pop() == i

    assert empty_stack.is_empty() is True


# --- EDGE CASES & EXCEPTIONS ---

def test_pop_on_empty_stack_raises(empty_stack):
    with pytest.raises(IndexError, match="Pop from empty stack"):
        empty_stack.pop()


def test_peek_on_empty_stack_raises(empty_stack):
    with pytest.raises(IndexError, match="Peek from empty stack"):
        empty_stack.peek()


def test_pop_underflow_after_emptying(filled_stack):
    filled_stack.pop()
    filled_stack.pop()
    filled_stack.pop()
    assert filled_stack.is_empty() is True

    with pytest.raises(IndexError, match="Pop from empty stack"):
        filled_stack.pop()


def test_push_duplicates_and_negative_numbers(empty_stack):
    empty_stack.push(-5)
    empty_stack.push(0)
    empty_stack.push(-5)
    
    assert empty_stack.getSize() == 3
    assert empty_stack.pop() == -5
    assert empty_stack.pop() == 0
    assert empty_stack.pop() == -5