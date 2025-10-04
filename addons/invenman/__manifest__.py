{
    'name': 'Invenman',
    'version': '1.0',
    "description": """
    Inventory, supplier and customer management
    """,
    'depends': ['base', "web"],
    'category': 'Inventory',
    'data': [
        'security/ir.model.access.csv',
        'data/unit_data.xml',
        'data/sequences.xml',
        'views/customer_views.xml',
        'views/product_category_views.xml',
        'views/product_views.xml',
        'views/purchase_views.xml',
        'views/sale_views.xml',
        'views/supplier_views.xml',
        'views/unit_views.xml',
        'views/menus.xml',
    ],
    'sequence': 1,
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
