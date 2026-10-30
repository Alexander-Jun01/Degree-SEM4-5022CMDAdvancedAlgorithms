# Q3.4: Compare required and custom experiments without multithreading.
#
# ======================================================================
# WHAT THIS FILE DOES (Brief Q3 #4)
#   The SAME work as Q3_3.py - F(35), F(38), F(40), 10 rounds - but
#   WITHOUT threads: the three calls run one after another in the main
#   thread. Each round's time is measured, then the total and average.
#
#   Same fibonacci() function, same show_results() output and same input
#   rules as Q3_3.py, so the ONLY difference is threads vs no threads.
#
# HOW T IS MEASURED HERE
#   start -> F(35) -> F(38) -> F(40) -> end;   T = end - start
#   (In Q3_3 T = last thread's end - first thread's start.)
# ======================================================================

import time
from Q3_2 import fibonacci, show_results, validate_numbers, read_experiment_inputs, MAX_ROUNDS

# ----------------------------------------------------------------------
# sequential_round : ONE round, three calculations in a row.
#   Returns (list of 3 results, elapsed time T in ns).
# ----------------------------------------------------------------------
# Perform the same three calculations one after another in the current thread.
def sequential_round(numbers=(35, 38, 40)):
    # Validate outside the timed region so invalid input never starts an experiment.
    numbers = validate_numbers(numbers)
    # Start the clock immediately before the work.
    start = time.perf_counter_ns()
    results = []
    # Each call must finish before the next one begins (no overlap).
    for number in numbers:
        results.append(fibonacci(number))
    # Stop the clock immediately after the last calculation.
    elapsed = time.perf_counter_ns() - start
    return results, elapsed

# ----------------------------------------------------------------------
# run_experiment : repeat sequential_round() (10 rounds by default),
#   check the answers, then print each T, the total and the average.
#   EDIT HERE: change the defaults (35, 38, 40) or rounds=10 - keep them
#   the same as in Q3_3.py so the comparison stays fair.
# ----------------------------------------------------------------------
# Defaults preserve the assignment's three values and ten rounds.
def run_experiment(numbers=(35, 38, 40), rounds=10):
    import sys
    numbers = validate_numbers(numbers)
    if type(rounds) != int or rounds < 1 or rounds > MAX_ROUNDS:
        raise ValueError("The number of rounds must be an integer from 1 to 100.")
    # Show the interpreter details so results can be compared with Q3_3.
    print("Python:", sys.version.split()[0])
    if hasattr(sys, "_is_gil_enabled"):
        print("GIL enabled:", sys._is_gil_enabled())
    print("Inputs:", numbers, "| Rounds:", rounds)
    # Validate answers after each round, outside its measured interval.
    expected = [fibonacci(number) for number in numbers]
    times = []
    for round_number in range(rounds):
        values, elapsed = sequential_round(numbers)
        if values != expected:
            raise ValueError("The experiment returned an incorrect Fibonacci result.")
        times.append(elapsed)
    print("Fibonacci results:", values)
    # Prints Round 1..10: T = ... ns, then Total and Average.
    show_results("Without multithreading", times)
    # The returned dictionary is used by the automated tests.
    return {"mode": "sequential", "numbers": numbers, "rounds": rounds,
            "values": values, "times": times, "total_ns": sum(times),
            "average_ns": sum(times) / rounds}

# ======================================================================
# MENU: the same choices as Q3_3.py, for a fair side-by-side comparison.
# ======================================================================
# Give the user the same choices as the threaded program for fair comparisons.
def main():
    while True:
        print("\n=== Fibonacci Without Multithreading ===")
        print("1. Run the required experiment (35, 38, 40; 10 rounds)")
        print("2. Run a custom experiment")
        print("0. Exit")
        try:
            choice = input("Enter choice: ").strip()
            if choice == "1":
                run_experiment()
            elif choice == "2":
                numbers, rounds = read_experiment_inputs()
                run_experiment(numbers, rounds)
            elif choice == "0":
                print("Goodbye.")
                return
            else:
                print("Choose 0, 1 or 2.")
        except ValueError as error:
            print("Invalid entry:", error)
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return

if __name__ == "__main__":
    main()
