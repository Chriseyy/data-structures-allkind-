class DynamicArray:

    def __init__(self, capacity: int = 2):
        self.capacity = max(1, capacity)
        self.size = 0
        self.array = [0] * self.capacity

    def get(self, i: int) -> int:
        self._check_index(i)
        return self.array[i]

    def set(self, i: int, n: int) -> None:
        self._check_index(i)
        self.array[i] = n

    def pushback(self, n: int) -> None:
        if self.size == self.capacity:
            self.resize(self.capacity * 2)
        self.array[self.size] = n
        self.size += 1

    def popback(self) -> int:
        if self.size == 0:
            raise IndexError("pop from empty DynamicArray")
        self.size -= 1
        val = self.array[self.size]
        
        if self.size > 0 and self.size <= self.capacity // 4 and self.capacity // 2 >= 2:
            self.resize(self.capacity // 2)
            
        return val

    def insert(self, i: int, n: int) -> None:
        if i < 0 or i > self.size:
            raise IndexError("Index out of bounds")
        if self.size == self.capacity:
            self.resize(self.capacity * 2)
        # Elemente nach rechts verschieben
        for j in range(self.size - 1, i - 1, -1):
            self.array[j + 1] = self.array[j]
        self.array[i] = n
        self.size += 1

    def remove(self, i: int) -> int:
        self._check_index(i)
        val = self.array[i]
        # Elemente nach links aufrücken
        for j in range(i, self.size - 1):
            self.array[j] = self.array[j + 1]
        self.size -= 1
        
        if self.size > 0 and self.size <= self.capacity // 4 and self.capacity // 2 >= 2:
            self.resize(self.capacity // 2)
            
        return val

    def resize(self, new_capacity: int) -> None:
        self.capacity = new_capacity
        new_array = [0] * self.capacity
        for i in range(self.size):
            new_array[i] = self.array[i]
        self.array = new_array

    def getSize(self) -> int:
        return self.size

    def getCapacity(self) -> int:
        return self.capacity

    def _check_index(self, i: int) -> None:
        if i < 0 or i >= self.size:
            raise IndexError("Index out of bounds")