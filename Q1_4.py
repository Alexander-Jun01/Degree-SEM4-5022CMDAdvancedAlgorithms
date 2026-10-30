# Q1.4: Hash-table versus array search
#
# ======================================================================
# WHAT THIS FILE DOES (Brief Q1 #4)
#   Compares how long it takes to SEARCH for records in:
#     (a) the hash table from Q1_1.py, and
#     (b) a one-dimensional array (a Python list) searched one by one.
#   Both hold EXACTLY the same Medicine objects and receive EXACTLY the
#   same search IDs, so the comparison is fair.
#
# EXPECTED RESULT (and why) - VIVA
#   Hash table : jumps to slot ID % size -> about 1-3 probes per search
#                -> expected O(1), does not grow with the number of records.
#   Array      : checks records one by one -> about n/2 checks on average,
#                n checks for a missing ID -> O(n).
#   So the hash table should be much faster, and the gap grows with n.
#
# MENU
#   1 = the required experiment (1000 records, 2003 slots, 10 rounds)
#   2 = a custom experiment (you choose records, rounds, load factor)
# ======================================================================

# math   -> isfinite() and ceil() for the custom option
# random -> generate random but repeatable product IDs
# time   -> perf_counter_ns() for nanosecond timing
import math
import random
import time
from Q1_2 import Medicine
from Q1_1 import HashTable

# ----------------------------------------------------------------------
# array_search : LINEAR SEARCH of a list.
#   Checks records[0], records[1], ... until the ID matches.
#   Best case 1 check (first item), worst case n checks (last/missing).
#   Time complexity: O(n).
# ----------------------------------------------------------------------
# Search a one-dimensional list for an ID by checking records one at a time.
def array_search(records, product_id):
    # Visit each object in list order, which is a linear search.
    for medicine in records:
        # Compare this record ID with the requested ID.
        if medicine.product_id == product_id:
            # Stop the search and return the matching Medicine object.
            return medicine
    # No match was found; return None to tell the caller.
    return None

# ----------------------------------------------------------------------
# compare_search : run the timing experiment.
#   record_count -> how many medicines to store       (default 1000)
#   rounds       -> how many times to repeat the test (default 10)
#   table_size   -> number of hash-table slots        (default 2003)
#   Load factor = 1000 / 2003 = about 0.5 (half full) -> short probes.
#
# EXPERIMENT STEPS
#   1. Check the parameters.
#   2. Create random unique IDs (fixed seed -> same IDs every run).
#   3. Put the SAME Medicine objects into the hash table AND the list.
#   4. Check both methods give the same answers (also warms them up).
#   5. For each round, time all searches for each method.
#   6. Print each round and the average time per single search.
# ----------------------------------------------------------------------
# Compare both search methods using identical objects and queries.
def compare_search(record_count=1000, rounds=10, table_size=2003):
    # Bound the classroom experiment and reject impossible sampling or storage sizes.
    # `not 1 <= x <= 5000` means "x is outside 1..5000".
    if type(record_count) is not int or not 1 <= record_count <= 5000:
        raise ValueError("Use a record count from 1 to 5000.")
    if type(rounds) is not int or not 1 <= rounds <= 20:
        raise ValueError("Use a round count from 1 to 20.")
    # The table must have at least one slot per record.
    if type(table_size) is not int or not record_count <= table_size <= 50000:
        raise ValueError("Table size must hold all records and be at most 50000.")
    # Defaults retain the original 1000 records in 2003 slots for ten rounds.
    table = HashTable(table_size)
    # Create the one-dimensional list used for the comparison.
    records = []
    # A fixed seed generates the same dataset when the experiment is repeated.
    # EDIT HERE: change 5022 to test a different random dataset.
    generator = random.Random(5022)
    # Enlarge the ID pool for custom experiments while keeping all keys unique.
    # IDs come from 0 .. id_limit-1 (0..9999 by default).
    id_limit = max(10000, record_count * 10)
    # sample() picks record_count DIFFERENT numbers (no duplicate IDs).
    keys = generator.sample(range(id_limit), record_count)

    # Create a record for each sampled ID.
    for key in keys:
        # Construct one test product with this ID.
        medicine = Medicine(key, "Test medicine", 5.00, 10)
        # Put this object into the hash table under its ID.
        table.insert(key, medicine)
        # Put the same object into the list so both structures contain identical data.
        records.append(medicine)

    # Search every stored ID plus one missing ID outside the sampled range.
    # id_limit is never a stored ID (IDs are below it), so it tests an
    # UNSUCCESSFUL search - the array's worst case (checks every record).
    queries = keys + [id_limit]
    # Visit every search ID in the same shared query list.
    for key in queries:
        # Verify that both methods return the same object, or both return None.
        # assert stops the program if they ever disagree (correctness check).
        # This loop is NOT timed; it also "warms up" both functions.
        assert table.search(key) == array_search(records, key)

    # Start the accumulated hash-table search time at zero.
    hash_total = 0
    # Start the accumulated list-search time at zero.
    array_total = 0
    print(f"\n{record_count} records, {len(queries)} searches per round, {rounds} rounds")
    # :.1% shows a fraction as a percentage with 1 decimal place.
    print(f"Table capacity: {table_size} | Load: {record_count / table_size:.1%}")
    # Run the requested number of rounds; range excludes its upper limit.
    for round_number in range(1, rounds + 1):
        # Alternate order to reduce a consistent first-method advantage.
        # (Odd rounds: hash first. Even rounds: array first. This is fairer
        #  in case the computer is faster/slower at the start of a round.)
        # Set the initial measurement order to hash first, then array.
        methods = ["hash", "array"]
        # A zero remainder identifies an even round.
        if round_number % 2 == 0:
            # Measure the array first on even rounds to alternate the order.
            methods.reverse()

        # Measure each search method in this round's chosen order.
        for method in methods:
            # TIMING PATTERN: start = counter; do the work; end - start.
            # perf_counter_ns() is a high-resolution clock in NANOSECONDS
            # meant for measuring time intervals.
            # Nothing is printed inside the timed part (printing is slow).
            # Choose the hash-table branch for this measurement.
            if method == "hash":
                # Record a counter value immediately before the measured work.
                start = time.perf_counter_ns()
                # Visit every search ID in the same shared query list.
                for key in queries:
                    # Perform a hash-table lookup without printing inside the timed section.
                    table.search(key)
                # Subtract the start counter to measure this entire batch of hash searches.
                hash_time = time.perf_counter_ns() - start
            else:
                # Record a counter value immediately before the measured work.
                start = time.perf_counter_ns()
                # Visit every search ID in the same shared query list.
                for key in queries:
                    # Perform a linear lookup without printing inside the timed section.
                    array_search(records, key)
                # Subtract the start counter to measure this entire batch of array searches.
                array_time = time.perf_counter_ns() - start

        # Add this round's hash duration to its running total.
        hash_total += hash_time
        # Add this round's array duration to its running total.
        array_total += array_time
        # Each printed number is the time for the WHOLE batch (1001
        # searches), not for one search.
        print(f"Round {round_number}: Hash = {hash_time} ns | Array = {array_time} ns")

    # AVERAGE PER SEARCH = total time / (rounds x searches per round)
    # Default: total / (10 x 1001) = total / 10010.
    # Divide by the number of searches across all rounds; .1f shows one decimal place.
    print(f"Hash average per search: {hash_total / (rounds * len(queries)):.1f} ns")
    # Use the same denominator to calculate the array mean per search.
    print(f"Array average per search: {array_total / (rounds * len(queries)):.1f} ns")

# ======================================================================
# MENU (only runs when this file is started directly)
# ======================================================================
# Offer the required experiment and a configurable version of the same method.
def main():
    while True:
        print("\n=== Hash Table and Array Search Comparison ===")
        print("1. Run default comparison (1000 records, 10 rounds, 2003 slots)")
        print("2. Run custom comparison")
        print("0. Exit")
        choice = input("Enter choice: ").strip()
        try:
            # 1. Required experiment: uses the default parameters.
            if choice == "1":
                compare_search()
            # 2. Custom experiment: the user chooses the parameters.
            elif choice == "2":
                record_count = int(input("Record count (1-5000): "))
                rounds = int(input("Rounds (1-20): "))
                # Load factor = records / slots. 0.5 means half full.
                load = float(input("Target table load (0.1-1.0, e.g. 0.5): "))
                if not math.isfinite(load) or not 0.1 <= load <= 1.0:
                    raise ValueError("Use a finite load from 0.1 to 1.0.")
                # Round upwards so the actual load never exceeds the requested load.
                # Example: 100 records at load 0.5 -> ceil(200) = 200 slots.
                table_size = math.ceil(record_count / load)
                compare_search(record_count, rounds, table_size)
            elif choice == "0":
                print("Goodbye.")
                return
            else:
                print("Choose 0, 1 or 2.")
        except ValueError as error:
            print("Invalid entry:", error)


# Imported comparisons can still be called directly without opening a menu.
if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")
