import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import time
import random
import pytest
from rbnode import RedBlackTree, RBNode, Color

if __name__ == "__main__":
    # Runs pytest with -s to show live output and execution times in the terminal
    pytest.main(["-s", "-v", __file__])


# --- FIXTURES & RULE-VERIFICATION HELPERS ---

@pytest.fixture
def empty_rbt():
    """Returns a freshly initialized empty Red-Black Tree."""
    return RedBlackTree()


def verify_rule1_node_colors(node: RBNode | None) -> bool:
    """Rule 1: Every node is either RED or BLACK."""
    if node is None:
        return True
    if node.color not in (Color.RED, Color.BLACK):
        return False
    return verify_rule1_node_colors(node.left) and verify_rule1_node_colors(node.right)


def verify_rule2_root_is_black(tree: RedBlackTree) -> bool:
    """Rule 2: The root node is always BLACK."""
    if tree.root is None:
        return True
    return tree.root.color == Color.BLACK


def verify_rule4_no_red_red_conflicts(node: RBNode | None) -> bool:
    """Rule 4: RED Property - If a node is RED, both of its children must be BLACK."""
    if node is None:
        return True

    if node.color == Color.RED:
        left_color = node.left.color if node.left else Color.BLACK
        right_color = node.right.color if node.right else Color.BLACK

        if left_color == Color.RED or right_color == Color.RED:
            return False

    return verify_rule4_no_red_red_conflicts(node.left) and verify_rule4_no_red_red_conflicts(node.right)


def get_black_height(node: RBNode | None) -> int:
    """Helper to calculate and verify Rule 5: Black Height Property."""
    if node is None:
        # Rule 3: NIL leaves are treated as BLACK, contributing 1 to black height
        return 1

    left_black_height = get_black_height(node.left)
    right_black_height = get_black_height(node.right)

    # If any subtree downstream violated the rule, propagate -1 error
    if left_black_height == -1 or right_black_height == -1:
        return -1

    # Every path down must have the exact same number of black nodes
    if left_black_height != right_black_height:
        return -1

    # Add 1 if the current node itself is BLACK
    current_count = 1 if node.color == Color.BLACK else 0
    return left_black_height + current_count


def verify_all_5_rb_rules(tree: RedBlackTree) -> bool:
    """Comprehensive check that verifies all 5 Red-Black invariants on the tree."""
    if tree.root is None:
        return True

    # Rule 1: Colors are RED or BLACK
    if not verify_rule1_node_colors(tree.root):
        return False

    # Rule 2: Root is BLACK
    if not verify_rule2_root_is_black(tree):
        return False

    # Rule 3 & 5: Equal Black Height across all paths
    if get_black_height(tree.root) == -1:
        return False

    # Rule 4: No RED-RED parent-child relationships
    if not verify_rule4_no_red_red_conflicts(tree.root):
        return False

    return True


# --- 1. TESTS FOR ALL 5 RED-BLACK TREE RULES ---

def test_rule1_and_rule2_root_always_black(empty_rbt):
    """Verifies that inserting elements always maintains a BLACK root and valid node colors."""
    elements = [10, 20, 30, 15, 25]
    for val in elements:
        empty_rbt.insert(val)
        assert empty_rbt.root.color == Color.BLACK
        assert verify_rule1_node_colors(empty_rbt.root)


def test_rule3_nil_leaves_are_black(empty_rbt):
    """Verifies that None / NIL leaves act as BLACK nodes in black height calculation."""
    empty_rbt.insert(42)
    # Single node tree: Root is BLACK, children are None (treated as BLACK)
    assert get_black_height(empty_rbt.root) == 2  # Root (1) + NIL leaf (1)


def test_rule4_no_red_red_conflict_after_rotations(empty_rbt):
    """Inserting sequential numbers (1, 2, 3, 4, 5, 6) triggers recoloring and rotations.
    Tests that NO RED node ever has a RED child.
    """
    for val in range(1, 7):
        empty_rbt.insert(val)
        assert verify_rule4_no_red_red_conflicts(empty_rbt.root)


def test_rule5_black_height_property(empty_rbt):
    """Verifies that every path from root to NIL leaves has the exact same black node count."""
    elements = [41, 38, 31, 12, 19, 8, 20]
    for val in elements:
        empty_rbt.insert(val)

    # get_black_height returns -1 if paths have unequal black node counts
    black_height = get_black_height(empty_rbt.root)
    assert black_height > 0
    assert verify_all_5_rb_rules(empty_rbt)


# --- 2. SEARCH & TRAVERSAL TESTS ---

def test_search_and_inorder_sorting(empty_rbt):
    """Verifies searching existing/missing elements and sorted In-Order output."""
    data = [50, 30, 70, 20, 40, 60, 80]
    for val in data:
        empty_rbt.insert(val)

    # In-Order traversal MUST be strictly ascending
    assert empty_rbt.inorder_traversal() == sorted(data)

    # Search existing
    assert empty_rbt.search(50) is True
    assert empty_rbt.search(20) is True
    assert empty_rbt.search(80) is True

    # Search missing
    assert empty_rbt.search(99) is False
    assert empty_rbt.search(-5) is False


def test_edge_cases_empty_single_and_duplicates(empty_rbt):
    """Tests empty tree operations, single insertions, and duplicate handling."""
    # Empty tree
    assert empty_rbt.search(10) is False
    assert empty_rbt.inorder_traversal() == []

    # Duplicates should be safely ignored
    for val in [10, 10, 5, 5, 20, 20]:
        empty_rbt.insert(val)

    assert empty_rbt.inorder_traversal() == [5, 10, 20]
    assert verify_all_5_rb_rules(empty_rbt)


# --- 3. STRESS TEST & BENCHMARK WITH EXECUTION TIME ---

def test_large_dataset_stress_benchmark():
    """Stress Test: Inserts 1,000 sequential numbers (worst-case for standard BST).
    Red-Black Tree must maintain balance and pass all 5 rules effortlessly.
    """
    rbt = RedBlackTree()
    n = 1000
    sequential_data = list(range(1, n + 1))

    start_time = time.perf_counter()
    for val in sequential_data:
        rbt.insert(val)
    elapsed_time_ms = (time.perf_counter() - start_time) * 1000

    print(f"\n\n{'='*60}")
    print(f"  RED-BLACK TREE STRESS TEST ({n} Sequential Elements)")
    print(f"{'='*60}")
    print(f"Total Insertion Time  : {elapsed_time_ms:.3f} ms")
    print(f"All 5 RB Rules Valid : {verify_all_5_rb_rules(rbt)}")
    print(f"Computed Black Height : {get_black_height(rbt.root)}")
    print(f"{'='*60}\n")

    assert verify_all_5_rb_rules(rbt) is True
    assert rbt.inorder_traversal() == sequential_data