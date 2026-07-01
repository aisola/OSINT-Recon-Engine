import argparse
import datetime

import crtsh_client
import dns_resolver
import graph
import reporter

parser = argparse.ArgumentParser(
    description="Herramienta para automatizar escaneos OSINT. Busca subdominios, resuelve IPs y grafica."
)
parser.add_argument("dominio", help="Dominio a escanear.")
args = parser.parse_args()
dominio = graph.Node("Dominio", "User Input", "User Input", "Alta", args.dominio)

main_graph = graph.Graph()
main_graph.add_node(dominio)


def procesar_modulo(graph: object, nodes: list, relations: list, modulo: str):
    for n in nodes:
        main_graph.add_node(n)
    for r in relations:
        main_graph.add_relation(r.origin_node_id, r.destination_node_id, r.type)
    print(f"Modulo {modulo} procesado con éxito")


nodes, relations = dns_resolver.resolver(dominio)
procesar_modulo(main_graph, nodes, relations, "dns")

nodes, relations = crtsh_client.crtsh(dominio)
procesar_modulo(main_graph, nodes, relations, "crt.sh")


main_graph.show_graph()
json_name = (
    f"reporte_{dominio.value}-{datetime.datetime.now().strftime('%Y_%m_%d-%H%M')}"
)
reportStatus = reporter.to_json(main_graph, json_name)
if reportStatus:
    print("Exportado con éxito")
