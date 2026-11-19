# Contribuir a Business Bots

Este repositorio es la fuente canónica de los plugins. Los datos de proyectos, credenciales y archivos comerciales pertenecen a sus sistemas de trabajo —por ejemplo, Google Drive— y no deben añadirse aquí.

## Preparación inicial

1. Clona el repositorio y entra en él.
2. Ejecuta `python3 scripts/validate.py`.
3. Instala el marketplace y los plugins que quieras probar:

   ```bash
   bash scripts/install.sh npv-marketing npv-data
   ```

4. Abre una conversación nueva de ChatGPT en modo Trabajo, escribe `@` y selecciona el plugin por su nombre. También puedes comprobar la instalación desde Codex.

La instalación inicial registra este repositorio como el marketplace local `business-bots`. Para instalar o reinstalar un plugin cuando el marketplace ya está registrado, usa `--update`:

```bash
bash scripts/install.sh --update npv-marketing
```

## Flujo de cambios

1. Actualiza `main` y crea una rama corta: `feature/...`, `fix/...` o `chore/...`.
2. Modifica el plugin afectado y sus pruebas. Si cambias las reglas comunes de la Capa NPV, edita [`shared/npv/capa-npv.md`](shared/npv/capa-npv.md) y ejecuta `python3 scripts/sync_shared.py`. Incluye las dos copias generadas, ya que el instalador copia cada carpeta de plugin por separado.
3. Ejecuta la validación estructural:

   ```bash
   python3 scripts/validate.py
   python3 -m unittest discover -s tests -p 'test_*.py'
   ```

4. Para una recarga local sin cambiar la versión estable, genera un cachebuster:

   ```bash
   python3 scripts/cachebust.py plugins/npv-marketing
   bash scripts/install.sh --update npv-marketing
   ```

5. Prueba en un hilo nuevo. Ejecuta `git restore plugins/npv-marketing/.codex-plugin/plugin.json` antes del commit si el único cambio del manifiesto es el cachebuster local.
6. Revisa los casos de `tests/behavior/` y registra cualquier cambio deliberado en las expectativas.
7. Abre un pull request. Antes de fusionar un cambio publicable, actualiza la versión semántica estable en `plugin.json` y el catálogo del `README.md`.

No incrementes versiones estables solo para forzar una recarga local. El cachebuster conserva la base de la versión y reemplaza cualquier sufijo anterior.
La validación normal y CI rechazan versiones `+codex.*`; únicamente `install.sh --update` permite ese sufijo durante la reinstalación local.

## Convenciones

- Cada plugin vive en `plugins/<nombre>/` y su manifiesto en `.codex-plugin/plugin.json`.
- El nombre de la carpeta debe coincidir con `plugin.json:name`.
- Cada skill vive en `skills/<nombre>/SKILL.md`; el `name` del frontmatter coincide con su carpeta.
- Mantén las instrucciones reutilizables. No incrustes nombres, precios, inventarios, leads ni segmentos de un desarrollo como valores por defecto.
- Usa ejemplos inventados o anonimizados. Nunca agregues credenciales, datos personales o exportaciones de clientes.
- Añade solo referencias que la skill realmente necesite y conserva válidos sus enlaces relativos.

## Revisión de un pull request

Un cambio está listo cuando:

- `python3 scripts/validate.py` termina correctamente;
- cada plugin afectado puede instalarse por separado desde `business-bots` y aparece con su nombre en el menú de `@`;
- el comportamiento se probó en un hilo nuevo;
- los casos afectados tienen expectativas actualizadas;
- el PR explica el cambio observable y sus límites;
- no contiene datos sensibles ni un cachebuster local accidental.
