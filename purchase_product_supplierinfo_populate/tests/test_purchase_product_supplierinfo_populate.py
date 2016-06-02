# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests import common


class TestPaymentReturn(common.TransactionCase):

    def setUp(self):
        super(TestPaymentReturn, self).setUp()

        self.supplier = self.env.ref('base.res_partner_1')
        self.product = self.env.ref('product.product_product_4')

        self.purchase_order = ''
