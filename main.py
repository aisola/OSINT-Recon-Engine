import argparse
import datetime

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
nodos, relaciones = dns_resolver.resolver(dominio)

for n in nodos:
    main_graph.add_node(n)
    print(f"Nodo {n.value} añadido con éxito.\n")

i = 1
for r in relaciones:
    main_graph.add_relation(r.origin_node_id, r.destination_node_id, r.type)
    print(f"Relación {i}/{len(relaciones)} añadida con éxito.\n")
    i += 1

main_graph.show_graph()
json_name = (
    f"reporte_{dominio.value}-{datetime.datetime.now().strftime('%Y_%m_%d-%H%M')}"
)
reportStatus = reporter.importToJson(main_graph, json_name)
if reportStatus:
    print("Exportado con éxito")
