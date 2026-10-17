# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tools.convert import convert_file


def pre_init_hook(env):
    """
    Create product_allergen_attribute used in compute methods with get_allergen_id()
    """
    convert_file(
        env, "product_ingredient", "data/product_allergen_data.xml", {}, mode="init"
    )
