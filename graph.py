import datetime as dt


class NodeTypeError(Exception):
    pass


class Node:
    def __init__(
        self,
        type: str,
        source: str,
        origin_node_id: str,
        trust: str,
        value: str,
        extra_data=None,
    ):
        self.type = type.strip().lower()
        self.source = source
        self.origin_node_id = origin_node_id
        self.trust = trust
        self.value = value
        self.extra_data = extra_data
        self.nod_id = type.strip().lower() + ":" + value.strip().lower()
        self.timestamp = dt.datetime.now().strftime("%Y_%m_%d-%H_%M")
        self.node_relations = []


class Relation:
    def __init__(self, origin_node_id: str, destination_node_id: str, type: str):
        self.origin_node_id = origin_node_id
        self.destination_node_id = destination_node_id
        self.type = type


class Graph:
    def __init__(self):
        self.nodes = {}
        self.relations = []

    def add_node(self, Node):
        self.nodes[Node.nod_id] = Node

    def add_relation(self, origin_node_id, destination_node_id, type):
        if origin_node_id in self.nodes and destination_node_id in self.nodes:
            relation = Relation(origin_node_id, destination_node_id, type)
            self.relations.append(relation)
            self.nodes[origin_node_id].node_relations.append(relation)
            self.nodes[destination_node_id].node_relations.append(relation)
        else:
            print(f"Los nodos {origin_node_id} y/o {destination_node_id} no existen.")

    def show_graph(self):
        shown_relations = []
        for n in self.nodes:
            for r in self.nodes[n].node_relations:
                if r not in shown_relations:
                    response = (
                        self.nodes[r.origin_node_id].value
                        + " "
                        + r.type
                        + " "
                        + self.nodes[r.destination_node_id].value
                    )
                    print(response)
                    shown_relations.append(r)
