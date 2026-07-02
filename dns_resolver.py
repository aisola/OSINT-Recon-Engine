import socket

from graph import Node, NodeTypeError, Relation

wordlist = [
    "www",
    "mail",
    "api",
    "admin",
    "ftp",
    "dev",
    "blog",
    "cdn",
    "mail2",
    "ns1",
    "ns2",
    "vpn",
    "test",
    "staging",
    "backup",
]


def resolver(node) -> tuple[list, list]:

    if node.type != "dominio":
        raise NodeTypeError(
            f"El tipo de nodo {node.type} no está soportado por el modulo."
        )

    nodes = []
    relations = []

    try:
        dom_ip = socket.gethostbyname(node.value)
        print(f"El dominio '{node.value}' resuleve a '{dom_ip}'")
        dom_ip_node = Node("IP", "dns", node.nod_id, "Alta", dom_ip)
        dom_ip_rel = Relation(node.nod_id, dom_ip_node.nod_id, "RESUELVE_A")
        nodes.append(dom_ip_node)
        relations.append(dom_ip_rel)
    except socket.gaierror:
        print(f"No se pudo resolver la IP de '{node.value}'\n")
        pass

    for w in wordlist:
        subdomain = f"{w}.{node.value}"

        try:
            sub_ip = socket.gethostbyname(subdomain)
            print(f"Se encontró el subdominio {subdomain} que resuelve a {sub_ip}\n")
            sub_node = Node("Subdominio", "dns", node.nod_id, "Alta", subdomain)
            sub_rel = Relation(node.nod_id, sub_node.nod_id, "TIENE_SUBDOMINIO")
            sub_ip_node = Node("IP", "dns", node.nod_id, "Alta", sub_ip)
            sub_ip_rel = Relation(sub_node.nod_id, sub_ip_node.nod_id, "RESUELVE_A")
            nodes.append(sub_node)
            nodes.append(sub_ip_node)
            relations.append(sub_rel)
            relations.append(sub_ip_rel)
        except socket.gaierror:
            print(f"El subdominio {subdomain} no existe.\n")
            continue

    return nodes, relations
