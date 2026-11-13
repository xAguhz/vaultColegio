---
tipo: equipo
funcion: aumentar la presión de un gas reduciendo su volumen
fluido: gases (aire)
variable_principal: presión
tps: [TP1, TP2, TP3, TP8]
tags: [equipo, compresor, aire-comprimido]
---

# Compresor

> [!summary] Función
> Aumenta la **presión de un gas** (casi siempre aire) mediante trabajo mecánico. **No es una bomba:** el gas es **compresible**, se **calienta** al comprimirse y arrastra **humedad** que después condensa.

![[compresor.png|420]]

## Tecnologías
| | Pistón (alternativo) | Tornillo (rotativo) | Centrífugo (dinámico) |
|---|---|---|---|
| Principio | Un cilindro y un pistón con válvulas de admisión y descarga | Dos rotores helicoidales achican el volumen | Un impulsor acelera el gas y un difusor lo convierte en presión |
| Entrega | **Pulsante** | **Continua** | Continua, con grandes caudales |
| Uso típico | Talleres, consumos **intermitentes**, presiones altas | Industria con demanda **continua o estable** | Plantas grandes, servicio continuo |
| Notas | El depósito amortigua las pulsaciones. Puede ser **multietapa con interenfriador** | Lubricado (el aceite sella, lubrica y enfría, y después se separa) u **oil-free** | — |

> [!tip] En el TP1 el grupo eligió el **compresor de tornillo**: dos rotores atrapan el aire y achican el espacio, y trabaja de forma continua.

## Conceptos clave
- **Multietapa + interenfriamiento:** al enfriar entre etapas, la segunda etapa comprime menos volumen. Se gasta menos trabajo y bajan las temperaturas finales.
- **Relación de compresión** = p_abs de descarga / p_abs de aspiración. Cuanto mayor es, más exigencia térmica.
- **Caudal:** el volumen depende de p y T, así que hay que saber en **qué condiciones** se midió (**FAD**, ensayo según ISO 1217).
- **Temperatura:** comprimir calienta. Afecta el aceite, los sellos y la humedad. La refrigeración (aire, agua o aceite) **no es un accesorio**.
- **Oil-free ≠ aire puro:** el aire atmosférico ya trae partículas y humedad, y además está toda la red aguas abajo.
- **Potencia específica** (kW por m³/min): es la forma correcta de comparar eficiencia, no la potencia del motor.

## Datos reales: fichas CAGI (TP8)
| | BOGE S 55-4 LF N | Atlas Copco GA45VSD-175 AP |
|---|---|---|
| Tipo | Tornillo lubricado, refrigerado por aire, con variador | Tornillo lubricado, refrigerado por aire, con variador |
| Presión de la ficha | 100 psig (6,9 bar) | 125 psig (8,6 bar) |
| Motor | 75 hp | 60 hp |
| Caudal máximo | 390,5 acfm (11,1 m³/min) | 284 acfm (8,0 m³/min) |
| Potencia específica a caudal máximo | **16,72** kW por 100 acfm | **20,4** kW por 100 acfm |
| Potencia específica a caudal mínimo | 22,54 (con 83,7 acfm) | 27,4 (con 55 acfm) |
| Fecha de la ficha | 25/09/2025 | 15/06/2012 |

- Las fichas están a **distinta presión**, así que no se comparan directo.
- En los dos equipos, **a bajo caudal el aire sale más caro**, aun con variador.
- El caudal está medido según ISO 1217, Anexo E, en condiciones de aspiración.

## Control
| Método | Cómo funciona | Cuándo conviene |
|---|---|---|
| **Start-stop** (presostato) | Para en la presión alta y arranca en la baja | Equipos chicos y demanda intermitente. El depósito espacia los arranques |
| **Carga-descarga** | El motor sigue girando y alterna entre producir y estar en vacío | Equipos grandes. En vacío igual consume energía |
| **Velocidad variable** (VFD) | Adapta las RPM a la demanda | Demanda muy variable, aunque no es la mejor opción en todos los casos |

## Fallas y diagnóstico
- **Temperatura alta:** poca refrigeración, suciedad, falta de aceite o problemas mecánicos.
- **Más consumo sin más producción:** fugas, más presión de consigna, filtros saturados, más horas en vacío.
- **Un compresor más grande no arregla una red mala:** primero hay que ver si la "demanda" es del proceso o son **fugas**.

## Relacionado
[[Sistema de aire comprimido]] · [[Recipiente a presión]] · [[Bomba]] · [[TP8 Compresores de aire]] · [[Unidad FRL]]
