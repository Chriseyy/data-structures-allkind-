import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import time
import random
import pytest
from bst import BinarySearchTree

if __name__ == "__main__":
    # Runs pytest with -s to show execution time benchmarks live in terminal
    pytest.main(["-s", "-v", __file__])


# --- FIXTURES ---

@pytest.fixture
def empty_tree():
    """Returns an empty Binary Search Tree."""
    return BinarySearchTree()


@pytest.fixture
def filled_tree_iterative():
    """Tree constructed strictly via insert_iterative."""
    tree = BinarySearchTree()
    for val in [10, 5, 15, 2, 7, 20]:
        tree.insert_iterative(val)
    return tree


@pytest.fixture
def filled_tree_with_helper():
    """Tree constructed strictly via insert_with_helper."""
    tree = BinarySearchTree()
    for val in [10, 5, 15, 2, 7, 20]:
        tree.insert_with_helper(val)
    return tree


@pytest.fixture
def filled_tree_no_helper():
    """Tree constructed strictly via insert_no_helper."""
    tree = BinarySearchTree()
    for val in [10, 5, 15, 2, 7, 20]:
        tree.insert_no_helper(val)
    return tree


# --- 1. ALL INSERTION VARIANTS & PARITY TESTS ---

def test_insertion_variants_parity(empty_tree):
    """Tests that all 3 insertion strategies build structurally equivalent trees."""
    elements = [50, 30, 70, 20, 40, 60, 80]

    t_iter = BinarySearchTree()
    t_help = BinarySearchTree()
    t_no_h = BinarySearchTree()

    for el in elements:
        t_iter.insert_iterative(el)
        t_help.insert_with_helper(el)
        t_no_h.insert_no_helper(el)

    expected_sorted = [20, 30, 40, 50, 60, 70, 80]
    expected_preorder = [50, 30, 20, 40, 70, 60, 80]

    # Verify In-Order (Values)
    assert t_iter.inorder_traversal() == expected_sorted
    assert t_help.inorder_traversal() == expected_sorted
    assert t_no_h.inorder_traversal() == expected_sorted

    # Verify Pre-Order (Structural Topology)
    assert t_iter.preorder_traversal() == expected_preorder
    assert t_help.preorder_traversal() == expected_preorder
    assert t_no_h.preorder_traversal() == expected_preorder


# --- 2. ALL SEARCH VARIANTS TESTS ---

@pytest.mark.parametrize("search_method", [
    "search_iterative",
    "search_with_helper",
    "search_no_helper"
])
def test_all_search_methods_existing(filled_tree_iterative, search_method):
    """Verifies that all 3 search implementations correctly find existing values."""
    search_fn = getattr(filled_tree_iterative, search_method)

    assert search_fn(10) is True  # Root node
    assert search_fn(5) is True   # Left child
    assert search_fn(15) is True  # Right child
    assert search_fn(2) is True   # Leaf node
    assert search_fn(20) is True  # Leaf node


@pytest.mark.parametrize("search_method", [
    "search_iterative",
    "search_with_helper",
    "search_no_helper"
])
def test_all_search_methods_missing(filled_tree_iterative, search_method):
    """Verifies that all 3 search implementations return False for missing values."""
    search_fn = getattr(filled_tree_iterative, search_method)

    assert search_fn(99) is False
    assert search_fn(-10) is False
    assert search_fn(8) is False


@pytest.mark.parametrize("search_method", [
    "search_iterative",
    "search_with_helper",
    "search_no_helper"
])
def test_search_on_empty_tree(empty_tree, search_method):
    """Verifies searching on an empty tree returns False for all search methods."""
    search_fn = getattr(empty_tree, search_method)
    assert search_fn(10) is False


# --- 3. TRAVERSAL TESTS (In-Order, Pre-Order, Post-Order) ---

def test_traversals_balanced_tree(filled_tree_iterative):
    """Verifies all 3 tree traversal strategies on a balanced tree."""
    # In-Order: Left -> Root -> Right (MUST BE STRICTLY ASCENDING)
    assert filled_tree_iterative.inorder_traversal() == [2, 5, 7, 10, 15, 20]

    # Pre-Order: Root -> Left -> Right
    assert filled_tree_iterative.preorder_traversal() == [10, 5, 2, 7, 15, 20]

    # Post-Order: Left -> Right -> Root
    assert filled_tree_iterative.postorder_traversal() == [2, 7, 5, 20, 15, 10]


def test_traversals_empty_tree(empty_tree):
    """Verifies traversals on empty tree return empty lists."""
    assert empty_tree.inorder_traversal() == []
    assert empty_tree.preorder_traversal() == []
    assert empty_tree.postorder_traversal() == []


def test_traversals_single_node(empty_tree):
    """Verifies traversals on a single-node tree."""
    empty_tree.insert_iterative(100)
    assert empty_tree.inorder_traversal() == [100]
    assert empty_tree.preorder_traversal() == [100]
    assert empty_tree.postorder_traversal() == [100]


# --- 4. SPECIAL & EDGE CASES ---

def test_skewed_tree_linked_list_behavior(empty_tree):
    """Tests edge case where insertion creates a degenerate (skewed) tree."""
    # Insert in strictly increasing order -> Creates right-skewed tree
    elements = [10, 20, 30, 40, 50]
    for val in elements:
        empty_tree.insert_iterative(val)

    assert empty_tree.inorder_traversal() == elements
    assert empty_tree.preorder_traversal() == elements
    assert empty_tree.search_iterative(40) is True


def test_negative_numbers_and_zero(empty_tree):
    """Verifies BST correctness with negative values and zero."""
    elements = [0, -10, 10, -20, -5]
    for val in elements:
        empty_tree.insert_iterative(val)

    assert empty_tree.inorder_traversal() == [-20, -10, -5, 0, 10]
    assert empty_tree.search_iterative(-5) is True
    assert empty_tree.search_with_helper(-15) is False


def test_duplicate_insertions_ignored(empty_tree):
    """Ensures duplicate values are safely ignored and do not corrupt tree."""
    empty_tree.insert_iterative(10)
    empty_tree.insert_iterative(10)
    empty_tree.insert_with_helper(5)
    empty_tree.insert_no_helper(5)

    assert empty_tree.inorder_traversal() == [5, 10]


# --- 5. STRESS & EXECUTION TIME BENCHMARK ---

def test_benchmark_insertion_and_search_performance():
    """Prints execution times for 1,000 random elements across variants."""
    n = 1000
    random.seed(42)
    random_data = list(set([random.randint(-10000, 10000) for _ in range(n)]))

    t_iter = BinarySearchTree()
    t_help = BinarySearchTree()

    # Measure Iterative Insertion
    start = time.perf_counter()
    for val in random_data:
        t_iter.insert_iterative(val)
    time_iter_ins = (time.perf_counter() - start) * 1000

    # Measure Recursive Insertion
    start = time.perf_counter()
    for val in random_data:
        t_help.insert_with_helper(val)
    time_rec_ins = (time.perf_counter() - start) * 1000

    # Measure Search Speeds
    search_target = random_data[len(random_data) // 2]

    start = time.perf_counter()
    res1 = t_iter.search_iterative(search_target)
    time_iter_search = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    res2 = t_iter.search_with_helper(search_target)
    time_rec_search = (time.perf_counter() - start) * 1000

    print(f"\n\n{'='*60}")
    print(f"  BST PERFORMANCE BENCHMARK ({len(random_data)} Elements)")
    print(f"{'='*60}")
    print(f"Iterative Insert Time : {time_iter_ins:.3f} ms")
    print(f"Recursive Insert Time : {time_rec_ins:.3f} ms")
    print(f"Iterative Search Time : {time_iter_search:.3f} ms")
    print(f"Recursive Search Time : {time_rec_search:.3f} ms")
    print(f"{'='*60}\n")

    assert res1 is True and res2 is True
    assert t_iter.inorder_traversal() == sorted(random_data)