# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Sales of the year",
    "summary": "Track product last 365 days sales ",
    "version": "16.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["delivery"],
    "data": [
        "data/ir_cron.xml",
        "views/product_product_views.xml",
        "views/product_template_views.xml",
    ],
}
