{
    'name': 'Product Visibility',
    'version': '17.0.1.0.0',
    'description': 'Product Visibility in Website',
    'category': 'Website/Product Visibility',
    'summary': 'Product Visibility in Website',
    'installable': True,
    'application': True,
    'depends': [
        'base',
        'website',
        'contacts',
        'website_sale',
        ],

    'data': [
        'views/product_visibility_views.xml',
    ]
}