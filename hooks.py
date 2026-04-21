from psycopg2 import sql


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
    if not source_column:
        return

    target_column = _find_column_name(cr, "product_template", "sid_AXI")
    if not target_column:
        return

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
