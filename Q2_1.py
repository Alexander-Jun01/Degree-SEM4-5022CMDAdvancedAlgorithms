# Q2.1: Generic unweighted directed graph
#
# ======================================================================
# WHAT THIS FILE DOES (Brief Q2 #1)
#   A reusable UNWEIGHTED DIRECTED GRAPH with the three required methods:
#     addVertex                  -> add a new vertex
#     addEdge                    -> connect source -> destination
#     listIncomingAdjacentVertex -> who points INTO this vertex?
#   Extra methods used by the advanced course features:
#     listOutgoingAdjacentVertex -> who does this vertex point TO?
#     removeEdge                 -> delete one edge
#     hasPath                    -> can we travel from A to B? (cycle check)
#
# ABSTRACTION (the brief's "programming best practice")
#   The Graph class has NO course-specific code. A vertex can be any
#   hashable object: a string "A", a number, or a Course object.
#   That is why the menu below can demonstrate it with plain letters.
#
# HOW THE GRAPH IS STORED: an ADJACENCY LIST (a dictionary)
#   adjacency = { vertex : [list of vertices it points to] }
#   Example:  {"A": ["B"], "B": [], "C": []}   means   A -> B
#   Directed  : A -> B is stored, but B -> A is NOT (unless added).
#   Unweighted: an edge has no number/cost, it simply exists or not.
#
# COMPLEXITY (V = vertices, E = edges, d = out-edges of one vertex)
#   storage O(V + E) | addVertex O(1) | addEdge O(d)
#   listIncoming O(V + E) | listOutgoing O(d) | hasPath O(V + E)*
#   (*the visited list makes the check slower for very big graphs)
# ======================================================================

# Store an unweighted directed graph without course-specific logic.
class Graph:
    # Create empty adjacency storage.
    def __init__(self):
        # Create a dictionary mapping each vertex to its outgoing-neighbour list.
        # Starts empty: no vertices, no edges.
        self.adjacency = {}

    # ------------------------------------------------------------------
    # addVertex (REQUIRED) : add a vertex with no edges yet.
    # ------------------------------------------------------------------
    # Add a new vertex with no edges.
    def addVertex(self, vertex):
        # Check whether this vertex already exists as a dictionary key.
        # `in` on a dictionary checks its keys - fast, O(1) on average.
        if vertex in self.adjacency:
            # Stop this operation and pass the explanatory error message to the caller.
            raise ValueError("Vertex already exists.")
        # Add the vertex with no outgoing edges yet.
        self.adjacency[vertex] = []

    # ------------------------------------------------------------------
    # addEdge (REQUIRED) : add ONE directed edge source -> destination.
    #   In the course system: prerequisite -> course that needs it.
    #   Example: addEdge(CS101, CS201) = "CS101 is needed for CS201".
    # ------------------------------------------------------------------
    # Connect one existing vertex to another in the specified direction.
    def addEdge(self, source, destination):
        # Require both endpoints to exist before adding the edge.
        if source not in self.adjacency or destination not in self.adjacency:
            # Stop this operation and pass the explanatory error message to the caller.
            raise ValueError("Both vertices must exist.")
        # Check whether this source already points to this destination.
        # (Prevents the same edge being stored twice.)
        if destination in self.adjacency[source]:
            # Stop this operation and pass the explanatory error message to the caller.
            raise ValueError("Edge already exists.")
        # Add source -> destination only; the reverse edge is not added.
        # This one line is what makes the graph DIRECTED.
        # (For an UNDIRECTED graph you would also add destination -> source.)
        self.adjacency[source].append(destination)

    # ------------------------------------------------------------------
    # removeEdge (extra, for advanced feature d) : delete source -> destination.
    # ------------------------------------------------------------------
    # Remove one directed edge, keeping the reverse direction unchanged.
    def removeEdge(self, source, destination):
        if source not in self.adjacency or destination not in self.adjacency:
            raise ValueError("Both vertices must exist.")
        # You cannot remove an edge that is not there.
        if destination not in self.adjacency[source]:
            raise ValueError("Edge does not exist.")
        # list.remove() deletes the first matching item from the list.
        self.adjacency[source].remove(destination)

    # ------------------------------------------------------------------
    # hasPath (extra, for the cycle check) : can we go from source to
    # destination by following edges? Uses DEPTH-FIRST SEARCH (DFS).
    #
    #   pending = a STACK of vertices still to explore (pop() takes the
    #             last one added -> depth-first).
    #   visited = vertices already explored, so we never loop forever.
    #
    # VIVA: Why do we need this?
    #   Before adding Y -> X ("X requires Y") we ask: can X already reach Y?
    #   If yes, Y -> X would close a loop (a course that, through a chain,
    #   requires itself), which is impossible to register for.
    # ------------------------------------------------------------------
    # Check whether following outgoing edges can reach a destination.
    def hasPath(self, source, destination):
        if source not in self.adjacency or destination not in self.adjacency:
            raise ValueError("Both vertices must exist.")
        # Start the search from the source vertex.
        pending = [source]
        visited = []
        # Keep going while there is something left to explore.
        while pending:
            # Take the most recently added vertex (stack = last in, first out).
            vertex = pending.pop()
            # Reached the target -> a path exists.
            if vertex == destination:
                return True
            # Only explore each vertex once.
            if vertex not in visited:
                visited.append(vertex)
                # Add all of its outgoing neighbours to explore next.
                pending.extend(self.adjacency[vertex])
        # Explored everything reachable without finding the destination.
        return False

    # ------------------------------------------------------------------
    # listIncomingAdjacentVertex (REQUIRED) : every vertex with an edge
    # INTO `vertex`. In the course system = the PREREQUISITES of a course.
    #
    # HOW: the dictionary only stores OUTGOING lists, so we look through
    # every vertex's list and collect those that contain the target.
    # Cost O(V + E) because every list is checked.
    # Example: CS102 -> CS301 and CS201 -> CS301, so the incoming list of
    # CS301 is [CS102, CS201].
    # ------------------------------------------------------------------
    # Find direct predecessors by scanning all outgoing lists.
    def listIncomingAdjacentVertex(self, vertex):
        # Check that the requested vertex belongs to this graph.
        if vertex not in self.adjacency:
            # Stop this operation and pass the explanatory error message to the caller.
            raise ValueError("Vertex does not exist.")
        # Start collecting the vertices that point directly to the target.
        incoming = []
        # Visit every vertex as a possible source of an incoming edge.
        for source in self.adjacency:
            # Check whether the target appears in this source's outgoing list.
            if vertex in self.adjacency[source]:
                # Save this source because it has an edge to the target.
                incoming.append(source)
        # Return the direct predecessors, or an empty list when there are none.
        return incoming

    # ------------------------------------------------------------------
    # listOutgoingAdjacentVertex : every vertex that `vertex` points TO.
    # In the course system = the courses this course UNLOCKS.
    # Example: CS201 -> CS301 and CS201 -> CS302, so the result is
    # [CS301, CS302].
    # ------------------------------------------------------------------
    # Return a copy of the direct outgoing neighbours.
    def listOutgoingAdjacentVertex(self, vertex):
        # Check that the requested vertex belongs to this graph.
        if vertex not in self.adjacency:
            # Stop this operation and pass the explanatory error message to the caller.
            raise ValueError("Vertex does not exist.")
        # Return a copy using [:], so callers cannot change the stored list accidentally.
        # VIVA: without [:] the caller would get the REAL list inside the
        # graph, and e.g. .clear() on it would delete the graph's edges.
        return self.adjacency[vertex][:]

# ======================================================================
# DEMONSTRATION MENU (only when this file is run directly)
#   Uses simple text labels (A, B, C...) to show the graph is generic.
# ======================================================================
# This display uses generic vertex labels, so it can demonstrate any domain.
def display_graph(graph):
    if not graph.adjacency:
        print("The graph is empty.")
    # Print each vertex and the vertices it points to, e.g. "A -> B".
    for vertex in graph.adjacency:
        neighbours = graph.listOutgoingAdjacentVertex(vertex)
        # ", ".join(...) makes "B, C"; if that text is empty, print "None".
        print(vertex, "->", ", ".join(str(item) for item in neighbours) or "None")


# Reject blank labels before adding or looking up a vertex.
def read_vertex(prompt):
    vertex = input(prompt).strip()
    # An empty string counts as False, so `not vertex` means "blank".
    if not vertex:
        raise ValueError("Vertex label cannot be empty.")
    return vertex


def main():
    # Sample graph so there is something to explore straight away.
    # EDIT HERE: change the starting vertices or edges.
    graph = Graph()
    for label in ["A", "B", "C"]:
        graph.addVertex(label)
    graph.addEdge("A", "B")
    print("Sample vertices: A, B, C. Sample edge: A -> B.")

    while True:
        print("\n=== Directed Graph ===")
        print("1. Add a vertex")
        print("2. Add a directed edge")
        print("3. View incoming vertices")
        print("4. View outgoing vertices")
        print("5. Remove a directed edge")
        print("6. Display graph")
        print("0. Exit")
        choice = input("Enter choice: ").strip()
        try:
            # 1. Add a vertex
            if choice == "1":
                vertex = read_vertex("New vertex label: ")
                graph.addVertex(vertex)
                print("Vertex added:", vertex)
            # 2. Add an edge / 5. Remove an edge (both need two labels)
            elif choice in ["2", "5"]:
                source = read_vertex("Source vertex: ")
                destination = read_vertex("Destination vertex: ")
                if choice == "2":
                    graph.addEdge(source, destination)
                    print("Edge added:", source, "->", destination)
                else:
                    graph.removeEdge(source, destination)
                    print("Edge removed:", source, "->", destination)
            # 3. Incoming / 4. Outgoing neighbours of one vertex
            elif choice in ["3", "4"]:
                vertex = read_vertex("Vertex label: ")
                if choice == "3":
                    neighbours = graph.listIncomingAdjacentVertex(vertex)
                    print("Incoming:", neighbours)
                else:
                    neighbours = graph.listOutgoingAdjacentVertex(vertex)
                    print("Outgoing:", neighbours)
            # 6. Show the whole graph
            elif choice == "6":
                display_graph(graph)
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Choose a number from 0 to 6.")
        # Errors from the Graph methods (missing vertex, duplicate edge...)
        # are printed and the menu continues.
        except ValueError as error:
            print("Invalid entry:", error)


# Importing Graph does not open the demonstration menu.
if __name__ == "__main__":
    main()
