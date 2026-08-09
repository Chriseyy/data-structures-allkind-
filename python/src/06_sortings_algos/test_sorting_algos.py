import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import time
import random
import pytest
from sorting_algos import AllSortingAlgorithms

if __name__ == "__main__":
    pytest.main(["-s", __file__])


SORTING_METHODS = [
    ("Bubble Sort", AllSortingAlgorithms.bubble_sort),
    ("Selection Sort", AllSortingAlgorithms.selection_sort),
    ("Insertion Sort", AllSortingAlgorithms.insertion_sort),
    ("Merge Sort", AllSortingAlgorithms.merge_sort),
    ("Quick Sort", AllSortingAlgorithms.quick_sort),
    ("Heap Sort", AllSortingAlgorithms.heap_sort),
    ("Timsort", AllSortingAlgorithms.timsort),
]


# --- EDGE CASES & BASIC CORRECTNESS ---

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


# --- VARIOUS ARRAY SIZES (5, 10, 30, 100) ---

@pytest.mark.parametrize("size", [5, 10, 30, 100])
@pytest.mark.parametrize("name, sort_fn", SORTING_METHODS)
def test_random_array_sizes(name, sort_fn, size):
    """Test correctness across different array sizes."""
    # Seed fixed for deterministic reproducibility per test run
    random.seed(size)
    random_data = [random.randint(-1000, 1000) for _ in range(size)]
    expected = sorted(random_data)

    assert sort_fn(random_data) == expected


# --- PERFORMANCE & BENCHMARK WITH TIME PRINTING ---

def test_benchmark_execution_times():
    """Prints a comparison benchmark table with execution times for 500 elements."""
    size = 500
    random.seed(42)
    test_data = [random.randint(-5000, 5000) for _ in range(size)]
    expected = sorted(test_data)

    print(f"\n\n{'='*60}")
    print(f"  SORTING BENCHMARK RESULTS ({size} Random Elements)")
    print(f"{'='*60}")
    print(f"{'Algorithm Name':<20} | {'Status':<10} | {'Execution Time (ms)':<20}")
    print(f"{'-'*60}")

    for name, sort_fn in SORTING_METHODS:
        # Measure time using perf_counter for microsecond precision
        start_time = time.perf_counter()
        result = sort_fn(test_data)
        elapsed_time_ms = (time.perf_counter() - start_time) * 1000

        # Verify correctness
        status = "PASSED" if result == expected else "FAILED"
        print(f"{name:<20} | {status:<10} | {elapsed_time_ms:>15.3f} ms")

        assert result == expected

    print(f"{'='*60}\n")