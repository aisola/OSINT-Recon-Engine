# OSINT-Recon-Engine

Herramienta OSINT basada en grafos para reconocimiento de infraestructura y superficie de ataque. Cada dato descubierto es un **nodo** y cada vínculo entre datos una **relación**, formando un grafo navegable y exportable.

> **Estado:** Work in progress — MVP funcional (V3 en curso). En desarrollo activo como proyecto de aprendizaje.

---

## Problema que resuelve

Las herramientas OSINT tradicionales devuelven listas planas de datos sin conexión semántica entre sí. Este proyecto modela la información como un **grafo dirigido**, permitiendo:

- Trazabilidad de cada descubrimiento (quién descubrió qué y desde dónde).
- Correlación entre activos (dominios, IPs, certificados, emails).
- Exportación estructurada para análisis posteriores.
- Arquitectura modular: agregar una nueva fuente OSINT requiere solo crear un módulo que devuelva nodos y relaciones.

---

## Stack

- Python 3.14 — solo **stdlib** (sin dependencias externas).
- `socket.gethostbyname` para resolución DNS.
- `urllib.request.urlopen` + `json` para APIs.

---

## Features implementadas

### V1 — Núcleo
- [x] Modelo de datos: `Node`, `Relation`, `Graph` con validación.
- [x] Resolución DNS con wordlist de 15 subdominios (`dns_resolver.py`).
- [x] Tipos de nodo: `Dominio`, `Subdominio`, `IP`.
- [x] Relaciones: `TIENE_SUBDOMINIO`, `RESUELVE_A`.
- [x] Entry point con `argparse` (`main.py`).

### V2 — Certificados y emails
- [x] Consulta a crt.sh con retry y timeout (`crtsh_client.py`).
- [x] Nuevos tipos de nodo: `Certificado`, `Email`.
- [x] Nuevas relaciones: `EMITIDO_PARA`, `APARECE_EN`.
- [x] Exportación a JSON (`reporter.py`).

### V3 — Infraestructura y propiedad
- [x] Módulo ASN lookup vía ip-api.com (`asn_client.py`).
- [x] Nuevos tipos de nodo: `ASN`, `ISP`.
- [x] Nuevas relaciones: `PERTENECE_A` (IP → ASN, ASN → ISP).
- [x] Validación de tipo de nodo en todos los módulos (`NodeTypeError`).
- [x] Flags de entrada: `-d` (dominio), `-i` (IP), `-s` (subdominio).
- [ ] Módulo WHOIS / empresa.
- [ ] Deduplicación y corroboración de nodos.

---

## Próximos pasos

### V3 — Infraestructura y propiedad (cont.)
- [ ] Módulo WHOIS / empresa.
- [ ] Deduplicación de nodos por múltiples fuentes.

### V4 — Exportación para visualización
- [ ] Exportación a GraphML.
- [ ] Exportación a GEXF.

### Post-V4
- [ ] Web UI.

---

## Uso

```bash
python main.py -d <dominio>
python main.py -i <ip>
python main.py -s <subdominio>
```

Ejemplo:

```bash
python main.py -d ejemplo.com
python main.py -i 104.16.0.0
```

Genera un reporte JSON con todos los nodos y relaciones descubiertos.

---

## Arquitectura

Cada módulo OSINT devuelve `tuple[list[Node], list[Relation]]` y se integra en `main.py` mediante una función auxiliar (`procesar_modulo`). Agregar una fuente nueva requiere únicamente crear el módulo y añadir dos líneas en `main.py`.

```
OSINT-Recon-Engine/
├── graph.py          # Modelo de datos (Node, Relation, Graph, NodeTypeError)
├── dns_resolver.py   # Resolución DNS + wordlist
├── crtsh_client.py   # Consulta a crt.sh
├── asn_client.py     # ASN lookup vía ip-api.com
├── reporter.py       # Exportación a JSON
└── main.py           # Orquestador con flags -d / -i / -s
```

---

## Licencia

MIT
