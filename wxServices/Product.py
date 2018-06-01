# coding=utf-8

# from .utils.Utils import Utils
from XmlrpclibUtil import XmlrpclibUtil
# from Sale import Sale

import json

class Product(object):
	# print object	

	def getFood(self,foodId):
		print "------------getFood-----------------"
		print id
		food = XmlrpclibUtil().search_read('product.template',[[('id','=',foodId)]],
				{'fields': ['id','name','image_small','list_price','order_max_number','description_sale'],'order':'name'})

		return json.dumps({'food':food})




	def getFoods(self,request):

		validityDate = request.args.get("validityDate")

		# print '-----------------------getFoods----------------------------'
		# print validityDate


		categorys = XmlrpclibUtil().search_read('product.category',[],
			{'fields': ['id','name','type'],'order':'name'})

		res_foods = []
		for category in categorys:
			foodList = {'name':{},'foods':[]}
			print "---------------------getFoods--------------------------"
			print validityDate
			if(validityDate == 'all'):

				foods = XmlrpclibUtil().search_read('product.template',[[('categ_id','=',category['id']),('company_id','=',3)]],
					{'fields': ['id','name','image_small','list_price','order_max_number','description_sale'],'order':'name'})
			else:

				foods = XmlrpclibUtil().search_read('product.template',[[('categ_id','=',category['id']),('company_id','=',3),('order_date_start','<=',validityDate),('order_date_end','>=',validityDate)]],
					{'fields': ['id','name','image_small','list_price','order_max_number','description_sale'],'order':'name'})

			print "foods-------------->>>"
			# print foods

			if len(foods) > 0:
				foodList['name'] = category['name']
				for food in foods:
					if food['image_small']:
						food['image_small'] = 'data:image/png;base64,' + food['image_small'].replace("\n", "%0A")
					else:
						food['image_small'] = ''

					# 调用Sale的方法,计算可订购数量
					res = json.loads(Product().getOrderNumberForFood(food['id'],validityDate))
					# print 'res'
					# print res
					food['leftNumber'] = food['order_max_number'] - res['sum_order'] 
					#处理描述为空的情况
					if (food['description_sale'] == False):
						food['description_sale'] = ""



				foodList['foods'] = foods
				res_foods.append(foodList)

				print res_foods


		# print res_product
		return json.dumps(res_foods)

	# 按日期获取产品的已订购数量
	def getOrderNumberForFood(self,foodId,validityDate):

		# print 'getOrderNumberForFood'
		# print foodId
		# print validityDate
		# print 'getOrderNumberForFood end'

		#先根据validityDate获取SaleOrder	
		if(validityDate == 'all'):
			orders = XmlrpclibUtil().search_read('sale.order',[[('status','in',['2','3','4','5'])]],{'fields':['id','name']})
		else:
			orders = XmlrpclibUtil().search_read('sale.order',[[('validity_date','=',validityDate),('status','in',['2','3','4','5'])]],{'fields':['id','name']})
		sum_order = 0

		#再根据product_id获取每个SaleOrder中获取line数量，进行累加 	
		for order in orders:
			orderId = order['id']
			cnt_order = XmlrpclibUtil().search_count('sale.order.line',[[('product_id','=',foodId),('order_id','=',orderId)]])
			sum_order = sum_order + cnt_order

		print "getOrderNumberForFood----------------------"
		print foodId
		
		food = json.loads(Product().getFood(foodId))
		print food,foodId
		order_max_number = 888

		if(len(food['food'])>=1):
			order_max_number = food['food'][0]['order_max_number']

		order_left_number = order_max_number - sum_order




		return json.dumps({'sum_order':sum_order,'order_max_number':order_max_number,'order_left_number':order_left_number})

		





