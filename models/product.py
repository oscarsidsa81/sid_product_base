from odoo import fields, api, models


class ProductTemplate ( models.Model ) :
    _inherit = "product.template"

    precio_ton = fields.Monetary ( string="Precio por Tonelada",
                                   help="Precio por Tonelada para el producto basado en Coste Medio\n"
                                        "y el peso unitario de la plantilla",
                                   store=True,
                                   readonly=True,
                                   tracking=True,
                                   compute="_compute_precio_ton",
                                   )
    sid_forecasted_mad = fields.Float (
        string="Cant. Pronosticada Madrid",
        compute="_compute_sid_forecasted_mad",
        store=True,
    )
    sid_forecasted_ptllno = fields.Float (
        string="Cant. Pronosticada Puertollano",
        compute="_compute_sid_forecasted_ptllno",
        store=True,
    )
    sid_pasillo = fields.Many2one (
        "sid.location.option",
        string="Pasillo",
        domain="[(\"location_type\", \"=\", \"pasillo\"), (\"active\", \"=\", True)]",
    )
    sid_alto = fields.Many2one (
        "sid.location.option",
        string="Alto",
        domain="[(\"location_type\", \"=\", \"alto\"), (\"active\", \"=\", True)]",
    )
    sid_lado = fields.Many2one (
        "sid.location.option",
        string="Lado",
        domain="[(\"location_type\", \"=\", \"lado\"), (\"active\", \"=\", True)]",
    )
    sid_largo = fields.Many2one (
        "sid.location.option",
        string="Largo",
        domain="[(\"location_type\", \"=\", \"largo\"), (\"active\", \"=\", True)]",
    )
    sid_AXI = fields.Char ( string="Referencia AXI", store=True, tracking=True,
                            help="Referencia AXI para tener trazabilidad con el sistema anterior" )

    purchased_qty_3y = fields.Float (
        string="Cantidad comprada (3 años naturales)",
        compute="_compute_purchased_qty_3y",
        store=False,
        help="Suma de cantidades compradas desde el 1/1 del año (año_actual-2) hasta hoy. "
             "Incluye el año en curso hasta la fecha y los dos años anteriores completos."
    )
    sid_coste_medio = fields.Float ( string="Coste Medio",
                                     compute="_compute_sid_coste_medio",
                                     tracking=True, readonly=True,
                                     help="Coste medio para poder realizar el tracking\n"
                                          " y que aparezca en el chatter" )

    # COMPUTES

    @api.depends ( "weight", "standard_price", "categ_id.parent_id" )
    def _compute_precio_ton(self) :
        for record in self :
            record.precio_ton = round (
                (record.standard_price / record.weight * 1000), 0 ) or 0.0

    @api.depends ( "standard_price" )
    def _compute_sid_coste_medio(self) :
        for record in self :
            record.sid_coste_medio = record.standard_price or 0.0

    @api.depends ( "virtual_available" )
    def _compute_sid_forecasted_mad(self) :
        madrid_state = self.env.ref ( "base.state_es_m",
                                      raise_if_not_found=False )

        wh_domain = []
        if madrid_state :
            wh_domain = [("partner_id.state_id", "=", madrid_state.id)]
        else :
            # Fallback si por lo que sea no existe el xml_id:
            wh_domain = [("partner_id.state_id.code", "=", "28")]

        # Opcional pero recomendable si trabajas multi-compañía:
        wh_domain.append ( ("company_id", "=", self.env.company.id) )

        wh = self.env["stock.warehouse"].search ( wh_domain, limit=1 )
        madrid_loc = wh.lot_stock_id if wh else False

        for tmpl in self :
            if not madrid_loc :
                tmpl.sid_forecasted_mad = 0.0
                continue

            qty = 0.0
            for product in tmpl.product_variant_ids :
                qty += product.with_context (
                    location=madrid_loc.id ).virtual_available

            tmpl.sid_forecasted_mad = qty

    @api.depends ( "virtual_available" )
    def _compute_sid_forecasted_ptllno(self) :
        cr_state = self.env.ref ( "base.state_es_cr",
                                  raise_if_not_found=False )
        wh_domain = []
        if cr_state :
            wh_domain = [("partner_id.state_id", "=", cr_state.id)]
        else :
            # Fallback si por lo que sea no existe el xml_id:
            wh_domain = [("partner_id.state_id.code", "=", "13")]

        # Opcional pero recomendable si trabajas multi-compañía:
        wh_domain.append ( ("company_id", "=", self.env.company.id) )

        wh = self.env["stock.warehouse"].search ( wh_domain, limit=1 )
        madrid_loc = wh.lot_stock_id if wh else False

        for tmpl in self :
            if not madrid_loc :
                tmpl.sid_forecasted_ptllno = 0.0
                continue

            qty = 0.0
            for product in tmpl.product_variant_ids :
                qty += product.with_context (
                    location=madrid_loc.id ).virtual_available

            tmpl.sid_forecasted_ptllno = qty

    def _get_3y_natural_range(self) :
        """Devuelve (start_dt, end_dt) para 3 años naturales: año_actual-2 a hoy."""
        today = fields.Date.context_today ( self )  # date
        start = date ( today.year - 2, 1, 1 )  # 1 enero de hace 2 años
        # end = ahora (datetime) para incluir hasta el momento actual
        start_dt = datetime.combine ( start, datetime.min.time () )
        end_dt = fields.Datetime.now ()
        return start_dt, end_dt

    @api.depends ( "product_variant_ids" )
    def _compute_purchased_qty_3y(self) :
        start_dt, end_dt = self._get_3y_natural_range ()

        # Todos los product.product (variantes) involucrados
        all_variants = self.mapped ( "product_variant_ids" )
        qty_by_tmpl = {tmpl.id : 0.0 for tmpl in self}

        if not all_variants :
            for tmpl in self :
                tmpl.purchased_qty_3y = 0.0
            return

        # Dominio de líneas de compra dentro del rango (date_approve si existe; si no, date_order)
        # En la práctica date_approve suele ser mejor para "comprado realmente".
        PurchaseLine = self.env["purchase.order.line"]
        date_field = "order_id.date_approve" if "date_approve" in self.env[
            "purchase.order"]._fields else "order_id.date_order"

        domain = [
            ("product_id", "in", all_variants.ids),
            ("order_id.state", "in", ("purchase", "done")),
            (date_field, ">=", start_dt),
            (date_field, "<=", end_dt),
        ]

        pols = PurchaseLine.search ( domain )

        for line in pols :
            product = line.product_id
            tmpl_id = product.product_tmpl_id.id

            # Convertimos la cantidad de la línea a la UoM del producto (uom_id)
            qty = line.product_uom._compute_quantity ( line.product_qty,
                                                       product.uom_id )
            qty_by_tmpl[tmpl_id] = qty_by_tmpl.get ( tmpl_id, 0.0 ) + qty

        for tmpl in self :
            tmpl.purchased_qty_3y = qty_by_tmpl.get ( tmpl.id, 0.0 )
