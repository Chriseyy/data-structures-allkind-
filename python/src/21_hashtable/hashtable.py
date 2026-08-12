class HashTable:
    """A Hash Table implementation using Separate Chaining for collision resolution.

    ===========================================================================
    WHAT IS A HASH TABLE?
    ===========================================================================
    A data structure that maps key-value pairs by using a Hash Function to compute 
    an index into an array of buckets.

    ===========================================================================
    PYTHON BUILT-IN EQUIVALENT (dict)
    ===========================================================================
    In Python, a Hash Table is natively implemented as the built-in `dict`.
    Python's dictionary is an optimized, highly efficient hash table that 
    preserves insertion order and delivers O(1) average lookup times.

    ===========================================================================
    KEY CONCEPTS
    ===========================================================================
    1. Hash Function: Converts arbitrary keys into array indices (0 <= index < capacity).
    2. Collision Resolution (Separate Chaining): Each bucket holds a list (chain) 
       of (key, value) pairs to handle keys that hash to the same index.
    3. Load Factor & Resizing: When size / capacity exceeds threshold (e.g., 0.75),
       capacity is doubled and all pairs are rehashed to maintain O(1) performance.

    ===========================================================================
    TIME & SPACE COMPLEXITY CHEATSHEET
    ===========================================================================
    Operation   | Average Case  | Worst Case (All keys collide into 1 bucket)
    -----------------------------------------------------------------
    Put         | O(1)          | O(n)
    Get         | O(1)          | O(n)
    Remove      | O(1)          | O(n)
    
    Space Complexity: O(n)
    ===========================================================================
    """

    def __init__(self, initial_capacity: int = 8, load_factor_threshold: float = 0.75):
        self.capacity = initial_capacity
        self.load_factor_threshold = load_factor_threshold
        self.size = 0
        self.buckets: list[list[tuple[any, any]]] = [[] for _ in range(self.capacity)]

    def _hash(self, key: any) -> int:
        """Computes bucket index for a key using Python's built-in hash()."""
        return hash(key) % self.capacity

    @property
    def load_factor(self) -> float:
        """Returns current load factor (size / capacity)."""
        return self.size / self.capacity

    def put(self, key: any, value: any) -> None:
        """Inserts or updates a key-value pair in O(1) average time."""
        index = self._hash(key)
        bucket = self.buckets[index]

        # 1. Update value if key already exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # 2. Key not present -> Append new (key, value) pair
        bucket.append((key, value))
        self.size += 1

        # 3. Trigger dynamic resizing if load factor threshold is breached
        if self.load_factor > self.load_factor_threshold:
            self._resize(self.capacity * 2)

    def get(self, key: any, default: any = None) -> any:
        """Retrieves value for a key in O(1) average time."""
        index = self._hash(key)
        bucket = self.buckets[index]

        for k, v in bucket:
            if k == key:
                return v

        return default

    def remove(self, key: any) -> bool:
        """Removes key-value pair. Returns True if found & removed, False otherwise."""
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True

        return False

    def contains(self, key: any) -> bool:
        """Returns True if key exists in hash table, False otherwise."""
        index = self._hash(key)
        bucket = self.buckets[index]
        return any(k == key for k, _ in bucket)

    def _resize(self, new_capacity: int) -> None:
        """Doubles capacity and rehashes all existing key-value pairs."""
        old_buckets = self.buckets
        self.capacity = new_capacity
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0  # Will be re-incremented during re-put

        for bucket in old_buckets:
            for k, v in bucket:
                self.put(k, v)

    def keys(self) -> list[any]:
        """Returns a list of all keys stored in the hash table."""
        return [k for bucket in self.buckets for k, _ in bucket]

    def values(self) -> list[any]:
        """Returns a list of all values stored in the hash table."""
        return [v for bucket in self.buckets for _, v in bucket]