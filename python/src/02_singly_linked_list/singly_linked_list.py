class Node:
    """A node in a Singly Linked List."""
    def __init__(self, val: int, next_node: "Node | None" = None):
        self.val = val
        self.next = next_node


class SinglyLinkedList:
    """A custom implementation of a Singly Linked List."""
    
    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None
        self.size: int = 0

    def get(self, index: int) -> int:
        """Returns the value of the node at the given index."""
        self._check_index(index)

        curr = self.head
        for _ in range(index):
            curr = curr.next
        return curr.val

        # def _get_recursive(curr: Node, current_index: int) -> int:
        #     if current_index == 0:
        #         return curr.val
        
        #     return _get_recursive(curr.next, current_index - 1)  

        # return _get_recursive(self.head, index)  

    def _check_index(self, index: int) -> None:
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")

    def prepend(self, val: int) -> None:
        """Inserts a new node with 'val' at the very beginning (Head)."""
        new_node = Node(val, self.head)
        self.head = new_node

        if self.size == 0:
            self.tail = new_node

        self.size += 1

    def append(self, val: int) -> None:
        """Inserts a new node with 'val' at the very end (Tail)."""
        new_node = Node(val)
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
            
        # Traverse to node at (index - 1)
        prev = self.head
        for _ in range(index - 1):
            prev = prev.next  
            
        new_node = Node(val, prev.next)  
        prev.next = new_node  
        self.size += 1

    def remove(self, index: int) -> int:
        """Removes and returns the node value at the specified index."""
        self._check_index(index)
        
        # Removing Head
        if index == 0:
            val = self.head.val  
            self.head = self.head.next  
            self.size -= 1
            if self.size == 0:
                self.tail = None
            return val

        # Traverse to node at (index - 1)
        prev = self.head
        for _ in range(index - 1):
            prev = prev.next  
            
        target_node = prev.next 
        val = target_node.val
        
        # Unlink the node
        prev.next = target_node.next 
        
        # If removing Tail update tail pointer
        if index == self.size - 1:
            self.tail = prev
            
        self.size -= 1
        return val

    def reverse(self) -> None:
        """Reverses the linked list in-place (O(1) auxiliary space)."""
        prev = None
        curr = self.head
        self.tail = self.head  # Old head becomes new tail
        
        while curr is not None:
            temp_next = curr.next  # 1. Save next node
            curr.next = prev       # 2. Reverse pointer
            prev = curr            # 3. Move prev forward
            curr = temp_next       # 4. Move curr forward
            
        self.head = prev  

    def getSize(self) -> int:
        return self.size