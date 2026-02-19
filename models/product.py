from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    sid_pasillo = fields.Char(string="Pasillo (SID)")
    sid_alto = fields.Char(string="Alto (SID)")
    sid_lado = fields.Char(string="Lado (SID)")
    sid_largo = fields.Char(string="Largo (SID)")

class ProductProduct(models.Model):
    _inherit = "product.product"

    sid_pasillo = fields.Char(string="Pasillo (SID)")
    sid_forecast_madrid = fields.Float(string="Forecast Madrid (SID)")
