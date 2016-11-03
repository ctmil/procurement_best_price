from openerp import models, fields, api, _
from openerp.osv import osv
from openerp.exceptions import except_orm, ValidationError
from StringIO import StringIO
import urllib2, httplib, urlparse, gzip, requests, json
import openerp.addons.decimal_precision as dp
import logging
import datetime
from openerp.fields import Date as newdate

#Get the logger
_logger = logging.getLogger(__name__)

class product_product(osv.osv):
	_inherit = 'product.product'

	def _select_seller(self, cr, uid, product_id, partner_id=False, quantity=0.0, date=time.strftime(DEFAULT_SERVER_DATE_FORMAT), uom_id=False, context=None):
        	if context is None:
	           context = {}
		seller_list = []
	        res = self.pool.get('product.supplierinfo').browse(cr, uid, [])
        	for seller in product_id.seller_ids:
	                # Set quantity in UoM of seller
       	        	quantity_uom_seller = quantity
			if quantity_uom_seller and uom_id and uom_id != seller.product_uom:
				quantity_uom_seller = uom_id._compute_qty_obj(uom_id, quantity_uom_seller, seller.product_uom)

			if seller.date_start and seller.date_start > date:
				continue
			if seller.date_end and seller.date_end < date:
				continue
			if partner_id and seller.name not in [partner_id, partner_id.parent_id]:
				continue
			if quantity_uom_seller < seller.qty:
				continue
			if seller.product_id and seller.product_id != product_id:
				continue

			#res |= seller
			seller_list.append(res)
		min_price = 999999999
	        res = self.pool.get('product.supplierinfo').browse(cr, uid, [])
		for seller in seller_list:
			if seller.price < min_price:
				res = seller
				min_price = seller.price
		res |= seller		
	        return res

