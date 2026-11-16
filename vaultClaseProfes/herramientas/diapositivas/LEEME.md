# Diapositivas de la charla

Fuente de las 15 diapositivas. **Esta carpeta es la versión principal.**

- `project/deck.json`: título, orden, secciones y tipografías.
- `project/deck.css`: estilos compartidos (paleta pizarrón, papel y naranja).
- `project/slides/<id>.html`: una diapositiva por archivo; el `<aside>` final son las notas del orador.

Se publican en dos lugares:
1. **Página pública** (para proyectar sin iniciar sesión): `python3 herramientas/armar_diapositivas.py` arma `Exposición/Diapositivas.html`, y el workflow la publica en https://xaguhz.github.io/vaultColegio/vaultClaseProfes/diapositivas/
2. **Artifact privado de Claude** (para editar y exportar a PDF o PowerPoint): https://claude.ai/artifact/QvCiGeS3oEQ3hX4JiLZ5sr. Para actualizarlo, se publican los archivos cambiados con `root` en esta carpeta.

Si cambiás una diapositiva, actualizá los dos.
