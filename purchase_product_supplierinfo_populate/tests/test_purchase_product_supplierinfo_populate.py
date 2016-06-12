# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests import common


class TestSupplierInfoPopulate(common.TransactionCase):

    def setUp(self):
        super(TestSupplierInfoPopulate, self).setUp()
        vals_supplier = {
            'name': 'My Supplier',
            'supplier': True,
            'is_company': True,
        }
        self.supplier = self.env['res.partner'].create(vals_supplier)

        vals_product = {
            'name': 'My Product',
            'standard_price': 500.00,
            'type': 'product',
        }
        self.product = self.env.ref('product.product_product_4')

        vals_supplier_info = {
            'name': self.supplier.id,
            'product_name': 'Supplier product name',
            'qty': 1.0,
            'product_tmpl_id': self.product.id,

        }
        self.supplier_info = self.env['product.supplierinfo'].create(
            vals_supplier_info)

        vals_supplier_price_list = {
            'name': self.supplier.id,
            'suppinfo_id': self.supplier_info.id,
            'min_quantity': 1.0,
            'price': 125.0,
        }
        self.supplier_info = self.env['pricelist.partnerinfo'].create(
            vals_supplier_price_list)

        vals_purchase = {
            'name': 'Test 01',
            'partner_id': self.supplier.id,
            'order_line': 1.0,
        }
        self.purchase_order = self.env['purchase.order'].create(vals_purchase)

        vals_purchase_line = {
            'name': 'Description',
            'product_qty': 1.0,
            'product_id': self.product.id,
            'order_id': self.purchase_order.id,
        }
        self.purchase_order = self.env['purchase.order.line'].create(
            vals_purchase_line)

        vals_stock = {
            'name': 'Test 01',
            'product_id': self.product.id,
            'product_qty': 1.0,
            'partner_id': self.supplier.id,
            'product_uom_qty': 1.0,
            'location_id': self.supplier.id,
            'location_dest_id': self.supplier.id,
            'price_unit': self.supplier.id,
        }
        self.stock_move = self.env['stock.move'].create(vals_stock)
