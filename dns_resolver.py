import socket

from graph import Node, Relation

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


def resolver(domain_node) -> tuple[list, list]:
    nodes = []
    relations = []

    try:
        dom_ip = socket.gethostbyname(domain_node.value)
        print(f"El dominio '{domain_node.value}' resuleve a '{dom_ip}'")
        dom_ip_node = Node("IP", "dns", domain_node.nod_id, "Alta", dom_ip)
        dom_ip_rel = Relation(domain_node.nod_id, dom_ip_node.nod_id, "RESUELVE_A")
        nodes.append(dom_ip_node)
        relations.append(dom_ip_rel)
    except socket.gaierror:
        print(f"No se pudo resolver la IP de '{domain_node.value}'\n")
        pass

    for w in wordlist:
        subdomain = f"{w}.{domain_node.value}"

        try:
            sub_ip = socket.gethostbyname(subdomain)
            print(f"Se encontró el subdominio {subdomain} que resuelve a {sub_ip}\n")
            sub_node = Node("Subdominio", "dns", domain_node.nod_id, "Alta", subdomain)
            sub_rel = Relation(domain_node.nod_id, sub_node.nod_id, "TIENE_SUBDOMINIO")
            sub_ip_node = Node("IP", "dns", domain_node.nod_id, "Alta", sub_ip)
            sub_ip_rel = Relation(sub_node.nod_id, sub_ip_node.nod_id, "RESUELVE_A")
            nodes.append(sub_node)
            nodes.append(sub_ip_node)
            relations.append(sub_rel)
            relations.append(sub_ip_rel)
        except socket.gaierror:
            print(f"El subdominio {subdomain} no existe.\n")
            continue

    return nodes, relations
