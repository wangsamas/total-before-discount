# -*- coding: utf-8 -*-
{
    'name': "total_before_discount",

    'summary': """
        Subtitute total after discount with total before discount""",

    'description': """
        Subtitute total after discount with total before discount
    """,

    'author': "Kusuma Ruslan",
    'website': "http://www.wangsamas.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_management','sale_discount_total'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}