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
        if weight < 1 or src == dst or src < 0 or dst < 0:
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
        if src < 0 or dst < 0:
            return
        elif len(self.adj_matrix) <= src or \
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
        This method takes a list of vertices.
        It then checks to ensure the path is valid by checking that
        all vertices exist, and if so, checking that each edge exists.
        """
        if len(path) == 0:  # Empty path is valid
            return True

        if path[0] < 0 or path[0] > len(self.get_vertices()):  # Ensure the first vertex is valid
            return False

        v = None

        for u in path:
            if v is None:   # Assign our start point and continue
                v = u
                continue

            if u < 0 or u > len(self.get_vertices()):   # Ensure u is a valid vertex
                return False
            elif self.adj_matrix[v][u] == 0:            # If the edge value is 0, there is no edge
                return False                            #   Thus the path is invalid
            v = u

        return True


    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in ascending numerical order
        If the starting vertex is not in the list, it will return an empty list.
        If the ending vertex is not in the list, it performs the DFS
        as if the end point is None.
        """
        if v_start not in self.get_vertices():  # Check to see if the first vertex is in the graph
            return []

        v_visited = []
        stack = deque()

        stack.append(v_start)

        while len(stack) != 0:
            v = stack.pop()
            if v == v_end:
                v_visited.append(v)
                return v_visited

            if v not in v_visited:  # If v hasn't been visited, push it to the stack, and
                v_visited.append(v)  # then push it's neighbours too (in ascending order)
                adjacent = self.adj_matrix[v]
                # Edges are represented as weight values, but we care about the destination vertex.
                # So we convert our list to be one of the connected destinations rather than weights.
                adjacent_vs = [x for x in range(len(adjacent)) if adjacent[x] != 0]
                adjacent_vs.sort()
                adjacent_vs = adjacent_vs[::-1]  # Ensure we explore in ascending numerical order
                for u in adjacent_vs:
                    stack.append(u)

        return v_visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        If the starting vertex is not in the list, it will return an empty list.
        If the ending vertex is not in the list, it performs the BFS
        as if the end point is None.
        """
        if v_start not in self.get_vertices():  # Check to see if the first vertex is in the graph
            return []

        v_visited = []
        queue = deque()

        queue.append(v_start)

        while len(queue) != 0:
            v = queue.popleft()
            if v == v_end:
                v_visited.append(v)
                return v_visited

            if v not in v_visited:  # If v hasn't been visited, push it to the stack, and
                v_visited.append(v)  # then push it's neighbours too (in ascending order)
                adjacent = self.adj_matrix[v]
                # Edges are represented as weight values, but we care about the destination vertex.
                # So we convert our list to be one of the connected destinations rather than weights.
                adjacent_vs = [x for x in range(len(adjacent)) if adjacent[x] != 0]
                adjacent_vs.sort()
                for u in adjacent_vs:
                    if u not in v_visited:
                        queue.append(u)

        return v_visited

    def has_cycle(self):
        """
        TODO: Write this implementation
        """
        v_unvisited = self.get_vertices()
        vertices = self.get_vertices()

        if len(vertices) < 3:
            return False

        # When checking a graph for cycles, we need to check
        # all components of the graph. Thus, we ensure we visit each
        # vertex through our BFS, by doing a BFS on each component.
        # If any component has a cycle, then the this method returns true

        while len(v_unvisited) > 0:
            has_cycle, visited = self.mod_dfs(v_unvisited[0])
            if has_cycle:
                return True
            for v in visited:
                if v in v_unvisited:
                    v_unvisited.remove(v)



        return False


    def mod_dfs(self, v_start):
        """
        Helper method for has_cycle.
        Modified DFS which returns both the paths visited, but also if the
        path we checked contained a cycle.
        """
        if len(self.adj_matrix) < 3:
            return False

        v_start = v_start

        v_visited = []
        stack = deque()
        current_traversal = deque()
        backTracking = False

        stack.append((v_start, None))
        current_traversal.append(v_start)

        while len(stack) != 0:
            # if not backTracking:
            #     v = stack.pop()
            #     current_traversal.append(v)
            # else:
            #     v = current_traversal[-1]
            #     if v in v_visited:
            #         v_visited.remove(v)
            tup = stack.pop()
            v = tup[0]
            predecessor = tup[1]
            if backTracking:
                while current_traversal[-1] != predecessor:
                    current_traversal.pop()

            if v not in current_traversal:
                current_traversal.append(v)

            if v not in v_visited:
                v_visited.append(v)
                adjacent = self.adj_matrix[v]
                # Edges are represented as weight values, but we care about the destination vertex.
                # So we convert our list to be one of the connected destinations rather than weights.
                adjacent_vs = [x for x in range(len(adjacent)) if adjacent[x] != 0]
                adjacent_vs.sort()
                adjacent_vs = adjacent_vs[::-1]  # Ensure we explore in ascending numerical order
                if len(adjacent_vs) != 0:
                    backTracking = False
                    for u in adjacent_vs:
                        if u in current_traversal:
                            return True, None
                        # if u not in v_visited and u not in stack:
                        #     stack.append(u)
                        stack.append((u, v))
                        # elif u in stack:
                        #     current_traversal.pop()
                        #     backTracking = True
                        # Not sure I can just do the above.
                        # Do we just put it in the stack twice? I think maybe

                else:
                    current_traversal.pop()
                    backTracking = True


        return False, v_visited

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

    # print("\nMethod Remove Edge custom Test")
    # print("----------------------------------")
    # g = DirectedGraph()
    # edges = [(3, 1, 7), (7, 1, 5), (8, 2, 10), (6, 4, 10), (9, 10, 11),
    #          (11, 10, 5), (12, 11, 20), (5, 12, 9)]
    #
    # g = DirectedGraph(edges)
    # print(g)
    # g.remove_edge(5, -1)


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))
    #
    #
    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0, 99)]
    for src, dst, *weight in edges_to_add:
        g.add_edge(src, dst, *weight)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    print("\nPDF - CUSTOM has_cycle())")
    print("----------------------------------")
    edges = [(1, 0, 10), (1, 3, 10), (1, 7, 10), (3, 7, 10), (4, 5, 10), (5, 11, 10),
             (5, 1, 10), (8, 4, 10), (8, 5, 10), (10, 7, 10), (10, 5, 10),
             (11, 0, 10), (11, 3, 10)]

    g = DirectedGraph(edges)
    print(g.has_cycle())
    print('\n', g)


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
