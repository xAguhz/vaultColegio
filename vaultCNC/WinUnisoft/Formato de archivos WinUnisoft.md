---
tipo: referencia
tags: [winunisoft, formato, prj]
---

# Formato de archivos WinUnisoft

Un proyecto de WinUnisoft MultiCNC son **4 archivos con el mismo nombre**. Los originales están en `WinUnisoft/originales/` (no se tocan).

| Archivo | Qué es | Contenido |
|---|---|---|
| `.prj` | Proyecto (formato INI) | Máquina, control, bruto, herramientas y orígenes |
| `.nc` | Programa CNC | El código G/M que se simula |
| `.txt` | Hoja de proceso vacía | Plantilla en francés, sin datos |
| `.wmf` | Imagen (Windows Metafile) | Dibujo de la pieza; los dos TP tienen el mismo archivo |

## Codificación
- Todos los archivos de texto usan finales de línea **CRLF** (`\r\n`).
- El `.prj` y el `.txt` están en **latin-1** (ISO-8859-1). El `.nc` es ASCII puro.
- Para leer el `.prj` en Python: `open(ruta, encoding="latin-1", newline="")`.

## Secciones del `.prj`

### [MAQUINA]
| Clave | Valor en los TP | Significado |
|---|---|---|
| Maquina | `...\Winunisoft multicnc\LIB\Apolo.mch` | Archivo de la máquina |
| TipoMaquina | Torno | Tipo |
| Tipo | 1 | Tipo numérico |
| ControlText | Fanuc16iTA | Control |
| Unidad | 0 | Milímetros |
| LimiteMaquina | -8.5,0.00,0.00,85.5,0.00,287 | Mínimos y máximos de los ejes |
| CeroMaquina | 85.5,0.00,287 | Cero máquina |
| OrigenPref | 0,0,0 | Origen preferido |
| VerCero, VerOrigen | 1, 0 | Qué se dibuja |
| PosicionCambioHta | 70.00,0.00,230.00 | Donde cambia de herramienta |
| TiempoCambio | 5 | Segundos por cambio |
| PosTorreta | 0 | Posición inicial de la torreta |
| VelocidadMaxima / Minima | 4000 / 10 | RPM |
| AvanceMaximo / AvanceG00 | 1500 / 1500 | Avances máximos |
| GiroCabezal, Trayectoria, CotaX | 0 | Opciones de visualización |

### [BRUTO]
Las claves cambian de nombre según la forma; para un cilindro (`Forma=0`):

| Clave | Valor | Significado |
|---|---|---|
| Forma | 0 | Cilindro |
| CodForma | 55 | Código de la forma |
| Fijacion / CodFijacion | 0 / 80 | Tipo de sujeción |
| `YMax/ZMax` | 130 | **Largo** del bruto |
| `ZMax/DExt` | 42 | **Diámetro exterior** del bruto |
| `XMax/Zmin`, `XMin/Long`, `YMin/D`, `ZMin/Nada` | 0 | No se usan en cilindro |

### [TOOLS]
Una línea `Tool=` por herramienta (T0 a T11). Los espacios del texto se escriben como `^`. Cada línea lleva el nombre y estas claves:

| Clave | Significado |
|---|---|
| `_NumHta`, `_Corrector` | Número de herramienta y de corrector |
| `_Descrip` | Descripción |
| `Quadrant` | Cuadrante de la punta (1 en las exteriores, 7 en las interiores, 2 en T10 y en T11 del Peón) |
| `Type` | DIAMOND (inserto), GROOVING (ranurado) o THREAD (rosca) |
| `IC`, `Alpha` | Círculo inscrito y ángulo de punta |
| `Orient.`, `_Orient.` | Orientación del inserto |
| `r` | Radio de punta |
| `_CodForma` | Código de forma (3 o 4; 2 interior) |
| `Height` | Profundidad máxima (ranurado, rosca) |
| `H_Width`, `H_Hght`, `H_Clr_X`, `H_Clr_Z`, `H_Ang` | Medidas del portaherramienta |
| `Rot_mode` | Sentido de giro (CW) |

La lista de herramientas está en [[Herramientas y plaquitas]].

### [ORIGEN]
`G53` a `G59` con tres números (X, Y, Z). En los TP: `G54=0.00,0.00,129` y los demás en cero. Es el **cero pieza** que usa `G54` en el programa (ver [[Estructura de un programa]]).

### [NOTAS]
Vacía.

### [General]
Parámetros de la pantalla del simulador: `Gama`, `PosX`, `PosZ`, `SCabezal`, `FAvance`, `G9495=95`, `G9697=97`, `THerramienta`, `HtaCorrecX`, `HtaCorrecZ`, holguras, `TipoTorno=$33`, `PosCarrusel` y orígenes. En los dos TP tienen los mismos valores.

## Por qué el generador puede escribirlos directo
Son texto plano con una estructura fija: un INI y un programa de líneas. No hay cabecera binaria ni firma. Si el generador respeta **CRLF**, **latin-1** y las mismas claves, WinUnisoft abre el proyecto como si lo hubieras guardado vos. Eso evita copiar y pegar el programa a mano en el simulador.

> [!tip] Qué cambia entre piezas
> Solo cambian `YMax/ZMax` y `ZMax/DExt` (bruto), `G54` (cero pieza) y el contenido del `.nc`. El resto del `.prj` se copia igual.

Ver también: [[Torno y control]], [[TP Peón]], [[TP Alfil]].
