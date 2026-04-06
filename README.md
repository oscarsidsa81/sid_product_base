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

## Licencia

`LGPL-3`

## Autor

- `oscarsidsa81`
- http://www.sidsaindustrial.com
