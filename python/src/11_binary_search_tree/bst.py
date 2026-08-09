class TreeNode:
    """A node inside a Binary Search Tree (BST).
    
    Each node holds a payload value and references to at most TWO child nodes:
    `left` (for values strictly smaller) and `right` (for values strictly larger).
    """
    def __init__(self, val: int):
        self.val = val
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None


class BinarySearchTree:
    """A Binary Search Tree (BST) supporting Recursive & Iterative operations.

    ===========================================================================
    WHAT IS A BINARY SEARCH TREE?
    ===========================================================================
    A node-based binary tree data structure with the BST Property:
      1. Left subtree of a node contains ONLY keys SMALLER than the node's key.
      2. Right subtree of a node contains ONLY keys LARGER than the node's key.
      3. Left and right subtrees must also be binary search trees.

    ===========================================================================
    VISUAL REPRESENTATION
    ===========================================================================
             10            <-- Root Node
            /  \
           5    15         <-- Left < Root (5 < 10) | Right > Root (15 > 10)
          / \     \
         2   7     20      <-- At most TWO children per node!

    ===========================================================================
    TIME & SPACE COMPLEXITY CHEATSHEET
    ===========================================================================
    Operation   | Average Case  | Worst Case (Degenerate/Skewed Tree)
    -----------------------------------------------------------------
    Search      | O(log n)      | O(n) -> Behaves like a Linked List!
    Insert      | O(log n)      | O(n) -> Solved by Self-Balancing (AVL / Red-Black)
    Traversals  | O(n)          | O(n) -> Visits every node exactly once
    
    Space Complexity:
    - Iterative operations: O(1) auxiliary space (no stack allocations)
    - Recursive operations: O(h) call stack memory (where h = tree height)
    ===========================================================================
    THE 3 TRAVERSAL STRATEGIES
    ===========================================================================
    1. In-Order   (Left -> Root -> Right): ALWAYS yields values in ASCENDING order.
    2. Pre-Order  (Root -> Left -> Right): Preserves tree shape (Great for copying).
    3. Post-Order (Left -> Right -> Root): Children before parent (Great for cleanup).
    ===========================================================================
    """

    def __init__(self):
        self.root: TreeNode | None = None

    # =========================================================================
    # INSERTION (3 VARIANTS)
    # =========================================================================

    # --- Variant 1: Iterative (while loop, O(1) Memory, NO Recursion) ---
    def insert_iterative(self, val: int) -> None:
        """Iterative insertion using a while loop."""
        new_node = TreeNode(val)

        if self.root is None:
            self.root = new_node
            return

        curr = self.root
        while True:
            if val < curr.val:
                if curr.left is None:
                    curr.left = new_node
                    break
                curr = curr.left
            elif val > curr.val:
                if curr.right is None:
                    curr.right = new_node
                    break
                curr = curr.right
            else:
                break  # Ignore duplicates

    # --- Variant 2: Recursive WITH Helper Function (Classic Textbook Approach) ---
    def insert_with_helper(self, val: int) -> None:
        """Recursive insertion using a separate internal helper method."""
        if self.root is None:
            self.root = TreeNode(val)
        else:
            self._insert_recursive(self.root, val)

    def _insert_recursive(self, node: TreeNode, val: int) -> TreeNode:
        """Internal helper method for recursive insertion."""
        if val < node.val:
            if node.left is None:
                node.left = TreeNode(val)
            else:
                self._insert_recursive(node.left, val)
        elif val > node.val:
            if node.right is None:
                node.right = TreeNode(val)
            else:
                self._insert_recursive(node.right, val)

        return node

    # --- Variant 3: Recursive WITHOUT Helper Function ---
    def insert_no_helper(self, val: int, node: TreeNode | None = None) -> TreeNode:
        """Recursive insertion directly on the main method using default parameter."""
        if self.root is None:
            self.root = TreeNode(val)
            return self.root

        if node is None:
            node = self.root

        if val < node.val:
            if node.left is None:
                node.left = TreeNode(val)
            else:
                self.insert_no_helper(val, node.left)
        elif val > node.val:
            if node.right is None:
                node.right = TreeNode(val)
            else:
                self.insert_no_helper(val, node.right)

        return node

    # =========================================================================
    # SEARCH (3 VARIANTS)
    # =========================================================================

    # --- Variant 1: Iterative (while loop, O(1) Memory, NO Recursion) ---
    def search_iterative(self, val: int) -> bool:
        """Iterative search using a while loop."""
        curr = self.root
        while curr is not None:
            if curr.val == val:
                return True
            elif val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        return False

    # --- Variant 2: Recursive WITH Helper Function  ---
    def search_with_helper(self, val: int) -> bool:
        """Recursive search using a separate internal helper method."""
        return self._search_recursive(self.root, val)

    def _search_recursive(self, node: TreeNode | None, val: int) -> bool:
        """Internal helper method for recursive search."""
        if node is None:
            return False
        if node.val == val:
            return True

        if val < node.val:
            return self._search_recursive(node.left, val)
        else:
            return self._search_recursive(node.right, val)

    # --- Variant 3: Recursive WITHOUT Helper Function ---
    def search_no_helper(self, val: int, node: TreeNode | None = None, is_initial_call: bool = True) -> bool:
        """Recursive search directly on the main method using default parameters.
        
        Good to Know: 'is_initial_call' ensures we correctly distinguish between 
        searching for 'node is None' at root level vs. reaching a leaf node!
        """
        if is_initial_call:
            if self.root is None:
                return False
            node = self.root

        if node is None:
            return False
        if node.val == val:
            return True

        if val < node.val:
            return self.search_no_helper(val, node.left, is_initial_call=False)
        else:
            return self.search_no_helper(val, node.right, is_initial_call=False)

    # =========================================================================
    # TRAVERSALS (In-Order, Pre-Order, Post-Order)
    # =========================================================================
    def inorder_traversal(self) -> list[int]:
        """In-Order Traversal (Left -> Root -> Right)."""
        result: list[int] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: TreeNode | None, result: list[int]) -> None:
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)

    def preorder_traversal(self) -> list[int]:
        """Pre-Order Traversal (Root -> Left -> Right)."""
        result: list[int] = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node: TreeNode | None, result: list[int]) -> None:
        if node is not None:
            result.append(node.val)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder_traversal(self) -> list[int]:
        """Post-Order Traversal (Left -> Right -> Root)."""
        result: list[int] = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node: TreeNode | None, result: list[int]) -> None:
        if node is not None:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.val)