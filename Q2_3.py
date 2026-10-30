# Q2.3: Create six course profiles
#
# ======================================================================
# WHAT THIS FILE DOES (Brief Q2 #3)
#   Creates the course PROFILES: 6 Course objects (the brief requires a
#   minimum of 5 and a maximum of 10).
#   Q2_4.py then connects these SAME objects in the prerequisite graph.
#
#   Code   Name                          Credits Level
#   CS101  Introduction to Programming   3       core
#   CS102  Discrete Mathematics          3       core
#   CS201  Data Structures               4       core
#   CS301  Advanced Algorithms           4       core
#   CS302  Database Systems              3       elective
#   CS401  Machine Learning              3       elective
# ======================================================================

from Q2_2 import Course

def create_courses():
    # Construct the course with its code, name, credit hours and core/elective level.
    # EDIT HERE: change a course's details, or add c7 = Course(...) and put
    # it in the list below (keep the total at 10 or fewer). If you add one,
    # also update the unpacking line in Q2_4.py (c1, ..., c6 = courses).
    c1 = Course("CS101", "Introduction to Programming", 3, "core")
    c2 = Course("CS102", "Discrete Mathematics", 3, "core")
    c3 = Course("CS201", "Data Structures", 4, "core")
    c4 = Course("CS301", "Advanced Algorithms", 4, "core")
    c5 = Course("CS302", "Database Systems", 3, "elective")
    c6 = Course("CS401", "Machine Learning", 3, "elective")
    # Keep all six objects in a list for display and code-based lookup.
    courses = [c1, c2, c3, c4, c5, c6]

    # Return the six course profiles without constructing a graph.
    return courses

# Match a code to its existing Course object.
# Returns the Course whose code matches, or None if there is none.
# The entered code is normalised first, so "cs101" finds "CS101".
# This is a simple linear search: O(n) for n courses (n <= 10 here).
def find_course(courses, code):
    code = code.strip().upper()
    for course in courses:
        if course.courseCode == code:
            return course
    return None


# Keep the standalone profile list within the assignment's ten-course limit.
# Adds a new profile to the list (used by this file's demo menu only).
def add_profile(courses, code, name, credits, level):
    # EDIT HERE: the maximum number of courses (brief: at most 10).
    if len(courses) >= 10:
        raise ValueError("A maximum of 10 courses is allowed.")
    # Course codes must be unique.
    if find_course(courses, code) is not None:
        raise ValueError("Course code already exists.")
    # Course() validates the remaining fields.
    course = Course(code, name, credits, level)
    courses.append(course)
    return course


# ======================================================================
# DEMONSTRATION MENU: list, view and add course profiles (no graph yet).
# ======================================================================
def main():
    courses = create_courses()
    while True:
        print("\n=== Course Profiles ===")
        print("1. List course names")
        print("2. View one full profile")
        print("3. Add a course profile")
        print("4. Display all full profiles")
        print("0. Exit")
        choice = input("Enter choice: ").strip()
        try:
            # 1. Code and name of every course, plus how many exist.
            if choice == "1":
                print("Courses:", len(courses), "/ 10")
                for course in courses:
                    print(course.courseCode, "-", course.courseName)
            # 2. Every field of one chosen course.
            elif choice == "2":
                course = find_course(courses, input("Course code: "))
                if course is None:
                    print("Course not found.")
                else:
                    course.display()
            # 3. Add a new profile (validated by add_profile and Course).
            elif choice == "3":
                code = input("New course code: ")
                name = input("Course name: ")
                credits = int(input("Credit hours: "))
                level = input("Level (core/elective): ")
                course = add_profile(courses, code, name, credits, level)
                print("Course added:", course.courseCode)
            # 4. Every field of every course.
            elif choice == "4":
                for course in courses:
                    course.display()
                    print()
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Choose a number from 0 to 4.")
        except ValueError as error:
            print("Invalid entry:", error)


if __name__ == "__main__":
    main()
