# Q2.2: Course entity class and interactive profile editor.
#
# ======================================================================
# WHAT THIS FILE DOES (Brief Q2 #2)
#   Defines the COURSE entity class - one course offered by a university.
#   Each Course object later becomes one VERTEX in the graph (Q2_4.py).
#
#   Attributes (names follow the brief's examples):
#     courseCode  : str -> e.g. "CS101", always stored in UPPER case
#     courseName  : str -> e.g. "Introduction to Programming"
#     creditHours : int -> positive whole number, e.g. 3
#     level       : str -> only "core" or "elective" (stored lower case)
#
# VIVA: How are Course objects used as graph vertices?
#   Course is an ordinary class, so Python compares and hashes objects by
#   IDENTITY (which object it is), not by their field values. The program
#   therefore always reuses the SAME Course objects created in Q2_3.py.
#   A new Course("CS101", ...) with equal values would be a different
#   vertex.
# ======================================================================

class Course:
    # Validate all fields before storing a new course profile.
    def __init__(self, courseCode, courseName, creditHours, level):
        # NORMALISE the text first so "cs101 " and "CS101" are the same.
        #   .strip() removes spaces at both ends
        #   .upper() / .lower() make the letter case consistent
        courseCode = courseCode.strip().upper()
        courseName = courseName.strip()
        level = level.strip().lower()
        # VALIDATE: reject bad data so an invalid Course can never exist.
        # An empty string counts as False -> `not courseCode` = blank code.
        if not courseCode or not courseName:
            raise ValueError("Course code and name cannot be empty.")
        # type(...) is not int also rejects 3.5 and True/False.
        if type(creditHours) is not int or creditHours <= 0:
            raise ValueError("Credit hours must be a positive whole number.")
        # EDIT HERE: to allow another level (e.g. "mpu"), add it to this list
        # and to the identical check in add_course() in Q2_5.py.
        if level not in ["core", "elective"]:
            raise ValueError("Level must be core or elective.")
        # All checks passed -> store the four attributes.
        self.courseCode = courseCode
        self.courseName = courseName
        self.creditHours = creditHours
        self.level = level
        # EDIT HERE: to add an attribute (e.g. lecturer), add a parameter,
        # validate it, store it here, print it in display(), and update
        # every Course(...) call (Q2_3.py, read_course() below, and
        # add_course() in Q2_5.py).

    # The compulsory details view always prints all four fields.
    # (Brief Q2 #5b mandatory: "ignore the level/visibility setting and
    #  display all information" - so electives show everything here.)
    def display(self):
        print("Code:", self.courseCode)
        print("Name:", self.courseName)
        print("Credit hours:", self.creditHours)
        print("Level:", self.level)


# Reuse this input form when creating or replacing the demonstration profile.
# Asks for the four fields and returns a NEW validated Course object.
def read_course():
    code = input("Course code: ")
    name = input("Course name: ")
    # int() raises ValueError if the user types letters.
    credits = int(input("Credit hours: "))
    level = input("Level (core/elective): ")
    return Course(code, name, credits, level)


# ======================================================================
# DEMONSTRATION MENU: view or replace ONE sample course profile.
# ======================================================================
def main():
    course = Course("CS302", "Database Systems", 3, "elective")
    while True:
        print("\n=== Course Profile ===")
        print("1. View full profile")
        print("2. Create a replacement profile")
        print("3. Edit current profile")
        print("0. Exit")
        choice = input("Enter choice: ").strip()
        try:
            if choice == "1":
                course.display()
            elif choice in ["2", "3"]:
                if choice == "3":
                    print("Enter all updated fields for this profile.")
                # A failed form leaves the previous Course object unchanged.
                # If read_course() raises ValueError, the next line never
                # runs, so `course` still holds the old valid profile.
                new_course = read_course()
                course = new_course
                print("Profile saved.")
                course.display()
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Choose 0, 1, 2 or 3.")
        except ValueError as error:
            print("Invalid entry:", error)


# Importing Course does not run the profile editor.
if __name__ == "__main__":
    main()
