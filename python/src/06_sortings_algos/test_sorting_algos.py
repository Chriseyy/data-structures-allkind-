import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import time
import random
import pytest
from sorting_algos import AllSortingAndSearchingAlgorithms

if __name__ == "__main__":
    pytest.main(["-s", "-v", __file__])


# List of all 9 sorting algorithms to test dynamically via parametrization
SORTING_METHODS = [
    ("Bubble Sort", AllSortingAndSearchingAlgorithms.bubble_sort),
    ("Selection Sort", AllSortingAndSearchingAlgorithms.selection_sort),
    ("Insertion Sort", AllSortingAndSearchingAlgorithms.insertion_sort),
    ("Merge Sort", AllSortingAndSearchingAlgorithms.merge_sort),
    ("Quick Sort", AllSortingAndSearchingAlgorithms.quick_sort),
    ("Heap Sort", AllSortingAndSearchingAlgorithms.heap_sort),
    ("Timsort", AllSortingAndSearchingAlgorithms.timsort),
    ("Counting Sort", AllSortingAndSearchingAlgorithms.counting_sort),
    ("Radix Sort", AllSortingAndSearchingAlgorithms.radix_sort),
]


# =============================================================================
# 1. SORTING ALGORITHMS - EDGE CASES & BASIC CORRECTNESS
# =============================================================================

@pytest.mark.parametrize("name, sort_fn", SORTING_METHODS)
def test_empty_and_single_element(name, sort_fn):
    """Test standard edge cases: Empty lists and single element lists."""
    assert sort_fn([]) == []
    assert sort_fn([42]) == [42]


@pytest.mark.parametrize("name, sort_fn", SORTING_METHODS)
def test_duplicates_and_identical_elements(name, sort_fn):
    """Test lists with all identical values or heavy duplicate counts."""
    assert sort_fn([5, 5, 5, 5, 5]) == [5, 5, 5, 5, 5]
    assert sort_fn([2, 1, 2, 1, 2, 1]) == [1, 1, 1, 2, 2, 2]


@pytest.mark.parametrize("name, sort_fn", SORTING_METHODS)
def test_negative_numbers_and_zero(name, sort_fn):
    """Test inputs containing negative values, zero, and positive values."""
    unsorted = [-5, 10, -20, 0, 15, -1]
    expected = [-20, -5, -1, 0, 10, 15]
    assert sort_fn(unsorted) == expected


@pytest.mark.parametrize("name, sort_fn", SORTING_METHODS)
def test_already_sorted_and_reverse_sorted(name, sort_fn):
    """Test best-case (already sorted) and worst-case (reversed) inputs."""
    already_sorted = [1, 2, 3, 4, 5, 6, 7]
    reversed_list = [7, 6, 5, 4, 3, 2, 1]
    expected = [1, 2, 3, 4, 5, 6, 7]

    assert sort_fn(already_sorted) == expected
    assert sort_fn(reversed_list) == expected


# =============================================================================
# 2. SORTING ALGORITHMS - VARIOUS ARRAY SIZES (5, 10, 30, 100)
# =============================================================================

@pytest.mark.parametrize("size", [5, 10, 30, 100])
@pytest.mark.parametrize("name, sort_fn", SORTING_METHODS)
def test_random_array_sizes(name, sort_fn, size):
    """Test correctness across different array sizes."""
    random.seed(size)
    random_data = [random.randint(-1000, 1000) for _ in range(size)]
    expected = sorted(random_data)

    assert sort_fn(random_data) == expected


# =============================================================================
# 3. SEARCHING ALGORITHMS - LINEAR & BINARY SEARCH TESTS
# =============================================================================

def test_linear_search_functionality():
    """Linear Search works on both unsorted and sorted arrays."""
    unsorted_data = [15, 3, 42, -10, 7, 0]

    assert AllSortingAndSearchingAlgorithms.linear_search(unsorted_data, 42) == 2
    assert AllSortingAndSearchingAlgorithms.linear_search(unsorted_data, -10) == 3
    assert AllSortingAndSearchingAlgorithms.linear_search(unsorted_data, 99) == -1
    assert AllSortingAndSearchingAlgorithms.linear_search([], 5) == -1


def test_binary_search_functionality():
    """Binary Search requires pre-sorted arrays and operates in O(log n)."""
    sorted_data = [-20, -5, 0, 3, 10, 15, 42, 100]

    assert AllSortingAndSearchingAlgorithms.binary_search(sorted_data, -20) == 0
    assert AllSortingAndSearchingAlgorithms.binary_search(sorted_data, 3) == 3
    assert AllSortingAndSearchingAlgorithms.binary_search(sorted_data, 100) == 7
    assert AllSortingAndSearchingAlgorithms.binary_search(sorted_data, 99) == -1
    assert AllSortingAndSearchingAlgorithms.binary_search(sorted_data, -50) == -1
    assert AllSortingAndSearchingAlgorithms.binary_search([], 10) == -1


# =============================================================================
# 4. PERFORMANCE BENCHMARKS (SORTING & SEARCHING)
# =============================================================================

def test_benchmark_sorting_execution_times():
    """Prints a comparison benchmark table for all 9 sorting algorithms (500 elements)."""
    size = 500
    random.seed(42)
    test_data = [random.randint(-5000, 5000) for _ in range(size)]
    expected = sorted(test_data)

    print(f"\n\n{'='*65}")
    print(f"  SORTING BENCHMARK RESULTS ({size} Random Elements)")
    print(f"{'='*65}")
    print(f"{'Algorithm Name':<20} | {'Status':<10} | {'Execution Time (ms)':<20}")
    print(f"{'-'*65}")

    for name, sort_fn in SORTING_METHODS:
        start_time = time.perf_counter()
        result = sort_fn(test_data)
        elapsed_time_ms = (time.perf_counter() - start_time) * 1000

        status = "PASSED" if result == expected else "FAILED"
        print(f"{name:<20} | {status:<10} | {elapsed_time_ms:>15.3f} ms")

        assert result == expected

    print(f"{'='*65}\n")


def test_benchmark_search_execution_times():
    """Benchmark comparing Linear Search O(n) vs Binary Search O(log n) on 10,000 elements."""
    size = 10000
    sorted_data = list(range(size))
    target = 9999

    start = time.perf_counter()
    lin_idx = AllSortingAndSearchingAlgorithms.linear_search(sorted_data, target)
    lin_time_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    bin_idx = AllSortingAndSearchingAlgorithms.binary_search(sorted_data, target)
    bin_time_ms = (time.perf_counter() - start) * 1000

    print(f"\n\n{'='*65}")
    print(f"  SEARCH BENCHMARK RESULTS ({size} Sorted Elements)")
    print(f"{'='*65}")
    print(f"Linear Search O(n)   : {lin_time_ms:.4f} ms | Found Index: {lin_idx}")
    print(f"Binary Search O(log n): {bin_time_ms:.4f} ms | Found Index: {bin_idx}")
    print(f"{'='*65}\n")

    assert lin_idx == bin_idx == 9999