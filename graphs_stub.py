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
    pass
        
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
    pass
    
def recommend_all_friends(G, max_depth):
    """
    Generates recommendations for all users by performing
    a depth-limited breadth-first search for each user.
    
    The resulting recommendations are stored as a DiGraph.
    """
    pass