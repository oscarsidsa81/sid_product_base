from odoo import fields, models


class SidLocationOption(models.Model):
    _name = "sid.location.option"
    _description = "SID Location Option"
    _order = "location_type, sequence, id"

    name = fields.Char(string="Etiqueta", required=True)
    code = fields.Char(string="Código", required=True)
    location_type = fields.Selection(
        selection=[
            ("pasillo", "Pasillo"),
            ("alto", "Alto"),
            ("lado", "Lado"),
            ("largo", "Largo"),
        ],
        string="Tipo",
        required=True,
    )
    sequence = fields.Integer(string="Secuencia", default=10)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            "sid_location_option_unique_type_code",
            "unique(location_type, code)",
            "El código debe ser único por tipo.",
        )
    ]
