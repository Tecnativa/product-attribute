# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from freezegun import freeze_time

from odoo.tests.common import Form, TransactionCase


class TestProductSalesMetrics(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        uom_kg = cls.env.ref("uom.product_uom_kgm")
        uom_g = cls.env.ref("uom.product_uom_gram")
        uom_unit = cls.env.ref("uom.product_uom_unit")
        partner_1 = cls.env["res.partner"].create(
            {
                "name": "Mr. Odoo",
            }
        )
        cls.company_1 = cls.env["res.company"].create(
            {
                "name": "Company 1",
            }
        )
        cls.company_2 = cls.env["res.company"].create(
            {
                "name": "Company 2",
            }
        )
        cls.product_a = cls.env["product.product"].create(
            {
                "name": "Product A",
                "type": "consu",
            }
        )
        cls.product_b = cls.env["product.product"].create(
            {
                "name": "Product B",
                "type": "service",
            }
        )
        cls.product_c = cls.env["product.product"].create(
            {
                "name": "Product C",
                "type": "product",
            }
        )
        product_d_form = Form(
            cls.env["product.product"].create(
                {
                    "name": "Product D",
                    "type": "product",
                }
            )
        )
        product_d_form.uom_id = uom_kg
        cls.product_d = product_d_form.save()
        cls.sale_1 = cls._create_sale(
            cls,
            partner_1,
            company=cls.company_1,
            date="2025-01-01 09:00:00",
            lines_definition=[
                (cls.product_a, uom_unit, 3),
                (cls.product_b, uom_unit, 7),
            ],
        )
        cls.sale_2 = cls._create_sale(
            cls,
            partner_1,
            company=cls.company_1,
            date="2025-01-02 09:00:00",
            lines_definition=[
                (cls.product_a, uom_unit, 8),
                (cls.product_d, uom_g, 4000),
            ],
        )
        cls.sale_3 = cls._create_sale(
            cls,
            partner_1,
            company=cls.company_1,
            date="2025-01-03 09:00:00",
            lines_definition=[
                (cls.product_c, uom_unit, 6),
                (cls.product_d, uom_kg, 20),
            ],
        )
        cls.sale_4 = cls._create_sale(
            cls,
            partner_1,
            company=cls.company_2,
            date="2025-01-01 09:00:00",
            lines_definition=[
                (cls.product_c, uom_unit, 1),
                (cls.product_a, uom_unit, 36),
            ],
        )

    def _create_sale(self, partner, company, date, lines_definition, confirm=True):
        sale_form = Form(
            self.env["sale.order"].create(
                {
                    "partner_id": partner.id,
                    "company_id": company.id,
                }
            )
        )
        for product, uom, qty in lines_definition:
            with sale_form.order_line.new() as line:
                line.product_id = product
                line.product_uom = uom
                line.product_uom_qty = qty
        sale = sale_form.save()
        if confirm:
            sale.action_confirm()
        sale.date_order = date
        return sale

    def _check_product_metrics(self, company, metrics_dict):
        for product, metrics in metrics_dict.items():
            for metric, value in metrics.items():
                self.assertAlmostEqual(product.with_company(company)[metric], value)

    @freeze_time("2026-01-01")
    def test_product_metrics(self):
        """Test metrics by product and company"""
        # 1. Metrics aren't yet computed
        metrics_dict = {
            self.product_a: {
                "product_sold_qty_365": 0,
                "product_sold_qty_365_monthly_mean": 0,
                "number_of_stock_days": 0,
                "minimum_recommended_qty": 0,
                "rotation_sale_mean": 0,
            },
            self.product_b: {
                "product_sold_qty_365": 0,
                "product_sold_qty_365_monthly_mean": 0,
                "number_of_stock_days": 0,
                "minimum_recommended_qty": 0,
                "rotation_sale_mean": 0,
            },
            self.product_c: {
                "product_sold_qty_365": 0,
                "product_sold_qty_365_monthly_mean": 0,
                "number_of_stock_days": 0,
                "minimum_recommended_qty": 0,
                "rotation_sale_mean": 0,
            },
            self.product_d: {
                "product_sold_qty_365": 0,
                "product_sold_qty_365_monthly_mean": 0,
                "number_of_stock_days": 0,
                "minimum_recommended_qty": 0,
                "rotation_sale_mean": 0,
            },
        }
        self._check_product_metrics(self.company_1, metrics_dict)
        self._check_product_metrics(self.company_2, metrics_dict)
        # 2. Let's trigger the cron
        self.env["product.product"]._cron_product_sales_metrics()
        # 3. Now we've got all the expected metrics
        self._check_product_metrics(
            self.company_1,
            {
                self.product_a: {
                    "product_sold_qty_365": 11,
                    "product_sold_qty_365_monthly_mean": 0.92,
                    "number_of_stock_days": 0,
                    "minimum_recommended_qty": 0,
                    "rotation_sale_mean": 2,
                },
                self.product_b: {
                    "product_sold_qty_365": 7,
                    "product_sold_qty_365_monthly_mean": 0.58,
                    "number_of_stock_days": 0,
                    "minimum_recommended_qty": 0,
                    "rotation_sale_mean": 1,
                },
                self.product_c: {
                    "product_sold_qty_365": 6,
                    "product_sold_qty_365_monthly_mean": 0.5,
                    "number_of_stock_days": 0,
                    "minimum_recommended_qty": 0,
                    "rotation_sale_mean": 1,
                },
                self.product_d: {
                    "product_sold_qty_365": 24,
                    "product_sold_qty_365_monthly_mean": 2,
                    "number_of_stock_days": 0,
                    "minimum_recommended_qty": 0,
                    "rotation_sale_mean": 2,
                },
            },
        )
        self._check_product_metrics(
            self.company_2,
            {
                self.product_a: {
                    "product_sold_qty_365": 36,
                    "product_sold_qty_365_monthly_mean": 3,
                    "number_of_stock_days": 0,
                    "minimum_recommended_qty": 0,
                    "rotation_sale_mean": 1,
                },
                self.product_c: {
                    "product_sold_qty_365": 1,
                    "product_sold_qty_365_monthly_mean": 0.08,
                    "number_of_stock_days": 0,
                    "minimum_recommended_qty": 0,
                    "rotation_sale_mean": 1,
                },
            },
        )
