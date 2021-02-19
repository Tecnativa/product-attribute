# Copyright 2020 Tecnativa - David Vidal
<<<<<<< HEAD
# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Multi Price",
    "version": "13.0.1.0.0",
    "author": "Tecnativa," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "category": "Product Management",
    "license": "AGPL-3",
    "depends": ["product"],
=======
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Multi Price",
    "version": "11.0.1.0.0",
    'author': 'Tecnativa,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/product-attribute',
    "category": "Product Management",
    "license": "AGPL-3",
    "depends": [
        "product",
    ],
>>>>>>> [ADD] product_multi_price: New Module
    "data": [
        "security/ir.model.access.csv",
        "security/multi_price_security.xml",
        "views/multi_price_views.xml",
        "views/product_pricelist_views.xml",
        "views/product_views.xml",
    ],
<<<<<<< HEAD
    "demo": ["demo/multi_price_demo_data.xml"],
    "post_init_hook": "post_init_hook",
=======
    'demo': [
        "demo/multi_price_demo_data.xml",
    ],
>>>>>>> [ADD] product_multi_price: New Module
    "installable": True,
}
