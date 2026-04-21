# sid_product_base

Módulo de Odoo 15 para extender la gestión de productos con información de ubicación logística y métricas operativas de stock/compras.

## Resumen funcional

Este módulo añade:

- **Clasificación de ubicación de producto** en 4 ejes:
  - Pasillo
  - Alto
  - Lado
  - Largo
- **Catálogo maestro de opciones de ubicación** (`sid.location.option`) con secuencia, activación y restricción de unicidad por tipo+código.
- **Campos calculados en producto** para soporte de operación:
  - Precio por tonelada (`precio_ton`)
  - Cantidad pronosticada en Madrid (`sid_forecasted_mad`)
  - Cantidad pronosticada en Puertollano (`sid_forecasted_ptllno`)
  - Cantidad comprada en los últimos 3 años naturales (`purchased_qty_3y`)
  - Coste medio trazable (`sid_coste_medio`)
- **Referencia histórica** de producto (`sid_AXI`) para trazabilidad con AXI.

## Dependencias

Declaradas en el manifiesto:

- `product`
- `stock`
- `sid_stock_cfg`

## Estructura del módulo

- `__manifest__.py`: metadatos y carga de recursos.
- `models/product.py`: ampliaciones sobre `product.template`.
- `models/sid_location.py`: modelo maestro `sid.location.option`.
- `views/sid_location_views.xml`: vistas tree/form, acción y menú de administración.
- `data/sid_location_data.xml`: datos iniciales (pasillos, altos, lados y largos).
- `security/ir.model.access.csv`: permisos del modelo de ubicaciones.

## Instalación

1. Copiar el módulo en la ruta de addons de Odoo.
2. Actualizar la lista de aplicaciones.
3. Instalar **sid_product_base** desde Apps.

## Configuración inicial

1. Ir a **Ajustes > Sidsa Ubicaciones-Productos** (requiere usuario con permisos de administración).
2. Revisar/ajustar catálogo de ubicaciones por tipo.
3. Validar que las plantillas de producto usen correctamente los campos Pasillo/Alto/Lado/Largo.

## Notas de operación

- Los campos de ubicación en producto filtran sólo opciones **activas** y del **tipo correspondiente**.
- El cálculo de cantidades pronosticadas por centro usa el almacén asociado al estado:
  - Madrid (`base.state_es_m`, fallback código `28`)
  - Ciudad Real / Puertollano (`base.state_es_cr`, fallback código `13`)
- El acumulado de compras considera pedidos en estado `purchase` o `done` dentro de los últimos 3 años naturales (desde el 1 de enero de hace 2 años hasta la fecha actual).

## Documentación de PR: migración de referencia AXI

### Objetivo de la PR

Esta PR incorpora migraciones automáticas para conservar información legacy al instalar/actualizar el módulo:

- **Origen legacy**: `product_template.x_default_code_old`
- **Destino nuevo**: `product_template.sid_AXI`
- **Campos legacy de ubicación**:
  - `x_pasillo` -> `sid_pasillo`
  - `x_alto` -> `sid_alto`
  - `x_lado` -> `sid_lado`
  - `x_largo` -> `sid_largo`

La migración AXI se ejecuta mediante `post_init_hook`, sólo cuando:

1. Existen ambas columnas en base de datos.
2. El destino (`sid_AXI`) está vacío.
3. El origen (`x_default_code_old`) contiene valor no vacío.

La migración de ubicaciones legacy:

1. Verifica que existan campo origen (`x_*`) y destino (`sid_*`) en `product.template`.
2. Sólo rellena el destino cuando está vacío.
3. Resuelve el valor contra `sid.location.option` por `code` y, como fallback, por `name`.

### Qué implica al instalar el módulo

Al instalar (o actualizar) `sid_product_base`, además de crear sus modelos/vistas, ocurrirá:

- Carga de datos maestros de ubicaciones (`pasillo`, `alto`, `lado`, `largo`).
- Ejecución del hook de migración de AXI y ubicaciones legacy (si aplica por estructura de BD).
- Disponibilidad de campos nuevos en `product.template`:
  - `sid_AXI` (Referencia AXI)
  - `sid_pasillo`, `sid_alto`, `sid_lado`, `sid_largo`
  - `sid_forecasted_mad`, `sid_forecasted_ptllno`
  - `precio_ton`, `sid_coste_medio`, `purchased_qty_3y`

### Módulos, campos y vistas a desactivar/revisar

Para evitar duplicidades funcionales o confusión de usuario tras la instalación, se recomienda:

1. **Campos legacy de referencia AXI**
   - Revisar vistas personalizadas que sigan mostrando `x_default_code_old`.
   - Ocultar/eliminar de formularios/listados ese campo legacy una vez validada la migración.

2. **Customizaciones de referencia alternativa**
   - Si existe otro módulo que gestione una “referencia histórica AXI” sobre `product.template`, revisar conflictos de:
     - Etiqueta de campo
     - Orden en formulario
     - Reglas de escritura/importación

3. **Vistas de ubicaciones antiguas**
   - Si hay menús o vistas heredadas para “pasillo/alto/lado/largo” fuera de `sid.location.option`, consolidar en este módulo y archivar las antiguas.

4. **Dependencias de stock/configuración**
   - Confirmar si `sid_stock_cfg` aporta configuración previa necesaria en el entorno (almacenes/convenciones).
   - Si no aporta nada en vuestra instalación, evaluar su permanencia para simplificar despliegues.

### Checklist de despliegue recomendado

1. Hacer backup de base de datos.
2. Instalar/actualizar `sid_product_base`.
3. Validar que `sid_AXI` se haya rellenado donde `x_default_code_old` tenía valor.
4. Validar que no se sobreescribieron `sid_AXI` ya informados.
5. Ajustar seguridad/vistas para ocultar `x_default_code_old` a usuarios finales.
6. Verificar menús de ubicaciones y catálogo maestro `sid.location.option`.

## Licencia

`LGPL-3`

## Autor

- `oscarsidsa81`
- http://www.sidsaindustrial.com
