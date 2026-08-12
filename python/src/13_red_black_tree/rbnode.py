from enum import Enum


class Color(Enum):
    RED = 1
    BLACK = 2


class RBNode:
    """A node inside a Red-Black Tree."""
    def __init__(self, val: int, color: Color = Color.RED):
        self.val = val
        self.color: Color = color
        self.left: RBNode | None = None
        self.right: RBNode | None = None
        self.parent: RBNode | None = None


class RedBlackTree:
    """A Self-Balancing Red-Black Binary Search Tree implementation.

    ===========================================================================
    RED-BLACK TREE PROPERTIES
    ===========================================================================
    1. Every node is either RED or BLACK.
    2. The root is always BLACK.
    3. Every leaf (NIL / None) is BLACK.
    4. RED nodes cannot have RED children (No Red-Red conflicts).
    5. Every path from a node to leaves contains the exact same number of BLACK nodes.
    ===========================================================================
    """

    def __init__(self):
        self.root: RBNode | None = None

    # -------------------------------------------------------------------------
    # HELPER METHODS (Color Handling & Rotations)
    # -------------------------------------------------------------------------
    def _get_color(self, node: RBNode | None) -> Color:
        """NIL / None leaves are defined as BLACK by rule #3."""
        if node is None:
            return Color.BLACK
        return node.color

    def _left_rotate(self, x: RBNode) -> None:
        """Performs a Left Rotation around node x."""
        y = x.right
        assert y is not None

        x.right = y.left
        if y.left is not None:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, x: RBNode) -> None:
        """Performs a Right Rotation around node x."""
        y = x.left
        assert y is not None

        x.left = y.right
        if y.right is not None:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    # -------------------------------------------------------------------------
    # INSERTION & FIXUP REBALANCING
    # -------------------------------------------------------------------------
    def insert(self, val: int) -> None:
        """Inserts a new value and fixes Red-Black property violations."""
        new_node = RBNode(val, color=Color.RED)
        parent: RBNode | None = None
        curr = self.root

        # 1. Standard BST insertion with parent pointer tracking
        while curr is not None:
            parent = curr
            if new_node.val < curr.val:
                curr = curr.left
            elif new_node.val > curr.val:
                curr = curr.right
            else:
                return  # Ignore duplicate values

        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif new_node.val < parent.val:
            parent.left = new_node
        else:
            parent.right = new_node

        # 2. Fix potential Red-Black property violations
        self._fix_insert(new_node)

    def _fix_insert(self, k: RBNode) -> None:
        """Fixes Red-Red conflicts caused by inserting a new RED node."""
        while k.parent is not None and k.parent.color == Color.RED:
            grandparent = k.parent.parent
            if grandparent is None:
                break

            # Case A: Parent is Left Child of Grandparent
            if k.parent == grandparent.left:
                uncle = grandparent.right

                # Case 1: Uncle is RED -> Recoloring
                if self._get_color(uncle) == Color.RED:
                    k.parent.color = Color.BLACK
                    if uncle:
                        uncle.color = Color.BLACK
                    grandparent.color = Color.RED
                    k = grandparent
                else:
                    # Case 2: k is Right Child -> Left Rotate Parent
                    if k == k.parent.right:
                        k = k.parent
                        self._left_rotate(k)

                    # Case 3: k is Left Child -> Right Rotate Grandparent
                    k.parent.color = Color.BLACK
                    grandparent.color = Color.RED
                    self._right_rotate(grandparent)

            # Case B: Parent is Right Child of Grandparent (Symmetric)
            else:
                uncle = grandparent.left

                # Case 1: Uncle is RED -> Recoloring
                if self._get_color(uncle) == Color.RED:
                    k.parent.color = Color.BLACK
                    if uncle:
                        uncle.color = Color.BLACK
                    grandparent.color = Color.RED
                    k = grandparent
                else:
                    # Case 2: k is Left Child -> Right Rotate Parent
                    if k == k.parent.left:
                        k = k.parent
                        self._right_rotate(k)

                    # Case 3: k is Right Child -> Left Rotate Grandparent
                    k.parent.color = Color.BLACK
                    grandparent.color = Color.RED
                    self._left_rotate(grandparent)

        # Rule #2 Enforcement: Root MUST always be BLACK
        if self.root is not None:
            self.root.color = Color.BLACK

    # -------------------------------------------------------------------------
    # SEARCH & TRAVERSALS
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

    def _inorder(self, node: RBNode | None, result: list[int]) -> None:
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)