from collections import deque
import copy
import sys


class Vertex:
    """
    Models vertices in a graph.  The pi, color, and d attributes
    are used to store information as part of a breadth-first search.
    The name attribute is used for a unique identifier for each
    vertex.
    """
    def __init__(self, pi=None, color="WHITE", d=sys.maxsize, name=None):
        self.pi = pi
        self.color = color
        self.d = d
        self.name = name

    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        if (isinstance(other, Vertex)):
            return self.name == other.name
        else:
            return self.name == other

def load_data(training_flname, testing_flname):
    """
    Loads the training and testing set data. Returns
    a pair of graphs corresponding to the two data sets.
    """
    # We want to avoid creating duplicate Vertex objects
    # for the same user.  We will check the dictionary for
    # an existing Vertex object before creating another
    vertices = dict()
    with open(training_flname) as fl:
        G1 = DiGraph()
        for ln in fl:
            cols = ln.split()
            if cols[0] not in vertices:
                vertices[cols[0]] = Vertex(name=cols[0])
            if cols[1] not in vertices:
                vertices[cols[1]] = Vertex(name=cols[1])
            u = vertices[cols[0]]
            v = vertices[cols[1]]
            G1.add_edge(u, v)
            
    with open(testing_flname) as fl:
        G2 = DiGraph()
        for ln in fl:
            cols = ln.split()
            if cols[0] not in vertices:
                vertices[cols[0]] = Vertex(name=cols[0])
            if cols[1] not in vertices:
                vertices[cols[1]] = Vertex(name=cols[1])
            u = vertices[cols[0]]
            v = vertices[cols[1]]
            G2.add_edge(u, v)

    return G1, G2

def precision(recommendations, testing_set):
    """
    Precision measures the fraction of positive predictions
    were found in the test set (were true positives).

    A precise algorithm rarely makes false positive predictions.
    """
    rec_edges = recommendations.edge_set()
    test_edges = testing_set.edge_set()
    intersection = rec_edges.intersection(test_edges)
    
    if len(rec_edges) == 0:
        return 0.0
    
    return float(len(intersection)) / len(rec_edges)
    
def recall(recommendations, testing_set):
    """
    Recall measures the fraction of test set that
    were predicted positively.
    """
    rec_edges = recommendations.edge_set()
    test_edges = testing_set.edge_set()
    intersection = rec_edges.intersection(test_edges)
    
    if len(test_edges) == 0:
        return 0.0
    
    return float(len(intersection)) / len(test_edges)

def bfs(G, s):
    """
    Performs a breadth-first search of the graph G, starting at vertex s.
    
    Hints:
     * sys.maxsize can be used in place of the INFTY constant.
     * The Python data structure deque is a double-ended queue. You can
       use q.append() to add the back of the queue, q.popleft() to remove
       items from the front of the queue, and len(q) to check if the queue
       is empty (len(q) == 0).
    """
    Q = deque()
    for vertex in G._edges:
        if not vertex == s:
            vertex.color = "WHITE"
            vertex.pi = None
            vertex.d = sys.maxsize
    s.color = "GRAY"   
    s.d = 0
    s.pi = None
    Q.append(s)

    while Q:
        u = Q.popleft()
        for vertex in G._edges[u]:
            if vertex.color == "WHITE":
                vertex.color = "GRAY"
                vertex.d = u.d + 1
                vertex.pi = u
                Q.append(vertex)
        u.color = "BLACK"
     
def recommend_friends_for_user(G, s, max_depth):
    """
    Performs a breadth-first search of the graph G, starting at vertex s.
    Does not traverse vertices with d > max_depth.
    Returns a list of all vertices encountered.
    
    Hints:
     * sys.maxsize can be used in place of the INFTY constant.
     * The Python data structure deque is a double-ended queue. You can
       use q.append() to add the back of the queue, q.popleft() to remove
       items from the front of the queue, and len(q) to check if the queue
       is empty (len(q) == 0).
    """
    vertices_encountered = []
    Q = deque()
    for vertex in G._edges:
        if not vertex == s:
            vertex.color = "WHITE"
            vertex.pi = None
            vertex.d = sys.maxsize
    s.color = "GRAY"   
    s.d = 0
    s.pi = None
    Q.append(s)

    while Q:
        u = Q.popleft()
        for vertex in G._edges[u]:
            if vertex.color == "WHITE":
                vertex.color = "GRAY"
                vertex.d = u.d + 1
                vertex.pi = u
                if (vertex.d <= max_depth):
                    Q.append(vertex)
                    vertices_encountered.append(vertex)
        u.color = "BLACK"
    return vertices_encountered
    
def recommend_all_friends(G, max_depth):
    """
    Generates recommendations for all users by performing
    a depth-limited breadth-first search for each user.
    
    The resulting recommendations are stored as a DiGraph.
    """
    friend_graph = DiGraph()
    for u in G._edges:
        targets = recommend_friends_for_user(G, u, max_depth)
        for v in targets:
            if not G.edge_exists(v, u):
                friend_graph.add_edge(u, v)
                friend_graph.add_edge(v, u)
    return friend_graph


class DiGraph:
    
    def __init__(self):
        self._edges = {}
        self.num_vertices = 0
        self.num_edges = 0

    def edge_set(self):
        """Loops through all of the edges, and adds the tuples
        of the vertices involved in each edge for each edge to a set.
        
        Returns:
        Set of tuples of vertices.
        
        """
        set_of_edges = set()

        for vertex, edge_destinations  in self._edges.items():
            for edge_destination in edge_destinations:
                set_of_edges.add((vertex, edge_destination))
        
        return set_of_edges
    
    def add_vertex(self, vertex):
        """Adds a vertex to the graph if it doesn't already exist.
        
            Parameters:
            vertex (Vertex or String): The vertex to be added to the graph."""
        if not (self.vertex_exists(vertex)): # adds vertex only if key isn't in dictionary
            self._edges[vertex] = set()
            self.num_vertices = self.num_vertices + 1

    def add_edge(self, v1, v2):
        """Adds an edge between the two passed in vertices.
        
            Parameters:
            v1 (Vertex or string): First vertex.
            v1 (Vertex or string): Second vertex.
            """
        if not self.vertex_exists(v1):
            self.add_vertex(v1)
        if not self.vertex_exists(v2):
            self.add_vertex(v2)
        self._edges[v1].add(self.get_vertex(v2))
        self.num_edges = self.num_edges + 1

    def get_vertex(self, vertex):
        """Gets a unique vertex from the graph. Corresponding to the one passed in.
        
            Paramters:
            vertex (Vertex or string): The vertex to retrieve.

            Returns:
            v (Vertex): If the unique vertex is in the graph.
            Otherwise None if the unique vertex is not in the graph.
            """
        for v in self._edges.keys():
            if v == vertex:
                return v
        return None
    
    def vertex_exists(self, vertex):
        """Determines if a given vertex exists in the graph.

            Parameters:
            vertex (Vertex): The vertex to check.
        
            Returns:
            (bool): Whether the vertex exists in the graph."""
        return vertex in self._edges

    def count_vertices(self):
        """Counts the number of vertices in the graph.
        
            Returns:
            (int): number of vertices in the graph."""
        return self.num_vertices

    def count_edges(self):
        """Counts the number of edges in the graph.
        
            Returns:
            (int): number of edges in the graph."""
        return self.num_edges

    def edge_exists(self, vertex1, vertex2):
        """Checks if an edge exists in the graph between the vertices passed in.
        
            Parameters:
            vertex1 (Vertex) - first vertex
            vertex2 (Vertex) - second vertex
            
            Returns:
            (bool): Whether the edge exists in the graph."""
        if not self.vertex_exists(vertex1):
            return False
        return vertex2 in self._edges[vertex1]

    def get_outgoing_edges(self, vertex):
        """
            Parameters:
            vertex (Vertex): the source vertex.
            Returns (list): the list of edges that have a source of the vertex passed in."""
        return self._edges[vertex]


