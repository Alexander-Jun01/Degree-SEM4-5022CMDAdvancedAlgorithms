# Q3.2: Fibonacci function and primitive-operation count
#
# ======================================================================
# WHAT THIS FILE DOES (Brief Q3 #2)
#   fibonacci(n) returns the nth Fibonacci number:
#     F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)
#     0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...
#   It also holds helper functions SHARED by Q3_3.py (with threads) and
#   Q3_4.py (without threads), so both experiments use identical code.
#
# BIG-O (Brief Q3.5(i)) - count primitive operations
#   (1 assignment / comparison / addition / return = 1 operation)
#     a = 0, b = 1, i = 0          -> 3
#     while i < n  (n+1 checks)    -> n + 1   (the last check is False)
#     next_value = a + b           -> 2 per loop (add + assign) = 2n
#     a = b ; b = next_value       -> 2 per loop                = 2n
#     i = i + 1                    -> 2 per loop (add + assign) = 2n
#     return a                     -> 1
#     input check                  -> constant C
#   T(n) = 3 + (n+1) + 6n + 1 + C = 7n + 5 + C   ->   O(n)  (linear)
#   Space: only a, b, i, next_value -> O(1).
#   Example: F(40) = 7*40 + 5 = 285 operations (+ C).
#
# VIVA: Why a loop and not recursion?
#   The textbook recursive version fib(n-1) + fib(n-2) recalculates the
#   same values again and again -> exponential time, about O(1.618^n).
#   F(40) would need hundreds of millions of calls. The loop needs 40.
# ======================================================================

# Calculate F(n) with a loop, using F(0) = 0 and F(1) = 1.
def fibonacci(n):
    # Require a non-negative integer; this check also rejects Boolean values.
    # (type(True) is bool, not int, so True/False are rejected too.)
    if type(n) != int or n < 0:
        # Stop this operation and pass the explanatory error message to the caller.
        raise ValueError("n must be a non-negative integer.")
    # Start a at F(0), the current Fibonacci value.
    a = 0
    # Start b at F(1), the next Fibonacci value.
    b = 1
    # Count the number of completed steps.
    i = 0
    # Advance the pair exactly n times.
    # LOOP RULE: at the start of every loop, a = F(i) and b = F(i+1).
    # TRACE for n = 5:
    #   i : 0  1  2  3  4  5
    #   a : 0  1  1  2  3  5   <- returns 5 = F(5)
    #   b : 1  1  2  3  5  8
    while i < n:
        # Compute the next Fibonacci value before overwriting the current pair.
        # (If we did a = b first, we would lose the old a and get it wrong.)
        next_value = a + b
        # Move the previous next value into the current position.
        a = b
        # Store the newly computed value as the next member of the pair.
        b = next_value
        # Count the completed step so the loop can stop at n.
        i = i + 1
    # After n steps, a contains F(n); when n is zero the loop is skipped.
    return a

# ----------------------------------------------------------------------
# Shared limits for the CUSTOM experiments (menu option 2 in Q3_3/Q3_4).
# EDIT HERE: change the largest n or the largest number of rounds allowed.
# ----------------------------------------------------------------------
# Keep interactive experiments small enough to print their results clearly.
MAX_NUMBER = 1000
MAX_ROUNDS = 100

# Check all three inputs before any timed work or worker threads begin.
# Returns them as a list. Used by both experiments, so the rules match.
def validate_numbers(numbers):
    # The brief uses exactly three values (one per thread).
    if len(numbers) != 3:
        raise ValueError("Enter exactly three Fibonacci inputs.")
    for number in numbers:
        if type(number) != int or number < 0 or number > MAX_NUMBER:
            raise ValueError("Each Fibonacci input must be an integer from 0 to 1000.")
    return list(numbers)

# Read one integer and explain the allowed range when the input is invalid.
# int() raises ValueError for text like "abc"; the range check raises one
# for numbers outside minimum..maximum. Both are caught by the menus.
def read_integer(prompt, minimum, maximum):
    value = int(input(prompt))
    if value < minimum or value > maximum:
        raise ValueError("Enter an integer from " + str(minimum) + " to " + str(maximum) + ".")
    return value

# The two experiment menus use the same input rules.
# Asks for three n values and a number of rounds (custom experiment).
def read_experiment_inputs():
    numbers = []
    # range(1, 4) gives 1, 2, 3 -> three inputs.
    for position in range(1, 4):
        number = read_integer("Fibonacci input " + str(position) + " (0-1000): ", 0, MAX_NUMBER)
        numbers.append(number)
    rounds = read_integer("Number of rounds (1-100): ", 1, MAX_ROUNDS)
    return numbers, rounds

# ----------------------------------------------------------------------
# show_results : print every round's time T, then the TOTAL and AVERAGE.
#   times -> list of nanosecond values, one per round.
#   Average = total / number of rounds.
#   Used by both Q3_3 and Q3_4 so their output looks the same.
# ----------------------------------------------------------------------
# Display every saved round and calculate the total and average in nanoseconds.
def show_results(title, times):
    print("\n===", title, "===")
    # An empty list would make the average divide by zero.
    if not times:
        print("No rounds completed; total and average are unavailable.")
        return
    total = 0
    for i in range(len(times)):
        # i starts at 0, so i + 1 shows rounds as 1, 2, 3, ...
        print(f"Round {i + 1}: T = {times[i]} ns")
        total += times[i]
    print(f"Total: {total} ns")
    # :.1f -> one decimal place.
    print(f"Average: {total / len(times):.1f} ns")

# Explain the same unit-cost model used in the portfolio discussion.
def explain_complexity():
    print("The loop runs exactly n times.")
    print("Count each assignment, addition, comparison and return as one operation.")
    print("Initial assignments: 3. Loop comparisons: n + 1.")
    print("Loop body: 6n. Return: 1. Validation: constant C.")
    print("Primitive operations: 7n + 5 + C; unit-cost time: O(n).")
    print("Large Python integers require more work per addition as their digits grow.")

# ======================================================================
# MENU (only when this file is run directly)
# ======================================================================
# Run this file directly to choose a calculation or review the explanation.
def main():
    while True:
        print("\n=== Fibonacci Calculator ===")
        print("1. Calculate a Fibonacci number")
        print("2. Show Fibonacci(35), Fibonacci(38) and Fibonacci(40)")
        print("3. Explain the operation count")
        print("0. Exit")
        try:
            choice = input("Enter choice: ").strip()
            # 1. Any n from 0 to 1000.
            if choice == "1":
                number = read_integer("Enter n (0-1000): ", 0, MAX_NUMBER)
                print("F(" + str(number) + ") =", fibonacci(number))
            # 2. The three values required by the brief.
            elif choice == "2":
                for number in [35, 38, 40]:
                    print("F(" + str(number) + ") =", fibonacci(number))
            # 3. Print the 7n + 5 + C explanation.
            elif choice == "3":
                explain_complexity()
            elif choice == "0":
                print("Goodbye.")
                return
            else:
                print("Choose 0, 1, 2 or 3.")
        except ValueError as error:
            print("Invalid entry:", error)
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return

if __name__ == "__main__":
    main()
