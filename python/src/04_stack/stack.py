class Node:
    """A single node inside the Stack.
    
    Each node stores its data value and points to the node directly beneath it.
    """
    def __init__(self, val: int, next_node: "Node | None" = None):
        self.val = val
        self.next = next_node


class Stack:
    """A LIFO (Last-In, First-Out) Stack implementation.

    ===========================================================================
    VISUAL REPRESENTATION (LIFO Principle)
    ===========================================================================
    
       push(30) --->  [ 30 ]  <-- self.top (Newest element / First to pop)
                      [ 20 ]
                      [ 10 ]  <-- Base element (Oldest element / Last to pop)
                      [ None ]

    ===========================================================================
    CS COMPARISON: LIFO Stack vs. C Execution Stack & Heap
    ===========================================================================
    - DATA STRUCTURE (This class):
      An abstract data type (ADT) defined by behavior: push, pop, peek (LIFO).

    - C SYSTEM MEMORY LAYOUT (Stack vs. Heap):
      1. Execution Stack (Memory Region):
         - Fast, fixed-size memory managed automatically by the CPU.
         - Stores local variables, function calls, and return addresses.
         - Follows strict LIFO order: function frames are pushed when called 
           and popped when returning. (Over-allocation leads to 'Stack Overflow').
      2. Dynamic Heap (Memory Region):
         - Large, unstructured pool of global memory.
         - Allocation is dynamic and manual (`malloc` / `free` in C).
         - Persistent across function calls, but slower and risks memory leaks.
    ===========================================================================
    """
    def __init__(self):
        self.top: Node | None = None
        self.size: int = 0

    def push(self, val: int) -> None:
        """Pushes an element onto the top of the stack."""
        new_node = Node(val, next_node=self.top)
        self.top = new_node
        self.size += 1

    def pop(self) -> int:
        """Removes and returns the top element of the stack."""
        if self.is_empty() or self.top is None:
            raise IndexError("Pop from empty stack")

        val = self.top.val
        self.top = self.top.next
        self.size -= 1
        return val

    def peek(self) -> int:
        """Returns the top element without removing it."""
        if self.is_empty() or self.top is None:
            raise IndexError("Peek from empty stack")

        return self.top.val

    def is_empty(self) -> bool:
        """Returns True if the stack is empty, False otherwise."""
        return self.size == 0

    def getSize(self) -> int:
        """Returns the number of elements in the stack."""
        return self.size