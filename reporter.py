import json


def to_json(graph: object, nombre_archivo):
    graph_dict = {}
    for n in graph.nodes:
        n_relations = []
        for r in graph.nodes[n].node_relations:
            relation = (
                graph.nodes[r.origin_node_id].value
                + " "
                + r.type
                + " "
                + graph.nodes[r.destination_node_id].value
            )
            n_relations.append(str(relation))
        n_dict = {
            "type": graph.nodes[n].type,
            "source": graph.nodes[n].source,
            "origin_node": graph.nodes[n].origin_node_id,
            "trust": graph.nodes[n].trust,
            "value": graph.nodes[n].value,
            "timestamp": graph.nodes[n].timestamp,
            "validated_by": graph.nodes[n].validated_by,
            "extra_data": graph.nodes[n].extra_data,
            "node_relations": n_relations,
        }
        graph_dict[n] = n_dict

    try:
        if not nombre_archivo.endswith(".json"):
            nombre_archivo = f"{nombre_archivo}.json"
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            json.dump(graph_dict, archivo, indent=4, ensure_ascii=False)
            print(f"Saved as {archivo}")
        return True
    except TypeError as e:
        print(
            f"Error: El diccionario contiene datos no soportados por el formato JSON. {e}"
        )
        return False
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: No se pudo crear el archivo. {e}")
        return False
