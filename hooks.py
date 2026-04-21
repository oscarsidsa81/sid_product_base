from psycopg2 import sql
from odoo import SUPERUSER_ID, api


def _find_column_name(cr, table_name, column_name):
    cr.execute(
        """
        SELECT column_name
          FROM information_schema.columns
         WHERE table_name = %s
           AND lower(column_name) = lower(%s)
         LIMIT 1
        """,
        (table_name, column_name),
    )
    row = cr.fetchone()
    return row[0] if row else None


def post_init_hook(cr, registry):
    """
    Migra los valores históricos de `x_default_code_old` al nuevo campo `sid_AXI`
    en product.template.
    """
    source_column = _find_column_name(cr, "product_template", "x_default_code_old")
    target_column = _find_column_name(cr, "product_template", "sid_AXI")

    if source_column and target_column:
        query = sql.SQL(
            """
            UPDATE product_template
               SET {target} = {source}
             WHERE COALESCE(TRIM({target}), '') = ''
               AND COALESCE(TRIM({source}), '') <> ''
            """
        )
        cr.execute(
            query.format(
                target=sql.Identifier(target_column),
                source=sql.Identifier(source_column),
            )
        )

    post_init_copy_legacy_to_base(cr, registry)


def post_init_copy_legacy_to_base(cr, registry):
    """
    Migra los campos legacy de ubicación (x_*) a los nuevos campos sid_*.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    product_template = env["product.template"].sudo()
    location_option = env["sid.location.option"].sudo()

    mapping = [
        ("x_pasillo", "sid_pasillo", "pasillo"),
        ("x_alto", "sid_alto", "alto"),
        ("x_lado", "sid_lado", "lado"),
        ("x_largo", "sid_largo", "largo"),
    ]

    for source_field, target_field, location_type in mapping:
        if source_field not in product_template._fields or target_field not in product_template._fields:
            continue

        records = product_template.search(
            [(source_field, "!=", False), (target_field, "=", False)]
        )
        values = {record[source_field] for record in records if record[source_field]}
        if not values:
            continue

        opts_by_code = location_option.search(
            [("location_type", "=", location_type), ("code", "in", list(values))]
        )
        by_code = {opt.code: opt.id for opt in opts_by_code}

        opts_by_name = location_option.search(
            [("location_type", "=", location_type), ("name", "in", list(values))]
        )
        by_name = {opt.name: opt.id for opt in opts_by_name}

        for record in records:
            value = record[source_field]
            option_id = by_code.get(value) or by_name.get(value)
            if option_id:
                record.write({target_field: option_id})
