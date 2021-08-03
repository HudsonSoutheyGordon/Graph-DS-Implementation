# Course: 
# Author: 
# Assignment: 
# Description:

from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Adds a new vertex to the graph. Name can be any string.
        If a node by the same name already exists in the graph,
        this method does nothing.
        """
        if v in self.adj_list:      # Vertex of this name already exists
            return

        self.adj_list[v] = []

    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph. If either/both vertices do not
        exist, this will first create them.
        If the edge already exists, or if u and v refer to the same vertex
        this method does nothing.
        """
        if u == v:                  # Loop cannot exist
            return

        if u not in self.adj_list:  # If either vertex doesn't exist, create it.
            self.add_vertex(u)
        if v not in self.adj_list:
            self.add_vertex(v)

        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)  # Add the relationships to our dictionary.
        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph. If either/both vertices do not exist,
        or there is no edge between them, this method does nothing.
        """
        if u == v:                  # Loop cannot exist
            return

        if u not in self.adj_list or v not in self.adj_list:  # If either vertex doesn't exist, return.
            return
        elif v not in self.adj_list[u] or u not in self.adj_list[v]:
            return

        self.adj_list[u].remove(v)  # Add the relationships to our dictionary.
        self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges.
        """
        if v not in self.adj_list:
            return

        # Since our graph is undirected, any vertex incident to v
        #   will be included in v's dictionary value.
        #   Thus we take each vertex from this list and remove v
        #   from their incident vertex list.
        for u in self.adj_list[v]:
            self.adj_list[u].remove(v)

        del self.adj_list[v]            # Remove v

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        return list(self.adj_list.keys())

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edges = []

        # Iterate through all edges
        # Each edge is to be a tuple (u, v)
        # Each tuple we make in alphabetical order, because the graph
        #   is undirected. Thus (u, v) is equivalent to (v, u)
        #   Alphabetized will make it easier for us to check for dupes.
        for key in self.adj_list:
            for vertex in self.adj_list[key]:
                if key < vertex:
                    edge = (key, vertex)
                else:
                    edge = (vertex, key)

                if edge not in edges:
                    edges.append(edge)

        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise.
        """
        if len(path) == 0:  # Empty path is valid
            return True

        if path[0] not in self.get_vertices():  # Ensure the first vertex is valid
            return False

        valid_edges = self.get_edges()
        cur_v = None

        for u in path:
            if cur_v is None:   # Assign our start point and continue
                cur_v = u
                continue

            # Our edges are paired in alphabetical order when added
            # Thus to test the edge's validity, it must also be paired
            # in alphabetical order.
            # Again, this is irrelevant to an undirected graph.

            if u < cur_v:
                edge = (u, cur_v)
            else:
                edge = (cur_v, u)

            if edge not in valid_edges:
                return False

            cur_v = u

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        If the starting vertex is not in the list, it will return an empty list.
        If the ending vertex is not in the list, it performs the DFS
        as if the end point is None.
        """
        if v_start not in self.get_vertices():
            return []

        v_visited = []
        stack = deque()

        stack.append(v_start)

        while len(stack) != 0:
            v = stack.pop()
            if v == v_end:
                v_visited.append(v)
                return v_visited

            if v not in v_visited:      # If v hasn't been visited, push it to the stack, and
                v_visited.append(v)     #    then push it's neighbours too (in alphabetical order)
                adjacent = self.adj_list[v]
                adjacent.sort()
                adjacent = adjacent[::-1]       # Ensure we explore in alphabetical order
                for u in adjacent:
                    stack.append(u)

        return v_visited


    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        If the starting vertex is not in the list, it will return an empty list.
        If the ending vertex is not in the list, it performs the BFS
        as if the end point is None.
        """
        if v_start not in self.get_vertices():
            return []

        v_visited = []
        queue = deque()

        queue.append(v_start)

        while len(queue) != 0:
            v = queue.popleft()
            if v == v_end:
                v_visited.append(v)
                return v_visited

            if v not in v_visited:      # If v hasn't been visited, push it to the stack, and
                v_visited.append(v)     #    then push it's neighbours too (in alphabetical order)
                adjacent = self.adj_list[v]
                adjacent.sort()         # Ensure we explore in alphabetical order
                for u in adjacent:
                    if u not in v_visited:
                        queue.append(u)

        return v_visited
        

    def count_connected_components(self):
        """
        Return number of connected components in the graph.
        """
        v_unvisited = self.get_vertices()   # Consider all vertices unvisited
        components = 0

        while len(v_unvisited) > 0:     # While we still have vertices to visit
            visited = self.dfs(v_unvisited[0])  # Perform a DFS on the next vertex
            for v in visited:
                v_unvisited.remove(v)   # Remove all vertices visited from the DFS
            components += 1

        return components

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
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
            has_cycle, visited = self.mod_bfs(v_unvisited[0])
            if has_cycle:
                return True
            for v in visited:
                v_unvisited.remove(v)



        return False


    def mod_bfs(self, v_start):
        """
        Helper method for has_cycle.
        Modified BFS which returns both the paths visited, but also if the
        path we checked contained a cycle.
        """
        v_visited = []
        queue = deque()
        prev_q = deque()        # Maintain a queue, so we can track v's first ancestor

        queue.append(v_start)
        prev_val = None

        while len(queue) != 0:
            v = queue.popleft()
            if len(prev_q) > 0:
                prev_val = prev_q.popleft()

            if v not in v_visited:
                v_visited.append(v)
                adjacent = list(self.adj_list[v])
                if prev_val is not None and prev_val in adjacent:
                    adjacent.remove(prev_val)   # Remove the first ancestor from the list
                adjacent.sort()
                for u in adjacent:
                    if u not in v_visited:
                        queue.append(u)
                        prev_q.append(v)
                    else:                       # If an adjacent node has been visited (and is not the ancestor)
                        return True, None       #   Then we have found a cycle


        return False, v_visited



if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
