# codin=utf-8

# from .utils.Utils import Utils
from XmlrpclibUtil import XmlrpclibUtil
import json

class Product(object):
	print object	

	def getProducts(self):

		res_product = XmlrpclibUtil().search_read('product.product',[],
			{'fields': ['name', 'display_name', 'weight', 'image_small'], 'limit': 10})

		for res in res_product:
			if res['image_small']:
				res['image_small'] = 'data:image/png;base64,' + res['image_small'].replace("\n", "%0A")
			else:
				res['image_small'] = ''

		return json.dumps({'success':True,'result':res_product,'msg':''})          





