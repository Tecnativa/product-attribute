# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade

from odoo import SUPERUSER_ID, api
from odoo.tools import config


def pre_init_hook(cr):
    """
    Create product_allergen_attribute to can be used in get_allergen_id() used in compute
    methods
    """
    if config["test_enable"]:
        return openupgrade.load_data(
            cr, "product_ingredient", "data/product_allergen_data.xml"
        )
    openupgrade.rename_xmlids(
        cr,
        {
            (
                "congeladosromero_custom.product_allergens_attribute",
                "product_ingredient.product_allergen_attribute",
            ),
        },
    )
    openupgrade.logged_query(
        cr,
        """ALTER TABLE stock_production_lot
            ADD COLUMN IF NOT EXISTS ingredient_additional_info TEXT""",
    )
    openupgrade.logged_query(
        cr,
        """CREATE TABLE IF NOT EXISTS product_attribute_value_product_product_rel
           (product_product_id integer,product_attribute_value_id integer)""",
    )
    env = api.Environment(cr, SUPERUSER_ID, {})
    attribute = env.ref("product_ingredient.product_allergen_attribute")
    openupgrade.logged_query(
        cr,
        """
        INSERT INTO product_attribute_value_product_product_rel (
            product_product_id, product_attribute_value_id)
        SELECT pp.id as product_product_id,
               pavptalr.product_attribute_value_id as product_attribute_value_id
        FROM product_template_attribute_line ptal
                 JOIN product_attribute_value_product_template_attribute_line_rel pavptalr
                      ON pavptalr.product_template_attribute_line_id = ptal.id
                 JOIN product_product pp ON pp.product_tmpl_id = ptal.product_tmpl_id
        WHERE ptal.attribute_id = %s
        """,
        [attribute.id],
    )
    openupgrade.logged_query(
        cr,
        """
        DELETE FROM product_template_attribute_value_sale_order_line_rel
        WHERE product_template_attribute_value_id IN (
          SELECT id
          FROM product_template_attribute_value
          WHERE attribute_id = %s
        )
        """,
        [attribute.id],
    )
    openupgrade.logged_query(
        cr,
        """
        DELETE FROM product_template_attribute_line WHERE attribute_id = %s
        """,
        [attribute.id],
    )
