from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sid_pasillo = fields.Many2one(
        "sid.location.option",
        string="Pasillo",
        domain="[(\"location_type\", \"=\", \"pasillo\"), (\"active\", \"=\", True)]",
    )
    sid_alto = fields.Many2one(
        "sid.location.option",
        string="Alto",
        domain="[(\"location_type\", \"=\", \"alto\"), (\"active\", \"=\", True)]",
    )
    sid_lado = fields.Many2one(
        "sid.location.option",
        string="Lado",
        domain="[(\"location_type\", \"=\", \"lado\"), (\"active\", \"=\", True)]",
    )
    sid_largo = fields.Many2one(
        "sid.location.option",
        string="Largo",
        domain="[(\"location_type\", \"=\", \"largo\"), (\"active\", \"=\", True)]",
    )

    sid_pasillo = fields.Char(string="Pasillo")
    sid_alto = fields.Char(string="Alto")
    sid_lado = fields.Char(string="Lado")
    sid_largo = fields.Char(string="Largo")

class ProductProduct(models.Model):
    _inherit = "product.product"

    sid_pasillo = fields.Many2one(
        "sid.location.option",
        string="Pasillo",
        domain="[(\"location_type\", \"=\", \"pasillo\"), (\"active\", \"=\", True)]",
    )
    sid_pasillo = fields.Char(string="Pasillo")
