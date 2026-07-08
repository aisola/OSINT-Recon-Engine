import socket
import time

from graph import Node, NodeTypeError, Relation


def whois_lookup(domain, whois_server):
    domain_b = f"{domain}\r\n".encode("utf-8")
    for intento in range(3):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(15)
            s.connect((whois_server, 43))
            s.sendall(domain_b)
            datos = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                datos += chunk
            return datos
        except Exception as e:
            print(f"Intento {intento + 1} falló: {e}")
            time.sleep(3)


def whois_client(node) -> tuple[list, list]:
    if node.type != "dominio":
        raise NodeTypeError(
            f"El tipo de nodo {node.type} no está soportado por el modulo."
        )
    domain = node.value
    whois_server = "whois.verisign-grs.com"
    datos = whois_lookup(domain, whois_server)
    if not datos:
        return [], []
    datos = datos.decode("utf-8", errors="ignore").split("\r\n")
    for d in datos:
        d = d.strip()
        if d.startswith("Registrar WHOIS Server:"):
            d_list = d.split(": ")
            whois_server = d_list[1]
            break

    datos_w = whois_lookup(domain, whois_server)
    if not datos_w:
        return [], []
    datos_w = datos_w.decode("utf-8", errors="ignore").split("\n")
    datos_utiles = {}
    for d in datos_w:
        d = d.strip()
        fields = [
            "Updated Date: ",
            "Creation Date: ",
            "Registrar Registration Expiration Date: ",
            "Registrant Name: ",
            "Registrant Organization: ",
            "Registrant Country: ",
        ]
        for f in fields:
            if d.startswith(f):
                dato = d.split(": ")
                datos_utiles[dato[0]] = dato[1]
                break
    # print(datos_utiles)
    if datos_utiles["Registrant Organization"]:
        nod_org = Node(
            "Empresa",
            "whois",
            node.nod_id,
            "Media",
            datos_utiles["Registrant Organization"],
            extra_data=datos_utiles,
        )
        rel_org = Relation(node.nod_id, nod_org.nod_id, "REGISTRADO_POR")
        nodes = [nod_org]
        relations = [rel_org]
        return nodes, relations


if __name__ == "__main__":
    dom = Node("Dominio", "User", "User", "Alto", "google.com")
    nodes, relations = whois_client(dom)
    # whois_client(dom)
    print(f"Empresa encontrada: {nodes[0].value}\n")
    print(
        relations[0].origin_node_id
        + " "
        + relations[0].type
        + " "
        + relations[0].destination_node_id
    )
