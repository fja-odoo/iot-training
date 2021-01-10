# -*- coding: utf-8 -*-
{
    'name': "nfc_iot",

    'summary': "NFC IOT",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['iot', 'point_of_sale'],

    'data': [
        'views/templates.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
}
