import json
import socket
import time
from urllib.request import urlopen

from graph import Node, NodeTypeError, Relation

socket.setdefaulttimeout(30)


def crtsh(node) -> tuple[list, list]:

    if node.type != "dominio":
        raise NodeTypeError(
            f"El tipo de nodo {node.type} no está soportado por el modulo."
        )

    nodes = []
    relations = []

    url = f"https://crt.sh/?q=%25.{node.value}&output=json"

    for intento in range(3):
        try:
            response = urlopen(url, timeout=30)
            break
        except Exception:
            if intento == 2:
                return [], []
            time.sleep(2)

    data = json.loads(response.read())

    for e in data:
        names = e["name_value"].split("\n")
        is_domain = False
        emails = []
        subdomains = []
        for n in names:
            if n.strip().endswith("." + node.value) or n.strip().endswith(
                "@" + node.value
            ):
                is_domain = True
                if n.strip().endswith("." + node.value):
                    subdomains.append(n)
                elif n.strip().endswith("@" + node.value):
                    emails.append(n)
        if not is_domain:
            continue
        e["subdomains"] = subdomains
        e["emails"] = emails
        crt_node = Node("Certificado", "crt.sh", node.nod_id, "Media", str(e["id"]), e)
        for s in subdomains:
            try:
                s = s.removeprefix("*.")
                sub_ip = socket.gethostbyname(s)
                print(f"Se encontró el subdominio {s} que resuelve a {sub_ip}\n")
                sub_node = Node("Subdominio", "crt.sh", node.nod_id, "Media", s)
                sub_rel = Relation(node.nod_id, sub_node.nod_id, "TIENE_SUBDOMINIO")
                sub_ip_node = Node("IP", "crt.sh", node.nod_id, "Media", sub_ip)
                sub_ip_rel = Relation(sub_node.nod_id, sub_ip_node.nod_id, "RESUELVE_A")
                sub_crt_rel = Relation(crt_node.nod_id, sub_node.nod_id, "EMITIDO_PARA")
                nodes.append(sub_node)
                nodes.append(sub_ip_node)
                relations.append(sub_rel)
                relations.append(sub_ip_rel)
                relations.append(sub_crt_rel)
            except socket.gaierror:
                print(f"El subdominio {s} no existe.\n")
                continue
        for em in emails:
            em_node = Node("Email", "crt.sh", node.nod_id, "Media", em)
            em_crt_relation = Relation(em_node.nod_id, crt_node.nod_id, "APARECE_EN")
            nodes.append(em_node)
            relations.append(em_crt_relation)
    return nodes, relations
