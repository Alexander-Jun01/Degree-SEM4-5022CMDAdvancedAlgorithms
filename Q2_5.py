# Q2.5: Menu for course and prerequisite queries
#
# ======================================================================
# WHAT THIS FILE DOES (Brief Q2 #5) - THE MAIN COURSE SYSTEM
#   MAIN MENU - mandatory features
#     1. List all course names                    (feature a)
#     2. View full details of one course          (feature b)
#     3. View prerequisites   = INCOMING edges    (feature c)
#     4. View courses unlocked = OUTGOING edges   (feature d)
#     5. Open the Advanced Features submenu
#     0. Exit
#   ADVANCED SUBMENU - all four optional features
#     1. Add a course on demand        (new vertex)            (adv a)
#     2. Profile by level              (elective: name only)    (adv b)
#     3. Add prerequisite Y to X       (new edge Y -> X)        (adv c)
#     4. Remove prerequisite Y from X  (delete edge Y -> X)     (adv d)
#     0. Return to the main menu
#
#   Both menus share the SAME `courses` list and `graph`, so anything
#   changed in the submenu is visible in the main menu afterwards.
#   Data is kept in memory and resets when the program closes.
# ======================================================================

from Q2_4 import create_prerequisite_graph
from Q2_2 import Course

# Find the Course object with this code (the caller normalises the code
# with .strip().upper() first). Returns None if no course matches.
def find_course(courses, code):
    # Visit each Course object in the list.
    for course in courses:
        # Compare the stored course identifier with the requested code.
        if course.courseCode == code:
            # Return the matching Course object immediately.
            return course
    # No match was found; return None to tell the caller.
    return None

# Print "CODE - Name" for each course in a list.
def display_courses(courses):
    # Visit each Course object in the list.
    for course in courses:
        print(course.courseCode, "-", course.courseName)

# ----------------------------------------------------------------------
# ADVANCED FEATURE (a): add a course on demand = create a NEW VERTEX.
#   Every check happens BEFORE anything is changed, so a rejected course
#   never half-appears in the list or the graph.
# ----------------------------------------------------------------------
# Validate a new profile before changing either the list or graph.
def add_course(courses, graph, code, name, credits, level):
    # Remove spaces at both ends and standardise the course code, for example cs101 becomes CS101.
    code = code.strip().upper()
    # Remove spaces at the beginning and end of the course name.
    name = name.strip()
    # Remove surrounding spaces and standardise the level to core or elective in lowercase.
    level = level.strip().lower()

    # An empty string is false; reject the input if either code or name is empty.
    if not code or not name:
        # Stop this operation with an error that the submenu will catch and display.
        raise ValueError("Course code and name cannot be empty.")

    # A returned Course object means this code already belongs to an existing course.
    if find_course(courses, code) is not None:
        # Reject the duplicate without changing the course list or graph.
        raise ValueError("Course code already exists.")

    # Count the existing courses and prevent adding an eleventh course.
    # EDIT HERE: the brief says a maximum of 10 courses.
    if len(courses) >= 10:
        # Report the course limit and stop adding this profile.
        raise ValueError("A maximum of 10 courses is allowed.")

    # Reject zero or negative credit hours, or a level outside the two allowed values.
    if type(credits) is not int or credits <= 0 or level not in ["core", "elective"]:
        # Tell the caller which values must be corrected.
        raise ValueError("Use positive whole-number credit hours and level core or elective.")

    # Create the Course object only after all validation checks have passed.
    course = Course(code, name, credits, level)
    # Add this same Course object as a graph vertex with no outgoing edges yet.
    graph.addVertex(course)
    # Add the object to the list used by the menus and code-based lookup.
    courses.append(course)
    # Finish the function and give the newly created object to its caller.
    return course

# ----------------------------------------------------------------------
# ADVANCED FEATURE (b): level-based profile.
#   elective -> only the name is shown (other details hidden)
#   core     -> all details are shown
#   NOTE: main menu option 2 (mandatory) still shows EVERYTHING; this
#   rule applies only to this advanced view.
# ----------------------------------------------------------------------
# Apply the advanced view without changing the mandatory full-details view.
def display_profile(course):
    # Check whether the selected course uses the restricted advanced profile view.
    # EDIT HERE: to change what electives show, edit the print below
    # (e.g. also print the credit hours).
    if course.level == "elective":
        # Display only the elective course name; do not print its code, credits or level.
        print("Name:", course.courseName)
    else:
        # For a core course, call its display method to print all four attributes.
        course.display()

# ----------------------------------------------------------------------
# ADVANCED FEATURES (c) and (d): add or remove a prerequisite.
#   "Course X requires course Y"  is stored as the edge  Y -> X.
#   remove=False -> add Y -> X   (feature c, with a cycle check)
#   remove=True  -> remove Y -> X (feature d)
# ----------------------------------------------------------------------
# Course X requires Y, so the directed edge goes from Y to X.
def change_prerequisite(courses, graph, x_code, y_code, remove=False):
    # Find course X, which will require the prerequisite; normalise the entered code first.
    course = find_course(courses, x_code.strip().upper())
    # Find course Y, which must be completed before X.
    prerequisite = find_course(courses, y_code.strip().upper())
    # Check whether either entered code failed to match an existing Course object.
    if course is None or prerequisite is None:
        # Stop without changing any edges when a course is missing.
        raise ValueError("Course not found.")

    # Use the removal branch when remove is True; its default False selects addition.
    if remove:
        # Remove Y -> X, so Y is no longer a direct prerequisite of X.
        # (removeEdge raises ValueError if that edge does not exist.)
        graph.removeEdge(prerequisite, course)
    else:
        # Adding Y -> X would create a cycle if X already reaches Y.
        # If X already reaches Y, adding Y -> X would create a circular prerequisite chain.
        # VIVA example: CS101 -> CS201 -> CS301 already exists. Asking for
        # "CS101 requires CS301" (CS301 -> CS101) is rejected because
        # CS101 can already reach CS301. X == Y is also caught, because a
        # vertex always "reaches" itself.
        if graph.hasPath(course, prerequisite):
            # Reject the edge before changing the graph, including a course requiring itself.
            raise ValueError("This prerequisite would create a cycle.")
        # Add Y -> X; the graph method also rejects an already-existing edge.
        graph.addEdge(prerequisite, course)

# ======================================================================
# ADVANCED FEATURES SUBMENU
# ======================================================================
# Share the main menu's existing list and graph, so changes remain visible.
def advanced_menu(courses, graph):
    # Keep showing the submenu until the return statement exits this function.
    while True:
        print("\n=== Advanced Features ===")
        print("1. Add a course")
        print("2. View profile by course level")
        print("3. Add a prerequisite")
        print("4. Remove a prerequisite")
        print("0. Return to University Courses")
        # Read the option as text and remove surrounding spaces.
        choice = input("Enter choice: ").strip()

        # Handle invalid numeric input or a ValueError from a helper without closing the submenu.
        try:
            # Select the add-course action.
            if choice == "1":
                # Ask for the identifier of the new course.
                code = input("New course code: ")
                # Ask for the full course name.
                name = input("Course name: ")
                # Convert the entered text to an integer; non-integer text raises ValueError.
                credits = int(input("Credit hours: "))
                # Ask whether this course is core or elective; add_course validates the answer.
                level = input("Level (core/elective): ")
                # Validate the inputs and add the course to the shared list and graph.
                add_course(courses, graph, code, name, credits, level)
                # Display this menu option or status message in the Run console.
                print("Course added.")

            # Select the profile view that follows the course-level visibility rule.
            elif choice == "2":
                # Read a course code and normalise it for lookup.
                code = input("Course code: ").strip().upper()
                # Find the existing Course object, returning None if there is no match.
                course = find_course(courses, code)
                # Check whether the entered code was not found.
                if course is None:
                    print("Course not found.")
                # Use this alternative when the preceding condition is false.
                else:
                    # Show only the name for electives, or all attributes for core courses.
                    display_profile(course)

            # Both add and remove actions need the same two course codes.
            elif choice in ["3", "4"]:
                # Ask for the course that requires, or currently requires, the prerequisite.
                x_code = input("Course X code: ")
                # Ask for the course to add or remove as the prerequisite.
                y_code = input("Prerequisite Y code: ")
                # The comparison supplies True for option 4 (remove) and False for option 3 (add).
                change_prerequisite(courses, graph, x_code, y_code, choice == "4")
                # Choose the success message for the completed add operation.
                if choice == "3":
                    print("Prerequisite added.")
                else:
                    print("Prerequisite removed.")

            # Select the action that returns to the University Courses menu.
            elif choice == "0":
                # End only advanced_menu; execution resumes in the main menu with the same data.
                return
            else:
                print("Choose 0, 1, 2, 3 or 4.")

        # Catch a ValueError raised inside try and store its message in error.
        except ValueError as error:
            # Display the error; the while loop then shows the submenu again.
            print("Invalid entry:", error)


# ======================================================================
# MAIN MENU - the four mandatory features
# ======================================================================
def main():
    # Build the sample data before accepting menu choices.
    # courses = list of 6 Course objects, graph = their prerequisite edges.
    courses, graph = create_prerequisite_graph()

    # Repeat the menu until the exit branch reaches break.
    while True:
        print("\n=== University Courses ===")
        print("1. List all courses")
        print("2. View course details")
        print("3. View prerequisites")
        print("4. View courses unlocked")
        print("5. Advanced features")
        print("0. Exit")
        # Read the choice as text and remove surrounding spaces.
        choice = input("Enter choice: ").strip()

        # MANDATORY (a): list every course's name (with its code).
        # Handle the menu option to list all courses.
        if choice == "1":
            # Print the code and name of every course in the list.
            display_courses(courses)

        # These three options share the step of selecting one course.
        elif choice in ["2", "3", "4"]:
            # Remove surrounding spaces and convert lowercase input to uppercase.
            code = input("Course code: ").strip().upper()
            # Look up the object needed for the selected menu action.
            course = find_course(courses, code)
            # Handle a code that does not match any course.
            if course is None:
                print("Course not found.")
                # Skip the remaining actions and return to the beginning of the menu loop.
                continue

            # MANDATORY (b): all details, even for an elective course.
            # When it is "2. View course details".
            if choice == "2":
                # Display all fields, including when the course is elective.
                course.display()

            # MANDATORY (c): prerequisites = vertices with an edge INTO this course.
            # Example: CS301 -> [CS102, CS201].
            # When it is "3. View prerequisites".
            elif choice == "3":
                # Incoming sources are the courses required before this course.
                prerequisites = graph.listIncomingAdjacentVertex(course)
                print("Direct prerequisites for", course.courseCode)
                # Check whether the list of prerequisites is empty.
                if len(prerequisites) == 0:
                    print("No prerequisites required.")
                else:
                    # List the prerequisite course codes and names.
                    display_courses(prerequisites)

            # MANDATORY (d): unlocked courses = vertices this course points TO.
            # Example: CS201 -> [CS301, CS302].
            # When it is "4. View courses unlocked".
            else:
                # Outgoing destinations are courses that depend directly on this course.
                unlocked = graph.listOutgoingAdjacentVertex(course)
                print("Courses directly unlocked by", course.courseCode)
                # Check whether there are no directly dependent courses.
                if len(unlocked) == 0:
                    print("No further courses.")
                else:
                    # List the directly dependent courses found by the query.
                    display_courses(unlocked)
                    # A course can need several prerequisites (CS301 needs
                    # CS201 AND CS102), so finishing one may not be enough.
                    print("Other prerequisites must also be completed.")

        # Open the submenu using the current data.
        elif choice == "5":
            advanced_menu(courses, graph)
        # Handle the menu option to exit.

        elif choice == "0":
            print("Goodbye.")
            # Leave the menu loop.
            break
        else:
            print("Choose a number from 0 to 5.")

# Run the example only when this file is started directly.
if __name__ == "__main__":
    # Run all four required menu features.
    main()
