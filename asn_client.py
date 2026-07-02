import json
import time
from urllib.request import urlopen

from graph import Node, NodeTypeError, Relation


def asn_lookup(node: object) -> tuple[list, list]:

    if node.type != "ip":
        raise NodeTypeError(
            f"El tipo de nodo {node.type} no está soportado por el modulo."
        )

    nodes = []
    relations = []

    url = f"http://ip-api.com/json/{node.value}"

    for intento in range(3):
        try:
            response = urlopen(url, timeout=30)
            break
        except Exception:
            if intento == 2:
                return [], []
            time.sleep(2)

    response = json.loads(response.read())

    as_parts = response["as"].split(" ", 1)

    asn_node = Node("ASN", "asn_lookup", node.nod_id, "Alta", as_parts[0])
    isp_node = Node("ISP", "asn_lookup", node.nod_id, "Alta", response["isp"])
    ip_asn_rel = Relation(node.nod_id, asn_node.nod_id, "PERTENECE_A")
    asn_isp_rel = Relation(asn_node.nod_id, isp_node.nod_id, "PERTENECE_A")

    nodes.append(asn_node)
    nodes.append(isp_node)
    relations.append(ip_asn_rel)
    relations.append(asn_isp_rel)

    return nodes, relations
