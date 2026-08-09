import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pytest
from queue import Queue

if __name__ == "__main__":
    pytest.main([__file__])


# --- FIXTURES ---

@pytest.fixture
def empty_queue():
    return Queue()


@pytest.fixture
def filled_queue():
    q = Queue()
    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)
    return q  # Head: 10, Tail: 30


# --- INITIALIZATION & BASIC STATE TESTS ---

def test_initialization(empty_queue):
    assert empty_queue.getSize() == 0
    assert empty_queue.is_empty() is True
    assert empty_queue.head is None
    assert empty_queue.tail is None


# --- ENQUEUE & POINTER INTEGRITY TESTS ---

def test_enqueue_single_element(empty_queue):
    empty_queue.enqueue(10)
    assert empty_queue.getSize() == 1
    assert empty_queue.is_empty() is False
    assert empty_queue.peek() == 10
    assert empty_queue.head.val == 10
    assert empty_queue.tail.val == 10


def test_enqueue_multiple_elements_pointers(empty_queue):
    empty_queue.enqueue(10)
    empty_queue.enqueue(20)
    empty_queue.enqueue(30)

    assert empty_queue.getSize() == 3
    assert empty_queue.head.val == 10
    assert empty_queue.head.next.val == 20
    assert empty_queue.head.next.next.val == 30
    assert empty_queue.tail.val == 30
    assert empty_queue.tail.next is None


# --- DEQUEUE & FIFO BEHAVIOR TESTS ---

def test_fifo_order_strict(empty_queue):
    elements = [100, 200, 300, 400, 500]
    for el in elements:
        empty_queue.enqueue(el)

    for el in elements:
        assert empty_queue.dequeue() == el


def test_dequeue_pointer_updates(filled_queue):
    # Head is initially 10
    assert filled_queue.dequeue() == 10
    assert filled_queue.head.val == 20
    assert filled_queue.getSize() == 2

    assert filled_queue.dequeue() == 20
    assert filled_queue.head.val == 30
    assert filled_queue.tail.val == 30
    assert filled_queue.getSize() == 1

    assert filled_queue.dequeue() == 30
    assert filled_queue.getSize() == 0
    assert filled_queue.head is None
    assert filled_queue.tail is None


def test_peek_idempotence(filled_queue):
    # Multiple calls to peek() should return same value and not modify queue
    assert filled_queue.peek() == 10
    assert filled_queue.peek() == 10
    assert filled_queue.peek() == 10
    assert filled_queue.getSize() == 3


def test_interleaved_enqueue_and_dequeue(empty_queue):
    empty_queue.enqueue(1)
    empty_queue.enqueue(2)
    assert empty_queue.dequeue() == 1

    empty_queue.enqueue(3)
    assert empty_queue.dequeue() == 2
    assert empty_queue.peek() == 3

    empty_queue.enqueue(4)
    assert empty_queue.dequeue() == 3
    assert empty_queue.dequeue() == 4
    assert empty_queue.is_empty() is True
    assert empty_queue.head is None
    assert empty_queue.tail is None


# --- STRESS & LARGE DATASETS TESTS ---

def test_large_number_of_elements(empty_queue):
    n = 10000
    for i in range(n):
        empty_queue.enqueue(i)

    assert empty_queue.getSize() == n
    assert empty_queue.peek() == 0

    for i in range(n):
        assert empty_queue.dequeue() == i

    assert empty_queue.is_empty() is True
    assert empty_queue.head is None
    assert empty_queue.tail is None


# --- EDGE CASES & EXCEPTIONS ---

def test_dequeue_on_empty_queue_raises(empty_queue):
    with pytest.raises(IndexError, match="Dequeue from empty queue"):
        empty_queue.dequeue()


def test_peek_on_empty_queue_raises(empty_queue):
    with pytest.raises(IndexError, match="Peek from empty queue"):
        empty_queue.peek()


def test_dequeue_underflow_after_emptying(filled_queue):
    filled_queue.dequeue()
    filled_queue.dequeue()
    filled_queue.dequeue()
    assert filled_queue.is_empty() is True

    with pytest.raises(IndexError, match="Dequeue from empty queue"):
        filled_queue.dequeue()


def test_enqueue_negative_numbers_and_duplicates(empty_queue):
    empty_queue.enqueue(-10)
    empty_queue.enqueue(0)
    empty_queue.enqueue(-10)

    assert empty_queue.getSize() == 3
    assert empty_queue.dequeue() == -10
    assert empty_queue.dequeue() == 0
    assert empty_queue.dequeue() == -10