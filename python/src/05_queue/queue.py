class Node:
    """A single node inside the Queue.
    
    Each node stores its value and a reference to the next node behind it in line.
    """
    def __init__(self, val: int, next_node: "Node | None" = None):
        self.val = val
        self.next = next_node


class Queue:
    """A FIFO (First-In, First-Out) Queue implementation.

    ===========================================================================
    VISUAL REPRESENTATION (FIFO Principle)
    ===========================================================================
    
      dequeue() <--- [ 10 ] ---> [ 20 ] ---> [ 30 ] <--- enqueue(40)
                      HEAD                    TAIL
                   (First Out)             (Last In)

    ===========================================================================
    PYTHON BUILT-IN ALTERNATIVE: collections.deque
    ===========================================================================
    In real-world Python development, you usually use `collections.deque`:
    - `deque` stands for "Double-Ended Queue".
    - `append()` serves as enqueue (O(1)).
    - `popleft()` serves as dequeue (O(1)).
    - Python lists (`list.pop(0)`) should NEVER be used as queues because 
      removing from index 0 takes O(n) time due to shifting elements!
    ===========================================================================
    """

    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None
        self.size: int = 0

    def enqueue(self, val: int) -> None:
        """Adds an element to the back of the queue (Tail).
        """
        new_node = Node(val)

        if self.size == 0 or self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def dequeue(self) -> int:
        """Removes and returns the front element of the queue (Head).
        """
        if self.is_empty() or self.head is None:
            raise IndexError("Dequeue from empty queue")

        val = self.head.val
        self.head = self.head.next
        self.size -= 1

        # Reset tail pointer if the queue became completely empty
        if self.size == 0:
            self.tail = None

        return val

    def peek(self) -> int:
        """Returns the front element without removing it.
        """
        if self.is_empty() or self.head is None:
            raise IndexError("Peek from empty queue")

        return self.head.val

    def is_empty(self) -> bool:
        """Checks whether the queue contains zero elements.
        """
        return self.size == 0

    def getSize(self) -> int:
        """Returns the total number of items currently in the queue.
        """
        return self.size