# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from dateutil.relativedelta import relativedelta

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_selled_qty_365 = fields.Float(
        company_dependent=True,
        digits='Product Unit of Measure',
        groups="base.group_user",
        help="Daily report on how many units were selled for the last 365 days"
    )
    product_selled_qty_365_monthly_mean = fields.Float(
        company_dependent=True,
        digits='Product Unit of Measure',
        groups="base.group_user",
        help="Monthly average for las 365 days sales"
    )
    number_of_stock_days = fields.Integer(
        company_dependent=True, help="Days with stock"
    )
    desired_availavility_days = fields.Integer(company_dependent=True, default=1)
    minimum_recommended_qty = fields.Float(
        company_dependent=True
    )
    rotation_sale_mean = fields.Integer(company_dependent=True)

    def _product_selled_qty_365(self):
        date_365_days_ago = fields.Datetime.today() - relativedelta(days=365)
        companies = self.env['res.company'].search([])
        for company in companies:
            order_lines_grouped = self.env["sale.order.line"].web_read_group(
                [
                    ("company_id", "=", company.id),
                    ("product_id", "in", self.ids),
                    ("state", "in", ["done", "sale"]),
                    ("order_id.date_order", ">=", date_365_days_ago),
                ],
                ["product_uom_qty", "order_id"],
                ["product_id"],
                expand=True
            )
            order_lines_dict = {
                self.browse(x["product_id"][0]): {
                    "product_uom_qty": x["product_uom_qty"],
                    "sales": set([y["order_id"] for y in x["__data"]["records"]])
                }
                for x in order_lines_grouped["groups"]
            }
            for product in self.with_company(company.id):
                sales_365 = order_lines_dict.get(product, {}).get("product_uom_qty", 0)
                product.product_selled_qty_365 = sales_365
                product.product_selled_qty_365_monthly_mean = sales_365 / 12
                product.number_of_stock_days = (365 * product.qty_available) / sales_365
                product.minimum_recommended_qty = (
                    (sales_365 / 365) * product.desired_availavility_days
                )
                product.rotation_sale_average = order_lines_dict.get(product, {}).get("sales", 0)

    def action_recompute_selled_qty_365(self):
        self._product_selled_qty_365()

    def _cron_product_sales_365(self):
        """Run daily to set product info"""
        products = self.with_context(active_test=False).search([])
        products._product_selled_qty_365()
