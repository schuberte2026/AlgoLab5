import unittest

import random

from graphs import bfs
from graphs import DiGraph
from graphs import recommend_all_friends
from graphs import recommend_friends_for_user
from graphs import Vertex

def extract_bfs_tree(G):
    """
    Creates a new graph containing the tree
    generated from a BFS of the input graph G.
    """
    t = DiGraph()
    
    for v in G._edges.keys():
        if v.pi != None:
            t.add_edge(v.pi, v)
            
    return t
    
def generate_complete_graph(n_vertices):
    """
    Generates a complete graph (all vertices are connected to each other).
    """
    g = DiGraph()
    
    vertices = [Vertex(name=i) for i in range(n_vertices)]
    for u in vertices:
        for v in vertices:
            if u != v:
                g.add_edge(u, v)

    return g, vertices
    
def generate_linear_graph(n_vertices, circular=False):
    """
    Generates a linear graph where each vertex is connected to two neighbors.
    (Think of a doubly-linked list.)
    """
    g = DiGraph()
    
    vertices = [Vertex(name=i) for i in range(n_vertices)]
    for i in range(n_vertices - 1):
        g.add_edge(vertices[i], vertices[i+1])
        g.add_edge(vertices[i+1], vertices[i])
        
    if circular:
        g.add_edge(vertices[0], vertices[n_vertices - 1])
        g.add_edge(vertices[n_vertices - 1], vertices[0])
        
    return g, vertices
    
class TestRecommendationAllFriends(unittest.TestCase):
    def test_linear_graph5(self):
        """
        Tests friend recommendations on a complete graph
        with 5 vertices and max_depth 2. Every vertex
        should be connected to every other vetex in the
        result.
        """
        
        g, vertices = generate_linear_graph(5, circular=True)
        f = recommend_all_friends(g, 2)
        
        for i in range(5):
            u = vertices[i]
            v = vertices[(i+2) % 5]
            self.assertTrue(f.edge_exists(u, v))
            self.assertTrue(f.edge_exists(v, u))
        
        
    
class TestRecommendationsForUser(unittest.TestCase):
    def test_complete4_d1(self):
        """
        Tests friends on a complete graph with 4 vertices.
        max_depth = 1
        """
        
        g, vertices = generate_complete_graph(4)

        s = vertices[0]
        max_depth = 1
        recommendations = recommend_friends_for_user(g, s, max_depth)
        
        for v in vertices:
            self.assertEqual(v.color, "BLACK")
            
        self.assertEqual(s.pi, None)
        self.assertEqual(s.d, 0)
        for v in vertices[1:]:
            self.assertEqual(v.pi, s)
            self.assertEqual(v.d, 1)
        
        # recommendations do not include source vertex
        self.assertEqual(len(recommendations), 3)
            
        t = extract_bfs_tree(g)
        self.assertEqual(t.count_vertices(), 4)
        self.assertEqual(t.count_edges(), 3)
        self.assertEqual(len(t.get_outgoing_edges(s)), 3)
        
    def test_complete4_d0(self):
        """
        Tests friends on a complete graph with 4 vertices.
        max_depth = 0
        """
        
        g, vertices = generate_complete_graph(4)
            
        s = vertices[0]
        max_depth = 0
        recommendations = recommend_friends_for_user(g, s, max_depth)
        
        self.assertEqual(s.pi, None)
        self.assertEqual(s.d, 0)
        self.assertEqual(s.color, "BLACK")
        for v in vertices[1:]:
            self.assertEqual(v.pi, s)
            self.assertEqual(v.d, 1)
            self.assertEqual(v.color, "GRAY")
        
        # recommendations do not include source vertex
        self.assertEqual(len(recommendations), 0)
        
    def test_bfs_linear5(self):
        """
        Tests on a linear graph with 5 vertices and
        various max depths.
        """
        
        g, vertices = generate_linear_graph(5, circular=False)
        
        s = vertices[0]
        
        for max_depth in range(4):
            recommendations = recommend_friends_for_user(g, s, max_depth)
        
            self.assertEqual(len(recommendations), max_depth)

class TestBFS(unittest.TestCase):
    def test_bfs_complete4(self):
        """
        Tests BFS on a complete graph with 4 vertices.
        """
        
        g, vertices = generate_complete_graph(4)
            
        s = vertices[0]        
        bfs(g, s)
        
        for v in vertices:
            self.assertEqual(v.color, "BLACK")
            
        self.assertEqual(s.pi, None)
        self.assertEqual(s.d, 0)
        for v in vertices[1:]:
            self.assertEqual(v.pi, s)
            self.assertEqual(v.d, 1)
            
        t = extract_bfs_tree(g)
        self.assertEqual(t.count_vertices(), 4)
        self.assertEqual(t.count_edges(), 3)
        self.assertEqual(len(t.get_outgoing_edges(s)), 3)
        
    def test_bfs_linear5(self):
        """
        Tests BFS on a linear graph with 5 vertices.
        """
        
        g, vertices = generate_linear_graph(5, circular=False)
        
        s = vertices[0]
        bfs(g, s)
        
        for v in vertices:
            self.assertEqual(v.color, "BLACK")
        
        t = extract_bfs_tree(g)
        self.assertEqual(t.count_edges(), g.count_edges() / 2)
        self.assertEqual(t.count_vertices(), g.count_vertices())

class TestGraph(unittest.TestCase):
    def test_init(self):
        g = DiGraph()
        
        self.assertIsInstance(g._edges, dict)
        
    def test_add_vertex(self):
        g = DiGraph()
        
        g.add_vertex("a")
        
        self.assertIn("a", g._edges)
        self.assertIsInstance(g._edges["a"], set)
        self.assertTrue(g.vertex_exists("a"))
        self.assertEqual(g.count_vertices(), 1)
        self.assertEqual(g.count_edges(), 0)
        
        g.add_vertex("b")
        
        self.assertIn("b", g._edges)
        self.assertIsInstance(g._edges["b"], set)
        self.assertTrue(g.vertex_exists("b"))
        self.assertEqual(g.count_vertices(), 2)
        self.assertEqual(g.count_edges(), 0)
        
    def test_add_edge(self):
        g = DiGraph()
        
        g.add_edge("a", "b")
        
        self.assertIn("a", g._edges)
        self.assertIn("b", g._edges)
        self.assertIsInstance(g._edges["a"], set)
        self.assertIsInstance(g._edges["b"], set)
        self.assertIn("b", g._edges["a"])
        self.assertNotIn("a", g._edges["b"])
        self.assertTrue(g.vertex_exists("a"))
        self.assertTrue(g.vertex_exists("b"))
        self.assertTrue(g.edge_exists("a", "b"))
        self.assertFalse(g.edge_exists("b", "a"))
        self.assertEqual(g.count_vertices(), 2)
        self.assertEqual(g.count_edges(), 1)
        
        # check that re-adding a vertex
        # doesn't erase edge information
        g.add_vertex("a")
        self.assertIn("b", g._edges["a"])
        self.assertEqual(g.count_vertices(), 2)
        self.assertEqual(g.count_edges(), 1)
        
        # validate that edges are directed
        g.add_edge("b", "a")
        self.assertIn("a", g._edges["b"])
        self.assertEqual(g.count_vertices(), 2)
        self.assertEqual(g.count_edges(), 2)
        self.assertTrue(g.edge_exists("a", "b"))
        self.assertTrue(g.edge_exists("b", "a"))
        
        self.assertFalse(g.edge_exists("b", "c"))
        self.assertFalse(g.edge_exists("c", "d"))
        
        neighbors_a = g.get_outgoing_edges("a")
        self.assertSetEqual(neighbors_a, set(["b"]))
        
    def test_vertex_exists(self):
        g = DiGraph()
        
        g.add_vertex("a")
        
        self.assertTrue(g.vertex_exists("a"))
        self.assertFalse(g.vertex_exists("none_existent"))


if __name__ == "__main__":
    unittest.main()
