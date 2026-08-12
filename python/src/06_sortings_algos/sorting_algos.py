class AllSortingAndSearchingAlgorithms:
    """Implementations of Sorting Algorithms + 2 Searching Algorithms."""

# --- 1. BUBBLE SORT O(n^2) ---
    @staticmethod
    def bubble_sort(arr: list[int]) -> list[int]:
        """Bubble Sort: Repeatedly swaps adjacent elements if they are in wrong order."""
        n = len(arr)
        a = arr.copy()
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    swapped = True
            if not swapped:
                break
                
        return a

    # --- 2. SELECTION SORT O(n^2) ---
    @staticmethod
    def selection_sort(arr: list[int]) -> list[int]:
        """Selection Sort: Finds the minimum element and places it at the beginning."""
        n = len(arr)
        a = arr.copy()
        
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if a[j] < a[min_idx]:
                    min_idx = j
            a[i], a[min_idx] = a[min_idx], a[i]
            
        return a

    # --- 3. INSERTION SORT O(n^2) ---
    @staticmethod
    def insertion_sort(arr: list[int]) -> list[int]:
        """Insertion Sort: Inserts each element into its correct position in a sorted sublist."""
        a = arr.copy()
        
        for i in range(1, len(a)):
            key = a[i]
            j = i - 1
            while j >= 0 and a[j] > key:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = key
            
        return a

    # --- 4. MERGE SORT O(n log n) ---
    @staticmethod
    def merge_sort(arr: list[int]) -> list[int]:
        """Merge Sort: Divide & Conquer, splits in half and merges sorted halves."""
        if len(arr) <= 1:
            return arr
            
        mid = len(arr) // 2
        left = AllSortingAndSearchingAlgorithms.merge_sort(arr[:mid])
        right = AllSortingAndSearchingAlgorithms.merge_sort(arr[mid:])
        
        return AllSortingAndSearchingAlgorithms._merge(left, right)

    @staticmethod
    def _merge(left: list[int], right: list[int]) -> list[int]:
        """Helper for Merge Sort."""
        result: list[int] = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
                
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    # --- 5. QUICK SORT O(n log n) average ---
    @staticmethod
    def quick_sort(arr: list[int]) -> list[int]:
        """Quick Sort: Partitioning around a pivot element."""
        if len(arr) <= 1:
            return arr
            
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return (
            AllSortingAndSearchingAlgorithms.quick_sort(left)
            + middle
            + AllSortingAndSearchingAlgorithms.quick_sort(right)
        )

    # --- 6. HEAP SORT O(n log n) ---
    @staticmethod
    def heap_sort(arr: list[int]) -> list[int]:
        """Heap Sort: Uses a Max-Heap to repeatedly extract the maximum element."""
        a = arr.copy()
        n = len(a)
        
        for i in range(n // 2 - 1, -1, -1):
            AllSortingAndSearchingAlgorithms._heapify(a, n, i)
            
        for i in range(n - 1, 0, -1):
            a[i], a[0] = a[0], a[i]
            AllSortingAndSearchingAlgorithms._heapify(a, i, 0)
            
        return a

    @staticmethod
    def _heapify(arr: list[int], n: int, i: int) -> None:
        """Helper to maintain Max-Heap property for subtree rooted at index i."""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] > arr[largest]:
            largest = left
            
        if right < n and arr[right] > arr[largest]:
            largest = right
            
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            AllSortingAndSearchingAlgorithms._heapify(arr, n, largest)

    # --- 7. TIMSORT O(n log n) [Python Default] ---
    @staticmethod
    def timsort(arr: list[int], run_size: int = 32) -> list[int]:
        """Timsort: Python's default algorithm combining Insertion Sort & Merge Sort."""
        a = arr.copy()
        n = len(a)

        for start in range(0, n, run_size):
            end = min(start + run_size - 1, n - 1)
            AllSortingAndSearchingAlgorithms._insertion_sort_range(a, start, end)

        size = run_size
        while size < n:
            for left in range(0, n, 2 * size):
                mid = min(n - 1, left + size - 1)
                right = min(left + 2 * size - 1, n - 1)

                if mid < right:
                    AllSortingAndSearchingAlgorithms._merge_in_place(a, left, mid, right)

            size *= 2

        return a

    @staticmethod
    def _insertion_sort_range(arr: list[int], left: int, right: int) -> None:
        """Helper: Insertion Sort applied only on a sub-range [left..right]."""
        for i in range(left + 1, right + 1):
            key = arr[i]
            j = i - 1
            while j >= left and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key

    @staticmethod
    def _merge_in_place(arr: list[int], l: int, m: int, r: int) -> None:
        """Helper: Merges two adjacent sorted subarrays arr[l..m] and arr[m+1..r]."""
        left_sub = arr[l : m + 1]
        right_sub = arr[m + 1 : r + 1]

        i = j = 0
        k = l

        while i < len(left_sub) and j < len(right_sub):
            if left_sub[i] <= right_sub[j]:
                arr[k] = left_sub[i]
                i += 1
            else:
                arr[k] = right_sub[j]
                j += 1
            k += 1

        while i < len(left_sub):
            arr[k] = left_sub[i]
            i += 1
            k += 1

        while j < len(right_sub):
            arr[k] = right_sub[j]
            j += 1
            k += 1

    # --- 8. COUNTING SORT O(n + k) [Non-Comparison] ---
    @staticmethod
    def counting_sort(arr: list[int]) -> list[int]:
        """Counting Sort: Non-comparison integer sorting algorithm."""
        if not arr:
            return []

        min_val = min(arr)
        max_val = max(arr)
        range_of_elements = max_val - min_val + 1

        count = [0] * range_of_elements
        output = [0] * len(arr)

        for num in arr:
            count[num - min_val] += 1

        for i in range(1, len(count)):
            count[i] += count[i - 1]

        for i in range(len(arr) - 1, -1, -1):
            output[count[arr[i] - min_val] - 1] = arr[i]
            count[arr[i] - min_val] -= 1

        return output

    # --- 9. RADIX SORT O(d * (n + k)) [Non-Comparison] ---
    @staticmethod
    def radix_sort(arr: list[int]) -> list[int]:
        """Radix Sort: Digit-by-digit LSD (Least Significant Digit) sorting."""
        if not arr:
            return []

        negatives = [-x for x in arr if x < 0]
        positives = [x for x in arr if x >= 0]

        def _sort_positives(nums: list[int]) -> list[int]:
            if not nums:
                return []
            max_num = max(nums)
            exp = 1
            while max_num // exp > 0:
                nums = AllSortingAndSearchingAlgorithms._counting_sort_by_digit(nums, exp)
                exp *= 10
            return nums

        sorted_pos = _sort_positives(positives)
        sorted_neg = _sort_positives(negatives)
        sorted_neg = [-x for x in reversed(sorted_neg)]

        return sorted_neg + sorted_pos

    @staticmethod
    def _counting_sort_by_digit(arr: list[int], exp: int) -> list[int]:
        """Helper for Radix Sort: Stable counting sort based on current digit position (exp)."""
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = (arr[i] // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1

        return output

    # =========================================================================
    # SEARCHING ALGORITHMS
    # =========================================================================

    # --- 10. LINEAR SEARCH O(n) ---
    @staticmethod
    def linear_search(arr: list[int], target: int) -> int:
        """Linear Search: Sequentially scans list for target value."""
        for i, num in enumerate(arr):
            if num == target:
                return i
        return -1

    # --- 11. BINARY SEARCH O(log n) ---
    @staticmethod
    def binary_search(arr: list[int], target: int) -> int:
        """Binary Search: Repeatedly halves search space on a SORTED array."""
        left, right = 0, len(arr) - 1

        while left <= right:
            mid = (left + right) // 2

            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1