# Formato de pieza (`<nombre>.json`)

Un solo archivo por pieza alimenta todo: el plano de FreeCAD (PDF con rótulo) y el proyecto de WinUnisoft (.prj + .nc + .txt + .wmf).

```json
{
  "nombre": "PEON",
  "material": "SAE 4140",
  "bruto": {"d": 42, "l": 130},
  "agarre": 30,
  "largo": 74,
  "perfil": [
    {"x": 0,  "z": 0},
    {"x": 14, "z": -17, "arco": {"r": 10, "g": "G03"}},
    {"x": 22, "z": -22}
  ],
  "rotulo": {
    "titulo": "PEON", "colegio": "E.E.S.TECNICA n°3",
    "dibujo_fecha": "4/12/25", "dibujo_nombre": "Alumno",
    "reviso_fecha": "", "reviso_nombre": "Profe",
    "aprobo_fecha": "", "aprobo_nombre": "Profe",
    "escala": "1:1", "normativa": "IRAM-ISO",
    "curso": "6°1", "lamina": "1", "nota": "", "observacion": ""
  }
}
```

Reglas del perfil:
- `x` es **diámetro** (como en el programa), `z` es negativo hacia la base; Z0 es la punta de la pieza.
- Los puntos van en orden desde la punta (Z0) hasta la base (`z = -largo`).
- Un tramo es recto salvo que el punto de llegada tenga `arco`: `r` = radio y `g` = la G que usaría el programa **recorriendo de la punta hacia la base** (G03 = antihorario, G02 = horario, mirando con el radio hacia arriba y +Z a la derecha).
- Puede haber tramos verticales (mismo `z`, distinto `x`): son escalones.
- El último punto es la base (`z = -largo`), normalmente sobre el diámetro de la base; el tronzado cierra hasta X0.
