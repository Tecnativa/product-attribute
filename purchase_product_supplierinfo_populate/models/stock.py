# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class SotckMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_price_list_values(self):
        pricelist_values = {
            'min_quantity': 1,
            'price': self.price_unit,
            'suppinfo_id': self.picking_id.partner_id.id,
            'name': self.product_id.name,
        }
        return pricelist_values

    def create_supplierinfo(self):
        if self.picking_id.partner_id and self.product_id:
            values = {
                'name': self.picking_id.partner_id.id,
                'product_name': self.product_id.name,
                'min_qty': 1,
                'product_tmpl_id': self.product_id.product_tmpl_id.id,
                'pricelist_ids': [(0, 0, self._prepare_price_list_values())]
            }
            self.env['product.supplierinfo'].create(values)
        return True

    def _update_supplierinfo_price(self):
        if (self.state == 'assigned' and
                    self.picking_type_id.code == 'incoming'):
            supplier_pick = self.picking_id.partner_id
            supplier = self.product_id.product_tmpl_id.seller_ids.filtered(
                lambda x: x.name == supplier_pick)
            if supplier:
                if supplier.pricelist_ids:
                    actual_price = supplier.pricelist_ids[:1].price
                    if actual_price != self.price_unit:
                        supplier.pricelist_ids[:1].price = self.price_unit
                else:
                    supplier.pricelist_ids = [
                        (0, 0, self._prepare_price_list_values())]
            else:
                self.create_supplierinfo()

    @api.multi
    def write(self, vals):
        res = super(SotckMove, self).write(vals)
        for move in self:
            move._update_supplierinfo_price()
        return res
