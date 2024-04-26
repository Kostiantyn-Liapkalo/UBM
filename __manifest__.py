# -*- coding: utf-8 -*-
{
    'name': "my_product",
    'summary': """
        Модуль управління товарами, замовленнями, автомобілями та маршрутами.""",
    'description': """
        Цей модуль дозволяє вам ефективно управляти товарами, замовленнями та логістичними процесами шляхом визначення взаємозв'язків між контрагентами, товарами, замовленнями, автомобілями та маршрутами.
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Inventory/Logistics',
    'version': '1.0',
    'depends': ['base', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/partner_view.xml',
        'views/product_view.xml',
        'views/order_view.xml',
        'views/order_line_view.xml',
        'views/vehicle_view.xml',
        'views/route_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'auto_install': False,
}
