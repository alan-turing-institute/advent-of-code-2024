

import numpy as np
from collections import deque
import copy
from tqdm import tqdm
import itertools

class Graph:
    def __init__(self, nodes, paths):
        self.nodes = nodes
        self.paths = paths
        n = len(self.nodes)
        self.adj = np.zeros((n, n), dtype=int)
        for i1, n1 in enumerate(self.nodes):
            for i2, n2 in enumerate(self.nodes):
                if n1 + n2 in self.paths:
                    self.adj[i1, i2] = 1
                    self.adj[i2, i1] = 1

        self.get_all_paths()
        
    def get_all_paths(self):
        self.all_paths = {}
        for i1, n1 in enumerate(self.nodes):
            for i2, n2 in enumerate(self.nodes):
                if n1 + n2 in self.paths:
                    self.all_paths[n1 + n2] = [self.paths[n1 + n2]]
                else:  # get ALL shortest paths
                    self.all_paths[n1 + n2] = self.get_shortest_paths(i1, i2)

    def get_shortest_paths(self, i1, i2):
        '''BFS'''
        shortest_paths = []
        n_nod = len(self.nodes)

        dist = [np.inf] * n_nod
        dist[i1] = 0

        queue = deque([(i1, [i1])])

        while len(queue) > 0:
            node, p = queue.popleft()
            for neigh in np.where(self.adj[node, :])[0]:
                if neigh == i2:
                    if dist[node] + 1 <= dist[neigh]:
                        shortest_paths.append((neigh, p + [neigh]))
                        dist[neigh] = dist[node] + 1
                elif node == i2:
                    pass
                elif dist[neigh] >= dist[node] + 1:
                    dist[neigh] = dist[node] + 1
                    if len(p) > dist[i2]:
                        pass
                    else:
                        queue.append((neigh, p + [neigh]))

        shortest_paths = [x[1] for x in shortest_paths]
        new_paths = []
        for p in shortest_paths:
            p_new = []
            for ii in range(len(p) - 1):
                tmp = self.nodes[p[ii]] + self.nodes[p[ii + 1]]
                p_new.append(self.paths[tmp])
            p_new = ''.join(p_new)
            new_paths.append(p_new)
        return new_paths

    def get_n_unique(self, s):
        # Remove consecutive duplicates and count unique groups
        unique_groups = ''.join(char for i, char in enumerate(s) if i == 0 or s[i] != s[i-1])
        return len(set(unique_groups)) == len(unique_groups)
    
class KeyPad(Graph):
    def __init__(self):

        self.paths = {}
        for hor in ['12', '23', '45', '56', '78', '89', '0A']:
            self.paths[hor] = '>'
            self.paths[hor[::-1]] = '<'

        for ver in ['41', '52', '63', '74', '85', '96', '20', '3A']:
            self.paths[ver] = 'v'
            self.paths[ver[::-1]] = '^'

        super().__init__(nodes=list('0123456789A'), paths=self.paths)

        ## get rid of all inefficient paths (<v< instead of <<v or v<<)
        for k, v in self.all_paths.items():
            self.all_paths[k] = [p for p in v if self.get_n_unique(p)]

class Direct(Graph):
    def __init__(self, shortcuts=False):

        self.paths = {}
        for hor in ['^A', '<v', 'v>']:
            self.paths[hor] = '>'
            self.paths[hor[::-1]] = '<'

        for ver in ['^v', 'A>']:
            self.paths[ver] = 'v'
            self.paths[ver[::-1]] = '^'

        super().__init__(nodes=list('<v>^A'), paths=self.paths)
        
        if shortcuts:
        # ## get rid of inefficient paths:
            self.all_paths['<A'] = ['^>>']
            self.all_paths['A<'] = ['v<<']
            self.all_paths['Av'] = ['v<']
            self.all_paths['^>'] = ['>v']
            self.all_paths['>^'] = ['^<']
            self.all_paths['vA'] = ['>^']


def insert_a_presses(c_paths):
    ''' ['>>', '^v>'] becomes ['>>', 'A', '^v>', 'A']'''
    result = [] 
    for c in c_paths:
        tmp = []
        for action in c:
            tmp.append(action)
            tmp.append('A')

        result.append(''.join(tmp))
    
    return result

def get_first_keypad_problems(c):
    ## c is eg 879A
    kp = KeyPad()

    # num_c = int(''.join([x for x in c if x != 'A']))
    c_paths = []
    c = 'A' + c
    for ii in range(len(c) - 1):
        c_combo = c[ii] + c[ii + 1]
        c_paths.append(kp.all_paths[c_combo])

    c_paths = list(itertools.product(*c_paths))  # (path between A and 1st, path between 1st and 2nd, ..)
    c_paths = insert_a_presses(c_paths)
    return c_paths