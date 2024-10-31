# import numpy as np
from what_not_how.model_data import ModelGroup, Process, DataObject, DataIdentifier


class Node:
    def __init__(self):
        self.edges_in = []
        self.edges_out = []
        self.rank = None
        self.flag = False
        self.name = None


class Edge:
    def __init__(self, tail, head):
        self.tail = tail
        self.head = head
        self.flag = False


class DiGraph:
    def __init__(self, proc_list: list[Process], data_list: list[DataObject]):
        self.nodes = []
        self.edges = []
        self.connections = []
        self.x = []
        self.build(proc_list, data_list)

    def build(self, proc_list: list[Process], data_list: list[DataObject]):
        max_pid = max([x.uid for x in proc_list])
        max_did = max([x.uid for x in data_list])
        n = max([max_pid, max_did]) + 1
        for i in range(n):
            row = [0 for _ in range(n)]
            self.connections.append(row)
            self.nodes.append(Node())

        for dat in data_list:
            self.nodes[dat.uid].name = dat.name

        for proc in proc_list:
            self.nodes[proc.uid].name = proc.name
            p_id = proc.uid
            for d in proc.inputs:
                d_id = d.identifier_id
                self.connect(d_id, p_id)

            for d in proc.outputs:
                d_id = d.identifier_id
                self.connect(p_id, d_id)

    def connect(self, tail: int, head: int):
        self.connections[tail][head] = 1
        edge = Edge(self.nodes[tail], self.nodes[head])
        self.nodes[tail].edges_out.append(edge)
        self.nodes[head].edges_in.append(edge)
        self.edges.append(edge)

    def primary_inputs(self) -> list[int]:
        input_list = []
        n = len(self.connections)
        for i in range(n):
            is_input = True
            for j in range(n):
                if self.connections[j][i] > 0:
                    is_input = False
                    break
            if is_input:
                input_list.append(i)
        return input_list

    def primary_outputs(self) -> list[int]:
        output_list = []
        n = len(self.connections)
        for i in range(n):
            is_output = True
            for j in range(n):
                if self.connections[i][j] > 0:
                    is_output= False
                    break
            if is_output:
                output_list.append(i)
        return output_list

    def initial_ranking(self):
        finished = False
        iters = 0
        while not finished:
            iters += 1
            finished = True
            for node in self.nodes:
                if node.rank is None:
                    finished = False
                    done = True
                    rank = 0
                    for edge in node.edges_in:
                        if edge.tail.rank is None:
                            done = False
                            break
                        elif edge.tail.rank > rank:
                            rank = edge.tail.rank
                    if done:
                        node.rank = rank + 1
        print(f"iters: {iters}")

    def print_ranks(self):
        max_rank = max([n.rank for n in self.nodes])
        ranks = [[] for _ in range(max_rank)]
        for node in self.nodes:
            ranks[node.rank - 1].append(node.name)

        for r, layer in enumerate(ranks):
            print(f"rank: {r+1}: " + ", ".join(layer))
