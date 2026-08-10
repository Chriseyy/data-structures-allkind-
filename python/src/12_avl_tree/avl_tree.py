class AVLNode:
    """A node inside an AVL Tree storing value, node height, and left/right children."""
    def __init__(self, val: int):
        self.val = val
        self.height: int = 1
        self.left: AVLNode | None = None
        self.right: AVLNode | None = None


class AVLTree:
    """A Self-Balancing Binary Search Tree (AVL Tree) implementation.

    ===========================================================================
    WHAT IS AN AVL TREE?
    ===========================================================================
    An AVL Tree is a self-balancing Binary Search Tree where the heights 
    of the two child subtrees of any node differ by AT MOST one (-1, 0, or 1).

    If at any time they differ by more than one, rebalancing is performed via 
    tree rotations (Left or Right) to guarantee O(log n) worst-case time!

    ===========================================================================
    THE 4 ROTATION CASES
    ===========================================================================
    1. Left-Left (LL) Case   -> Right Rotation
    2. Right-Right (RR) Case -> Left Rotation
    3. Left-Right (LR) Case  -> Left Rotate child, then Right Rotate node
    4. Right-Left (RL) Case  -> Right Rotate child, then Left Rotate node
    ===========================================================================
    """

    def __init__(self):
        self.root: AVLNode | None = None

    # -------------------------------------------------------------------------
    # HELPER METHODS (Height & Balance Factor)
    # -------------------------------------------------------------------------
    def get_height(self, node: AVLNode | None) -> int:
        """Returns the height of a node (0 if None)."""
        if node is None:
            return 0
        return node.height

    def get_balance(self, node: AVLNode | None) -> int:
        """Calculates Balance Factor = height(left) - height(right)."""
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # -------------------------------------------------------------------------
    # ROTATION OPERATIONS
    # -------------------------------------------------------------------------
    def _right_rotate(self, z: AVLNode) -> AVLNode:
        """Performs a Right Rotation around node z.
        
        Visual Transformation:
             z               y
            / \             / \
           y   T4   -->    x   z
          / \                 / \
         x   T3              T3  T4
        """
        y = z.left
        assert y is not None
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update node heights (bottom-up: z first, then y)
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y  # New root of this subtree

    def _left_rotate(self, z: AVLNode) -> AVLNode:
        """Performs a Left Rotation around node z.
        
        Visual Transformation:
             z                   y
            / \                 / \
           T1  y     -->       z   x
              / \             / \
             T2  x           T1  T2
        """
        y = z.right
        assert y is not None
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update node heights (bottom-up: z first, then y)
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y  # New root of this subtree

    # -------------------------------------------------------------------------
    # INSERTION WITH AUTOMATIC REBALANCING
    # -------------------------------------------------------------------------
    def insert(self, val: int) -> None:
        """Inserts a new value and maintains AVL balance property."""
        self.root = self._insert_recursive(self.root, val)

    def _insert_recursive(self, node: AVLNode | None, val: int) -> AVLNode:
        """Recursively inserts value and rebalances ancestor nodes on the way up."""
        # 1. Standard BST insertion
        if node is None:
            return AVLNode(val)

        if val < node.val:
            node.left = self._insert_recursive(node.left, val)
        elif val > node.val:
            node.right = self._insert_recursive(node.right, val)
        else:
            return node  # Duplicates are ignored

        # 2. Update height of this ancestor node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # 3. Get Balance Factor to check if node became unbalanced
        balance = self.get_balance(node)

        # 4. If node is unbalanced, apply one of the 4 rotation cases:

        # Case 1: Left-Left (LL) -> Right Rotation
        if balance > 1 and node.left is not None and val < node.left.val:
            return self._right_rotate(node)

        # Case 2: Right-Right (RR) -> Left Rotation
        if balance < -1 and node.right is not None and val > node.right.val:
            return self._left_rotate(node)

        # Case 3: Left-Right (LR) -> Left-Right Rotation
        if balance > 1 and node.left is not None and val > node.left.val:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Case 4: Right-Left (RL) -> Right-Left Rotation
        if balance < -1 and node.right is not None and val < node.right.val:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    # -------------------------------------------------------------------------
    # TRAVERSAL & SEARCH
    # -------------------------------------------------------------------------
    def search(self, val: int) -> bool:
        """Searches for a value in O(log n) time."""
        curr = self.root
        while curr is not None:
            if curr.val == val:
                return True
            elif val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        return False

    def inorder_traversal(self) -> list[int]:
        """In-Order Traversal (Left -> Root -> Right). Always sorted."""
        result: list[int] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: AVLNode | None, result: list[int]) -> None:
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)