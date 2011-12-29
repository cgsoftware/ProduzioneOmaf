# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2008 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from tools.translate import _

from osv import fields, osv

#
# Dimensions Definition
#
class mrp_product_produce(osv.osv_memory):
    _inherit = "mrp.product.produce"
    _columns = {
                'product_id_produce': fields.many2one('product.product', 'Articolo', required=True, select=True, domain=[('type', '<>', 'service')]),

                }
    
    def _get_product_id_produce(self, cr, uid, context=None):
        #import pdb;pdb.set_trace()
        ## è previsto che questo tipo di produzione sia per singolo articolo e non x + articoli sulla stessa produzione
        if context is None:
            context = {}
        prod = self.pool.get('mrp.production').browse(cr, uid, context['active_id'], context=context)
        return  prod.product_id.id
    
    


    

    def do_produce(self, cr, uid, ids, context=None):
       
        # cicla si movimenti che ha se c'è già la riga per sicurezza la riscrive aggiornando la qta di scarico
        # se non c'è il movimento scrive la nuova riga con lo stato giusto di confermato
        production_id = context['active_id']
        production_order = self.pool.get('mrp.production').browse(cr, uid, context['active_id'], context=context)
        product_qty_planned = production_order.product_qty
        for dati in self.browse(cr, uid, ids):        
            ok = self.pool.get('mrp.production').write(cr, uid, [production_order.id], {'product_qty':dati.product_qty, 'product_qty_planned':product_qty_planned})
            change_qty= self.pool.get('change.production.qty').create(cr,uid,{'product_qty':dati['product_qty']})
            ok = self.pool.get('change.production.qty').change_prod_qty(cr,uid,[change_qty],context)
 
        # import pdb;pdb.set_trace()
        # qui modifica il carico della qta prodotta
        #production_order = self.pool.get('mrp.production').browse(cr, uid, context['active_id'], context=context)
        #product_qty_planned = production_order.product_qty
        #ok = self.pool.get('mrp.production').write(cr, uid, [production_order.id], {'product_qty':dati.product_qty, 'product_qty_planned':product_qty_planned})
        #for mov_mag_id in production_order.move_created_ids:
        #    ok = self.pool.get('stock.move').write(cr, uid, [mov_mag_id.id], {'product_qty': dati.product_qty, })
        
        
        
       
        
        # qui fa lo standard
        if context is None:
            context = {}
        prod_obj = self.pool.get('mrp.production')
        move_ids = context.get('active_ids', [])
        for data in self.read(cr, uid, ids, context=context):
            for move_id in move_ids:
                prod_obj.action_produce(cr, uid, move_id,
                                    data['product_qty'], data['mode'], context=context)

        return {'type': 'ir.actions.act_window_close'}

    _defaults = {
        'product_id_produce':_get_product_id_produce,
    }
   
mrp_product_produce()


class mrp_production(osv.osv):
    _inherit = 'mrp.production' 
                #Do not touch _name it must be same as _inherit
                #_name = 'mrp.production' cr
    _columns = {
                'product_qty_planned': fields.float('Product Qty Planned', required=False, states={'draft':[('readonly', False)]}, readonly=True),
                'note':fields.text('Note'),
                'pz_busta_collo':fields.integer('N. Pezzi in Busta o Collo'),
                'buste_scatola':fields.integer('N. Buste per Scatolo'),
                'tipo_scatola':fields.selection([('Stampata', 'Stampata'), ('Neutra', 'Neutra')], 'Tipo Scatola', required=False, ),
                'tasselli':fields.integer('Tasselli'),
                'battute':fields.integer('Battute'),
                
                
                }
mrp_production()  

