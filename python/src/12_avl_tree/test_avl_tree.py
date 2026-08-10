import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import time
import random
import pytest
from avl_tree import AVLTree, AVLNode

if __name__ == "__main__":
    # Runs pytest with -s to display execution times live in terminal
    pytest.main(["-s", "-v", __file__])


# --- FIXTURES & HELPER FUNCTIONS ---

@pytest.fixture
def empty_avl():
    """Returns a freshly initialized empty AVL tree."""
    return AVLTree()


def verify_avl_invariant(tree: AVLTree, node: AVLNode | None) -> bool:
    """Helper method to recursively assert that ALL nodes satisfy the AVL Balance Property:
    abs(height(left) - height(right)) <= 1
    """
    if node is None:
        return True

    balance = tree.get_balance(node)
    if abs(balance) > 1:
        return False

    return verify_avl_invariant(tree, node.left) and verify_avl_invariant(tree, node.right)


# --- 1. EXPLICIT ROTATION CASES (LL, RR, LR, RL) ---

def test_left_left_case_right_rotation(empty_avl):
    """LL Case: Inserting 30 -> 20 -> 10 triggers a single Right Rotation.
    
    Before:        30
                  /
                20
               /
             10
             
    After:      20
               /  \
             10    30
    """
    for val in [30, 20, 10]:
        empty_avl.insert(val)

    assert empty_avl.root.val == 20
    assert empty_avl.root.left.val == 10
    assert empty_avl.root.right.val == 30
    assert verify_avl_invariant(empty_avl, empty_avl.root)


def test_right_right_case_left_rotation(empty_avl):
    """RR Case: Inserting 10 -> 20 -> 30 triggers a single Left Rotation.
    
    Before:     10
                  \
                   20
                     \
                      30
                      
    After:      20
               /  \
             10    30
    """
    for val in [10, 20, 30]:
        empty_avl.insert(val)

    assert empty_avl.root.val == 20
    assert empty_avl.root.left.val == 10
    assert empty_avl.root.right.val == 30
    assert verify_avl_invariant(empty_avl, empty_avl.root)


def test_left_right_case_double_rotation(empty_avl):
    """LR Case: Inserting 30 -> 10 -> 20 triggers a Left Rotation on 10, then Right Rotation on 30.
    
    Before:        30
                  /
                10
                  \
                   20
                   
    After:      20
               /  \
             10    30
    """
    for val in [30, 10, 20]:
        empty_avl.insert(val)

    assert empty_avl.root.val == 20
    assert empty_avl.root.left.val == 10
    assert empty_avl.root.right.val == 30
    assert verify_avl_invariant(empty_avl, empty_avl.root)


def test_right_left_case_double_rotation(empty_avl):
    """RL Case: Inserting 10 -> 30 -> 20 triggers a Right Rotation on 30, then Left Rotation on 10.
    
    Before:     10
                  \
                   30
                  /
                20
                
    After:      20
               /  \
             10    30
    """
    for val in [10, 30, 20]:
        empty_avl.insert(val)

    assert empty_avl.root.val == 20
    assert empty_avl.root.left.val == 10
    assert empty_avl.root.right.val == 30
    assert verify_avl_invariant(empty_avl, empty_avl.root)


# --- 2. MULTIPLE SEQUENTIAL ROTATIONS & COMPLEX BALANCING ---

def test_multiple_cascading_rotations(empty_avl):
    """Inserts a larger sequence requiring multiple rotations across different levels."""
    elements = [10, 20, 30, 40, 50, 25]
    for val in elements:
        empty_avl.insert(val)

    # In-Order must remain strictly sorted
    assert empty_avl.inorder_traversal() == [10, 20, 25, 30, 40, 50]

    # Tree height must be optimal O(log n) -> 6 elements should fit in height 3
    assert empty_avl.get_height(empty_avl.root) <= 3
    assert verify_avl_invariant(empty_avl, empty_avl.root)


# --- 3. SEARCH & EDGE CASES ---

def test_search_functionality(empty_avl):
    """Verifies existing vs non-existing searches."""
    for val in [15, 10, 20, 8, 12, 17, 25]:
        empty_avl.insert(val)

    assert empty_avl.search(15) is True
    assert empty_avl.search(8) is True
    assert empty_avl.search(25) is True

    assert empty_avl.search(99) is False
    assert empty_avl.search(-1) is False


def test_empty_and_single_node_tree(empty_avl):
    """Edge cases: operations on empty tree or single-node tree."""
    assert empty_avl.search(10) is False
    assert empty_avl.inorder_traversal() == []

    empty_avl.insert(42)
    assert empty_avl.search(42) is True
    assert empty_avl.inorder_traversal() == [42]
    assert empty_avl.get_height(empty_avl.root) == 1


def test_duplicate_insertions_ignored(empty_avl):
    """Verifies duplicate values are ignored without breaking height calculation."""
    for val in [10, 10, 5, 5, 15, 15]:
        empty_avl.insert(val)

    traversal = empty_avl.inorder_traversal()
    assert traversal == [5, 10, 15]
    assert verify_avl_invariant(empty_avl, empty_avl.root)

def test_negative_numbers_and_zero(empty_avl):
    """Verifies tree balances correctly with negative values."""
    for val in [0, -10, -20, -30, 10]:
        empty_avl.insert(val)

    assert empty_avl.inorder_traversal() == [-30, -20, -10, 0, 10]
    assert verify_avl_invariant(empty_avl, empty_avl.root)


# --- 4. STRESS TEST & BENCHMARK WITH EXECUTION TIMES ---

def test_large_dataset_stress_and_benchmark():
    """Stress test: Inserts 1,000 strictly ascending numbers.
    A standard BST would degenerate into height 1,000 (Linked List).
    AVL Tree must maintain height <= 11!
    """
    avl = AVLTree()
    n = 1000
    data = list(range(1, n + 1))  # Worst-case input for standard BST

    start_time = time.perf_counter()
    for val in data:
        avl.insert(val)
    elapsed_time_ms = (time.perf_counter() - start_time) * 1000

    print(f"\n\n{'='*60}")
    print(f"  AVL TREE STRESS TEST ({n} Sequential Elements)")
    print(f"{'='*60}")
    print(f"Total Insertion Time  : {elapsed_time_ms:.3f} ms")
    print(f"Resulting Tree Height : {avl.get_height(avl.root)} (Max theoretical O(log n): 11)")
    print(f"AVL Invariant Intact  : {verify_avl_invariant(avl, avl.root)}")
    print(f"{'='*60}\n")

    # Height of 1,000 elements in balanced binary tree is ceil(log2(1000)) = 10 (or 11)
    assert avl.get_height(avl.root) <= 11
    assert verify_avl_invariant(avl, avl.root)
    assert avl.inorder_traversal() == data



def test_all_four_rotations_in_single_tree(empty_avl):
    """Executes a carefully chosen sequence of insertions that forces ALL 4 rotation 
    types (LL, RR, LR, RL) to trigger sequentially in a single tree session.
    """
    # 1. Triggers RR (Left Rotation) -> Root becomes 20
    empty_avl.insert(10)
    empty_avl.insert(20)
    empty_avl.insert(30)
    assert empty_avl.root.val == 20

    # 2. Triggers LL (Right Rotation) on left branch
    empty_avl.insert(5)
    empty_avl.insert(2)
    assert empty_avl.get_balance(empty_avl.root) <= 1

    # 3. Triggers LR (Left-Right Rotation)
    empty_avl.insert(4)

    # 4. Triggers RL (Right-Left Rotation)
    empty_avl.insert(25)

    # Verify that tree invariants hold and sorted order is strictly preserved
    assert empty_avl.inorder_traversal() == [2, 4, 5, 10, 20, 25, 30]
    assert verify_avl_invariant(empty_avl, empty_avl.root)


def test_height_difference_never_exceeds_one(empty_avl):
    """Inserts numbers in reverse-sorted order to verify continuous balancing.
    Inserting 100 down to 10 forces a Right Rotation (LL-Case) at almost every step!
    """
    decreasing_data = list(range(100, 0, -10))  # [100, 90, 80, ..., 10]
    
    for val in decreasing_data:
        empty_avl.insert(val)
        # Check balance condition after EVERY SINGLE insertion!
        assert verify_avl_invariant(empty_avl, empty_avl.root)

    assert empty_avl.inorder_traversal() == sorted(decreasing_data)