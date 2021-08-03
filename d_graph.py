# Course: CS261 - Data Structures
# Author:
# Assignment:
# Description:

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a new vertex to the graph.
        Name of the vertex will be the next available int (starting from 0)
        Vertices are stored in an adjacency matrix.
        """
        vertices = len(self.adj_matrix)
        new_vertex = []

        for vertex in range(vertices + 1):  # +1 to include itself
            new_vertex.append(0)

        for u in self.adj_matrix:
            u.append(0)                     # Add a cell to all other vertices for the new vertex

        self.adj_matrix.append(new_vertex)  # Add the new vertex to the list
        self.v_count += 1

        return vertices + 1                 # Total amount of vertices in graph

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds a new edge to the graph from src, to dst, with the given weight.
        If either vertex does not exist, the weight is not a positive integer,
        or src == dst, the method does nothing.
        If the edge already exists, this method updates its weight.
        """
        if weight < 1 or src == dst:
            return
        elif len(self.adj_matrix) <= src or \
             len(self.adj_matrix) <= dst:    # Check to see if src or dst are not in the graph
            return

        src_list = self.adj_matrix[src]      # Get the list of edges for the source

        src_list[dst] = weight               # Add the weight to the matrix

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes the edge from src, to dst.
        If either vertex does not exist,
        or the edge does not exist, the method does nothing.
        """

        if len(self.adj_matrix) <= src or \
           len(self.adj_matrix) <= dst:  # Check to see if src or dst are not in the graph
            return

        src_list = self.adj_matrix[src]  # Get the list of edges for the source

        src_list[dst] = 0  # 0 is no edge, thus remove the edge

    def get_vertices(self) -> []:
        """
        Returns a list of the vertices in the graph in ascending order.
        """
        return [x for x in range(len(self.adj_matrix))]

    def get_edges(self) -> []:
        """
        Returns a list of edges in the graph.
        Each edge is a tuple of two incident vertices and the weight.
        The first item is the source of the edge, the second, the destination,
        and the third, the weight.
        List is ordered by vertex value in ascending order.
        """
        edges = []
        v_i = 0
        for v in self.adj_matrix:
            u_i = 0
            for edge in v:
                if edge != 0:
                    edges.append((v_i, u_i, edge))
                u_i += 1
            v_i += 1

        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        TODO: Write this implementation
        """
        if len(path) == 0:
            return True

        if path[0] not in self.get_vertices():  # Ensure the first vertex is valid
            return False

        valid_edges = self.get_edges()
        cur_v = None

    def dfs(self, v_start, v_end=None) -> []:
        """
        TODO: Write this implementation
        """
        pass

    def bfs(self, v_start, v_end=None) -> []:
        """
        TODO: Write this implementation
        """
        pass

    def has_cycle(self):
        """
        TODO: Write this implementation
        """
        pass

    def dijkstra(self, src: int) -> []:
        """
        TODO: Write this implementation
        """
        pass


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')

    #
    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    # for path in test_cases:
    #     print(path, g.is_valid_path(path))
    #
    #
    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # for start in range(5):
    #     print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')
    #
    #
    # print("\nPDF - method has_cycle() example 1")
    # print("----------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    #
    # edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    # for src, dst in edges_to_remove:
    #     g.remove_edge(src, dst)
    #     print(g.get_edges(), g.has_cycle(), sep='\n')
    #
    # edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    # for src, dst in edges_to_add:
    #     g.add_edge(src, dst)
    #     print(g.get_edges(), g.has_cycle(), sep='\n')
    # print('\n', g)
    #
    #
    # print("\nPDF - dijkstra() example 1")
    # print("--------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # for i in range(5):
    #     print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    # g.remove_edge(4, 3)
    # print('\n', g)
    # for i in range(5):
    #     print(f'DIJKSTRA {i} {g.dijkstra(i)}')
