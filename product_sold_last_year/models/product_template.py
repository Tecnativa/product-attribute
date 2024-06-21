# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_sold_qty_365 = fields.Float(
        string="Last 365 days sales",
        compute="_compute_product_sold_qty_365",
        compute_sudo=True,
        digits="Product Unit of Measure",
        groups="base.group_user",
        help="Daily report on how many units were sold for the last 365 days",
    )
    product_sold_qty_365_monthly_mean = fields.Float(
        string="Last 365 days sales (monthly mean)",
        compute="_compute_product_sold_qty_365",
        compute_sudo=True,
        digits="Product Unit of Measure",
        groups="base.group_user",
        readonly=True,
        help="Monthly average for las 365 days sales",
    )
    number_of_stock_days = fields.Integer(
        compute="_compute_product_sold_qty_365",
        compute_sudo=True,
        readonly=True,
        help="Days with stock",
    )
    minimum_recommended_qty = fields.Float(
        string="Recommended min.",
        compute="_compute_product_sold_qty_365",
        compute_sudo=True,
        readonly=True,
    )
    desired_availavility_days = fields.Integer(
        compute="_compute_desired_availavility_days",
        inverse="_inverse_desired_availavility_days",
    )
    rotation_sale_mean = fields.Integer(
        compute="_compute_product_sold_qty_365", compute_sudo=True, readonly=True
    )

    @api.depends_context("company")
    def _compute_product_sold_qty_365(self):
        """Get metrics info from the product variants and aggregate them into the
        template"""
        for template in self:
            template.product_sold_qty_365 = sum(
                template.product_variant_ids.mapped("product_sold_qty_365")
            )
            template.product_sold_qty_365_monthly_mean = (
                template.product_sold_qty_365 / 12
            )
            template.number_of_stock_days = (
                365 * template.qty_available
            ) / template.product_sold_qty_365
            template.minimum_recommended_qty = (
                template.product_sold_qty_365 / 365
            ) * template.desired_availavility_days
            template.rotation_sale_mean = sum(
                template.product_variant_ids.mapped("rotation_sale_mean")
            ) / len(template.product_variant_ids)

    @api.depends_context("company")
    def _compute_desired_availavility_days(self):
        for template in self:
            template.desired_availavility_days = sum(
                template.product_variant_ids.mapped("desired_availavility_days")
            ) / len(template.product_variant_ids)

    def _inverse_desired_availavility_days(self):
        self.product_variant_ids.desired_availavility_days = (
            self.desired_availavility_days
        )
