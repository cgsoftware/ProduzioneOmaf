# -*- coding: utf-8 -*-

{
    "name": "Gestione Lancio Produzione Omaf ",
    "version": "1.01",
    "depends": ["product", "mrp"],
    "author": "C & G Software S.a.s.",
    "category": "Mrp",
    "description": """ Al momento del lancio in produzione chiede conferma della qta da produrre e ricalcola i consumi delle 
materie prime prima di confermare i consumi stessi, in pratica cambia la qta prodotta con quella prevista
    """,
    "init_xml": [],
    'update_xml': [
                   'mrp_view.xml',
                   'security/ir.model.access.csv',
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}
