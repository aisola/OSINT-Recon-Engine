# OSINT-Recon-Engine

Herramienta OSINT basada en grafos para reconocimiento de infraestructura y superficie de ataque. Cada dato descubierto es un **nodo** y cada vínculo entre datos una **relación**, formando un grafo navegable y exportable.

> **Estado:** Work in progress — MVP funcional (V2). En desarrollo activo como proyecto de aprendizaje.

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

---

## Próximos pasos

### V3 — Infraestructura y propiedad
- [ ] Módulo ASN lookup.
- [ ] Módulo WHOIS / empresa.
- [ ] Nuevos tipos de nodo: `ASN`, `Empresa`.
- [ ] Nuevas relaciones: `PERTENECE_A`, `OPERADO_POR`.

### V4 — Exportación para visualización
- [ ] Exportación a GraphML.
- [ ] Exportación a GEXF.

### Post-V4
- [ ] Web UI.

---

## Uso

Actualmente solo funciona con el tipo de dato "dominio"
```bash
python main.py <dominio>
```

Ejemplo:

```bash
python main.py ejemplo.com
```

Genera un reporte JSON con todos los nodos y relaciones descubiertos.

---

## Arquitectura

Cada módulo OSINT devuelve `tuple[list[Node], list[Relation]]` y se integra en `main.py` mediante una función auxiliar (`procesar_modulo`). Agregar una fuente nueva requiere únicamente crear el módulo y añadir dos líneas en `main.py`.

```
OSINT-Recon-Engine/
├── graph.py          # Modelo de datos (Node, Relation, Graph)
├── dns_resolver.py   # Resolución DNS + wordlist
├── crtsh_client.py   # Consulta a crt.sh
├── reporter.py       # Exportación a JSON
└── main.py           # Orquestador
```

---

## Licencia

MIT
