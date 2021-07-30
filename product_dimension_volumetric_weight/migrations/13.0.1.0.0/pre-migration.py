# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

column_renames = {
    "uom_uom": [("weight_volumetric_ratio", "volumetric_weight_ratio")],
    "product_product": [("weight_volumetric", "volumetric_weight")],
}


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_columns(env.cr, column_renames)
