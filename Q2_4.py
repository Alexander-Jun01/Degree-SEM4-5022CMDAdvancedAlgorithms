# Q2.4: Construct the course-prerequisite graph
#
# ======================================================================
# WHAT THIS FILE DOES (Brief Q2 #4)
#   Builds the GRAPH OBJECT for the course-prerequisite system:
#     vertices = the 6 Course objects from Q2_3.py
#     edges    = "prerequisite -> course that requires it"
#
# EDGE DIRECTION (very important for the VIVA)
#   An edge Y -> X means "Y must be completed before X".
#     incoming edges of X  = X's PREREQUISITES     (what X needs)
#     outgoing edges of Y  = courses Y UNLOCKS      (what Y opens up)
#
#   The six edges:
#     CS101 -> CS201         CS201 -> CS302
#     CS201 -> CS301         CS301 -> CS401
#     CS102 -> CS301         CS102 -> CS401
#
#   So CS301 needs BOTH CS201 and CS102 (two incoming edges), and CS201
#   unlocks BOTH CS301 and CS302 (two outgoing edges). CS101 has no
#   prerequisites; CS401 unlocks nothing. There are no cycles.
# ======================================================================

from Q2_1 import Graph
from Q2_3 import create_courses, find_course

# Connect the Course instances created in Q2.3.
def create_prerequisite_graph():
    # Reuse these same objects as graph vertices.
    courses = create_courses()
    # "Unpack" the list into six named variables for readable edges below.
    c1, c2, c3, c4, c5, c6 = courses
    # Create an empty directed graph.
    graph = Graph()
    # Visit each Course object in the list.
    for course in courses:
        # Use this Course object as a graph vertex.
        graph.addVertex(course)

    # Each edge goes from the prerequisite to the course it unlocks.
    # EDIT HERE: add or remove prerequisite connections with addEdge(Y, X)
    # meaning "Y is a prerequisite of X". Keep the graph free of cycles.
    # Programming is a prerequisite for Data Structures.
    graph.addEdge(c1, c3)
    # Data Structures is a prerequisite for Advanced Algorithms.
    graph.addEdge(c3, c4)
    # Discrete Mathematics is another prerequisite for Advanced Algorithms.
    graph.addEdge(c2, c4)
    # Data Structures is a prerequisite for Database Systems.
    graph.addEdge(c3, c5)
    # Advanced Algorithms is a prerequisite for Machine Learning.
    graph.addEdge(c4, c6)
    # Discrete Mathematics is another prerequisite for Machine Learning.
    graph.addEdge(c2, c6)

    # Return both the profiles and their connected graph.
    # The list is used to find a course by code; the graph stores the edges.
    return courses, graph

# Look up both objects before adding or removing the edge Y -> X.
#   x_code = the course that needs the prerequisite (X)
#   y_code = the prerequisite course (Y)
#   remove = False -> add Y -> X,  True -> remove Y -> X
# (Q2_5.py has its own version, change_prerequisite(), for the main menu.)
def update_prerequisite(courses, graph, x_code, y_code, remove=False):
    course = find_course(courses, x_code)
    prerequisite = find_course(courses, y_code)
    if course is None or prerequisite is None:
        raise ValueError("Course not found.")
    if remove:
        graph.removeEdge(prerequisite, course)
    else:
        # If X already reaches Y, adding Y -> X would close a cycle.
        # Example: CS101 -> CS201 -> CS301. Making CS301 a prerequisite of
        # CS101 would mean CS101 indirectly requires itself.
        if graph.hasPath(course, prerequisite):
            raise ValueError("This prerequisite would create a cycle.")
        graph.addEdge(prerequisite, course)


# Print "CODE - Name" for each course, or "None" if the list is empty.
def display_related(courses):
    if not courses:
        print("None")
    for course in courses:
        print(course.courseCode, "-", course.courseName)


# ======================================================================
# DEMONSTRATION MENU: explore and change the prerequisite graph.
# (The full required course system is the menu in Q2_5.py.)
# ======================================================================
def main():
    courses, graph = create_prerequisite_graph()
    print("Use course codes such as CS101, CS102, CS201, CS301, CS302, CS401.")
    print("Direction: prerequisite Y -> course X.")
    while True:
        print("\n=== Course Prerequisite Graph ===")
        print("1. Display all relationships")
        print("2. View prerequisites of a course")
        print("3. View courses unlocked")
        print("4. Add a prerequisite")
        print("5. Remove a prerequisite")
        print("0. Exit")
        choice = input("Enter choice: ").strip()
        try:
            # 1. For every course: its incoming AND outgoing edges.
            if choice == "1":
                for course in courses:
                    print("\nCourse:", course.courseCode, "-", course.courseName)
                    print("Direct prerequisites:")
                    display_related(graph.listIncomingAdjacentVertex(course))
                    print("Courses directly unlocked:")
                    display_related(graph.listOutgoingAdjacentVertex(course))
            # 2. Prerequisites (incoming) / 3. Unlocked courses (outgoing)
            elif choice in ["2", "3"]:
                course = find_course(courses, input("Course code: "))
                if course is None:
                    raise ValueError("Course not found.")
                if choice == "2":
                    print("Direct prerequisites for", course.courseCode)
                    display_related(graph.listIncomingAdjacentVertex(course))
                else:
                    print("Courses directly unlocked by", course.courseCode)
                    display_related(graph.listOutgoingAdjacentVertex(course))
                    print("Other prerequisites must also be completed.")
            # 4. Add Y -> X / 5. Remove Y -> X
            elif choice in ["4", "5"]:
                x_code = input("Course X code: ")
                y_code = input("Prerequisite Y code: ")
                # choice == "5" is True for remove, False for add.
                update_prerequisite(courses, graph, x_code, y_code, choice == "5")
                if choice == "4":
                    print("Prerequisite added.")
                else:
                    print("Prerequisite removed.")
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Choose a number from 0 to 5.")
        except ValueError as error:
            print("Invalid entry:", error)


if __name__ == "__main__":
    main()
