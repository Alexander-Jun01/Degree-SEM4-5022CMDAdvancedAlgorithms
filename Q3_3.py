# Q3.3: Ten rounds using three threads
#
# ======================================================================
# WHAT THIS FILE DOES (Brief Q3 #3)
#   Calculates F(35), F(38) and F(40) using MULTITHREADING:
#     - 3 separate threads, ONE thread per value
#     - time measured in NANOSECONDS
#     - T = end time of the thread that finished LAST
#           - start time of the thread that started FIRST
#     - repeated for 10 rounds, then the total and average are shown
#
# HOW A ROUND WORKS
#   1. Make 3 Calculation "job" objects (one per number).
#   2. Make 3 Thread objects, each told to run one job.
#   3. start() all three threads  -> they now run concurrently.
#   4. join() all three threads   -> main thread waits for them to finish.
#   5. Read each job's start/end times and results; T = max(ends) - min(starts).
#
# VIVA: What result did we get, and why?
#   Threads were SLOWER than the sequential version (Q3_4.py), because:
#   - CPython's GIL lets only ONE thread run Python code at a time, so
#     CPU-bound work like Fibonacci cannot run in parallel;
#   - each calculation is tiny (35-40 loops), so the cost of creating,
#     starting and switching threads is bigger than the work itself.
#   Threads DO help with I/O-bound work (e.g. downloading several web
#   pages), because a waiting thread releases the GIL.
# ======================================================================

import threading
import time
from Q3_2 import fibonacci, show_results, validate_numbers, read_experiment_inputs, MAX_ROUNDS

# ----------------------------------------------------------------------
# Calculation : one job for one thread.
#   Holds the input number, the result and that thread's own start/end
#   times.
#
# VIVA: DATA CONSISTENCY - why no lock is needed
#   Each thread writes ONLY to its own Calculation object. No two threads
#   ever change the same variable, so there is no race condition. The
#   main thread reads the results only AFTER join(), when every thread
#   has finished writing.
# ----------------------------------------------------------------------
# Keep one worker's input, result and timestamps together.
class Calculation:
    # Prepare the fields for one calculation job.
    def __init__(self, number):
        # Store the input that this particular job must calculate.
        self.number = number
        # Use None until this job has calculated its answer.
        self.result = None
        # Reserve a field for this worker's start counter.
        self.start_time = 0
        # Reserve a field for this worker's finish counter.
        self.end_time = 0

    # This method is what each THREAD runs.
    # Time one calculation and save the answer on this job object.
    def run(self):
        # Each thread writes only to its own Calculation object.
        # perf_counter_ns() = high-resolution clock in nanoseconds, made for
        # measuring time intervals (better than the wall clock time_ns(),
        # which can jump if the system clock is adjusted).
        # Record this worker's start just before its calculation.
        self.start_time = time.perf_counter_ns()
        # Calculate the answer and save it on this worker's own object.
        self.result = fibonacci(self.number)
        # Record the finish immediately after the calculation and result assignment.
        self.end_time = time.perf_counter_ns()

# ----------------------------------------------------------------------
# threaded_round : ONE round = 3 threads calculating 3 numbers.
#   Returns (list of 3 results, elapsed time T in ns).
# ----------------------------------------------------------------------
# Create three threads, wait for them and calculate the required time interval.
def threaded_round(numbers=(35, 38, 40)):
    # Validate all three inputs before starting any worker.
    numbers = validate_numbers(numbers)
    # Create one independent job object for each selected Fibonacci input.
    jobs = []
    for number in numbers:
        jobs.append(Calculation(number))
    # Prepare a list to hold the three Thread objects.
    threads = []

    # Visit each calculation job in its original order.
    for job in jobs:
        # Pass the method without (); the thread calls it later when started.
        # VIVA: target=job.run   -> gives the thread the method to run later.
        #       target=job.run() -> would run it NOW in the main thread
        #                           (no multithreading at all).
        thread = threading.Thread(target=job.run)
        # Keep this thread so the program can start it and wait for it later.
        threads.append(thread)
    # Visit each of the three Thread objects.
    for thread in threads:
        # Start this worker in a separate thread; directly calling run() would not do that.
        thread.start()
    # Visit each of the three Thread objects.
    # VIVA: start ALL threads first, THEN join them. If we joined inside the
    # start loop, each thread would finish before the next began (no overlap).
    for thread in threads:
        # Wait for this worker to finish; the preceding loop has already started all workers.
        thread.join()

    # Read results only after all three threads have finished.
    # Prepare to collect every worker's start counter.
    starts = []
    # Prepare to collect every worker's finish counter.
    ends = []
    # Prepare to collect the answers in job order.
    results = []
    # Visit each calculation job in its original order.
    for job in jobs:
        # Add this job's start counter to the list.
        starts.append(job.start_time)
        # Add this job's finish counter to the list.
        ends.append(job.end_time)
        # Add this job's Fibonacci answer to the results.
        results.append(job.result)

    # Use the latest finish minus the earliest start, not the sum of worker durations.
    # THE BRIEF'S FORMULA:
    #   T = End_Time_Of_Thread_Finished_Last - Start_Time_Of_Thread_That_Started_First
    # VIVA example: starts [100, 90, 110], ends [120, 140, 130]
    #   T = max(ends) - min(starts) = 140 - 90 = 50 ns
    elapsed = max(ends) - min(starts)
    # Return the answers and elapsed time as a pair of values.
    return results, elapsed



# ----------------------------------------------------------------------
# run_experiment : repeat threaded_round() for several rounds (10 by
#   default), check every answer, then print each T, the total and the
#   average via show_results().
#   EDIT HERE: change the defaults (35, 38, 40) or rounds=10.
# ----------------------------------------------------------------------
# Run the required experiment by default, or use validated custom inputs.
def run_experiment(numbers=(35, 38, 40), rounds=10):
    import sys
    numbers = validate_numbers(numbers)
    if type(rounds) != int or rounds < 1 or rounds > MAX_ROUNDS:
        raise ValueError("The number of rounds must be an integer from 1 to 100.")
    # Print the Python version and whether the GIL is on, because the
    # result depends on the interpreter (the GIL check exists only in
    # Python 3.13+, hence hasattr).
    print("Python:", sys.version.split()[0])
    if hasattr(sys, "_is_gil_enabled"):
        print("GIL enabled:", sys._is_gil_enabled())
    print("Inputs:", numbers, "| Rounds:", rounds)
    # Calculate expected answers before measuring any round.
    expected = [fibonacci(number) for number in numbers]
    times = []
    for round_number in range(rounds):
        values, elapsed = threaded_round(numbers)
        # Every round must produce the correct answers, otherwise stop.
        if values != expected:
            raise ValueError("A worker returned an incorrect Fibonacci result.")
        times.append(elapsed)
    print("Fibonacci results:", values)
    # Prints Round 1..10: T = ... ns, then Total and Average.
    show_results("With multithreading", times)
    # The returned dictionary is used by the automated tests.
    return {"mode": "threaded", "numbers": numbers, "rounds": rounds,
            "values": values, "times": times, "total_ns": sum(times),
            "average_ns": sum(times) / rounds}

# ======================================================================
# MENU: 1 = required experiment, 2 = custom numbers/rounds.
# Use the same custom values in Q3_4.py to compare fairly.
# ======================================================================
# Required and custom experiments have separate choices for clear evidence.
def main():
    while True:
        print("\n=== Fibonacci With Multithreading ===")
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
