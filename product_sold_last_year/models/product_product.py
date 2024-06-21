# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_sold_qty_365 = fields.Float(
        string="Last 365 days sales",
        company_dependent=True,
        digits="Product Unit of Measure",
        groups="base.group_user",
        copy=False,
        help="Daily report on how many units were sold for the last 365 days",
    )
    product_sold_qty_365_monthly_mean = fields.Float(
        company_dependent=True,
        digits="Product Unit of Measure",
        groups="base.group_user",
        copy=False,
        help="Monthly average for las 365 days sales",
    )
    number_of_stock_days = fields.Integer(
        copy=False, company_dependent=True, help="Days with stock"
    )
    desired_availavility_days = fields.Integer(company_dependent=True, default=1)
    minimum_recommended_qty = fields.Float(
        string="Recommended minimum", copy=False, company_dependent=True
    )
    rotation_sale_mean = fields.Integer(copy=False, company_dependent=True)

    def _product_sales_metrics(self):
        """Compute product sale metrics for each company. We use the field `product_qty`
        from `delivery` which gives us already the converted UoM quantities"""
        date_365_days_ago = fields.Datetime.today() - relativedelta(days=365)
        companies = self.env["res.company"].search([])
        for company in companies:
            order_lines_grouped = self.env["sale.order.line"].web_read_group(
                [
                    ("company_id", "=", company.id),
                    ("product_id", "in", self.ids),
                    ("state", "in", ["done", "sale"]),
                    ("order_id.date_order", ">=", date_365_days_ago),
                ],
                ["product_qty", "order_id"],
                ["product_id"],
                expand=True,
            )
            order_lines_dict = {
                self.browse(x["product_id"][0]): {
                    "product_qty": sum(
                        [q["product_qty"] for q in x["__data"]["records"]]
                    ),
                    "sales": {o["order_id"] for o in x["__data"]["records"]},
                }
                for x in order_lines_grouped["groups"]
            }
            for product in self.with_company(company):
                sales_365 = order_lines_dict.get(product, {}).get("product_qty", 0)
                product.with_company(company).product_sold_qty_365 = sales_365
                product.product_sold_qty_365_monthly_mean = sales_365 / 12
                product.number_of_stock_days = (365 * product.qty_available) / (
                    sales_365 or 1
                )
                product.minimum_recommended_qty = (
                    sales_365 / 365
                ) * product.desired_availavility_days
                product.rotation_sale_mean = len(
                    order_lines_dict.get(product, {}).get("sales", [])
                )

    @api.model
    def _cron_product_sales_metrics(self):
        """Run daily to set product info"""
        products = self.with_context(active_test=False).search([])
        products._product_sales_metrics()
