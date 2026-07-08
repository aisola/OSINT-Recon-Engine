import argparse
import datetime

import asn_client
import crtsh_client
import dns_resolver
import graph
import reporter
import whois_client


def procesar_modulo(graph: object, nodes: list, relations: list, modulo: str):
    for n in nodes:
        main_graph.add_node(n)
    for r in relations:
        main_graph.add_relation(r.origin_node_id, r.destination_node_id, r.type)
    print(f"Modulo {modulo} procesado con éxito")


parser = argparse.ArgumentParser(
    description="Herramienta para automatizar escaneos OSINT. Busca subdominios, resuelve IPs y grafica."
)
grupo = parser.add_mutually_exclusive_group(required=True)
grupo.add_argument("-d", "--dominio", help="Input de tipo 'Dominio'")
grupo.add_argument("-i", "--ip", help="Input de tipo 'IP'")
grupo.add_argument("-s", "--subdominio", help="Input de tipo 'Subdominio'")

args = parser.parse_args()

main_graph = graph.Graph()

if args.dominio:
    main_node = graph.Node("Dominio", "User Input", "User Input", "Alta", args.dominio)
    main_graph.add_node(main_node)
    nodes, relations = dns_resolver.resolver(main_node)
    procesar_modulo(main_graph, nodes, relations, "dns_resolver")
    nodes, relations = crtsh_client.crtsh(main_node)
    procesar_modulo(main_graph, nodes, relations, "crt.sh")
    nodes, relations = whois_client.whois_client(main_node)
    procesar_modulo(main_graph, nodes, relations, "whois")
elif args.subdominio:
    main_node = graph.Node(
        "Subdominio", "User Input", "User Input", "Alta", args.subdominio
    )
    main_graph.add_node(main_node)
elif args.ip:
    main_node = graph.Node("IP", "User Input", "User Input", "Alta", args.ip)
    main_graph.add_node(main_node)
    nodes, relations = asn_client.asn_lookup(main_node)
    procesar_modulo(main_graph, nodes, relations, "asn_lookup")

main_graph.show_graph()
json_name = (
    f"reporte_{main_node.value}-{datetime.datetime.now().strftime('%Y_%m_%d-%H%M')}"
)
reportStatus = reporter.to_json(main_graph, json_name)
if reportStatus:
    print("Exportado con éxito")
