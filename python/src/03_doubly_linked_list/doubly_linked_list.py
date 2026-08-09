class Node:
    """A node in a Doubly Linked List."""
    def __init__(
        self, 
        val: int, 
        prev_node: "Node | None" = None, 
        next_node: "Node | None" = None
    ):
        self.val = val
        self.prev = prev_node
        self.next = next_node


class DoublyLinkedList:
    """A custom implementation of a Doubly Linked List."""

    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None
        self.size: int = 0

    def _get_node(self, index: int) -> Node:
        """Helper method to return the Node object at a given index efficiently."""
        self._check_index(index)

        # Optimization: Start from head or tail depending on index proximity
        if index < self.size // 2:
            curr = self.head
            for _ in range(index):
                curr = curr.next  
        else:
            curr = self.tail
            for _ in range(self.size - 1 - index):
                curr = curr.prev 

        return curr  

    def get(self, index: int) -> int:
        """Returns the value at the given index."""
        return self._get_node(index).val

    def prepend(self, val: int) -> None:
        """Inserts a new node at the very beginning (Head)."""
        new_node = Node(val, prev_node=None, next_node=self.head)

        if self.size == 0:
            self.head = new_node
            self.tail = new_node
        else:
            self.head.prev = new_node 
            self.head = new_node

        self.size += 1

    def append(self, val: int) -> None:
        """Inserts a new node at the very end (Tail)."""
        new_node = Node(val, prev_node=self.tail, next_node=None)

        if self.size == 0:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node  
            self.tail = new_node

        self.size += 1

    def insert(self, index: int, val: int) -> None:
        """Inserts a new node at the specified index."""
        if index < 0 or index > self.size:
            raise IndexError("Index out of bounds")

        if index == 0:
            self.prepend(val)
            return
        if index == self.size:
            self.append(val)
            return

        # Get target node currently at index
        target = self._get_node(index)
        prev_node = target.prev

        new_node = Node(val, prev_node=prev_node, next_node=target)
        
        prev_node.next = new_node 
        target.prev = new_node

        self.size += 1

    def remove(self, index: int) -> int:
        """Removes and returns the value at the specified index."""
        self._check_index(index)

        target = self._get_node(index)
        val = target.val

        # Unlink Head
        if target.prev is None:
            self.head = target.next
        else:
            target.prev.next = target.next

        # Unlink Tail
        if target.next is None:
            self.tail = target.prev
        else:
            target.next.prev = target.prev

        self.size -= 1
        return val

    def reverse(self) -> None:
        """Reverses the list in-place by swapping prev and next pointers for each node."""
        if self.head is None or self.head.next is None:
            return

        curr = self.head
        new_head = None

        while curr is not None:
            # 1. Swap prev and next pointers
            temp = curr.prev
            curr.prev = curr.next
            curr.next = temp

            # 2. Track the new head (the original last node)
            new_head = curr

            # 3. Move forward (which is curr.prev after swapping!)
            curr = curr.prev

        # 4. Swap head and tail references
        self.tail = self.head
        self.head = new_head

    def getSize(self) -> int:
        return self.size

    def _check_index(self, index: int) -> None:
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")