# Plantilla para pasarme los campos por tabla

Una sección por tabla. Si no sabes algo, pon "no sé". Con esto hago el mapeo y la traducción de métricas (Paso 0 del plan) sin tener acceso a la data.

```
## Tabla: nombre_de_la_tabla
Origen: Currents / Snowflake / export del dashboard / otro
Qué representa una fila: (ej. un email enviado a un usuario)
Filas aprox: 
Periodo que cubre: 
Columnas:
| columna | tipo | qué significa | ejemplo |
|---|---|---|---|
| id | string | id único del evento | 5f3a... |
| time | timestamp | cuándo pasó | 2026-05-03 14:22:10 |
| ... | | | |
```

Además de las tablas, me sirve saber:

1. Cómo identifican hoy al dueño de una campaña: teams, tags, prefijo en el nombre, o nada.
2. Si tienen una tabla o export de usuarios con estado de suscripción.
3. Si tienen tarifas de SMS, WhatsApp, email y el costo del contrato de Braze.
4. Cómo definen hoy "conversión" y si Braze ya la atribuye.
5. Qué periodo quieren analizar.

Con esto te devuelvo `data/mapeo.md`: inventario, uniones, y una tabla por métrica con "de qué tabla sale, qué columnas usa, cómo se calcula en palabras y en SQL". Lo apruebas y después arrancan los analistas.
