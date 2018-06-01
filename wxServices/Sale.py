# coding=utf-8

# from .utils.Utils import Utils
from XmlrpclibUtil import XmlrpclibUtil
from User import User
from operator import itemgetter, attrgetter
from Product import Product
import json
import time 

# TODO 查询方法对表封装


class Sale(object):
	print object	

	# 获取订单列表 用户
	def getOrders(self,request):

		session = request.args.get("session")
		openid = User().chkSession(session)

		sale_orders = XmlrpclibUtil().search_read('sale.order',[[('wx_openid','=',openid)]],
			{'fields': ['id','name','amount_total','confirmation_date','date_order','order_line','state','validity_date','currency_id',
        'date_order',
        'status',
        'name',
        'partner_id',
        'partner_invoice_id',
        'partner_shipping_id',
        'pricelist_id'],'order':'name'})

		for order in sale_orders:
			order['orderNo'] = order['name']
			order['bookTime'] = order['validity_date']
			order['sum'] = order['amount_total']
			order['cnt'] = len(order['order_line'])
			order['statusName'] = Sale().convertStatusName(order['status'])
			print 'statusName:'+order['statusName']

		# print res_product
		return json.dumps(sale_orders)

	#获取订单明细
	def getOrderDetail(self,request):

		id = request.args.get("id")
		print "id---------------------"
		print id

		sale_orders = XmlrpclibUtil().search_read('sale.order',[[('id','=',id)]],
			{'fields': ['id','name','status','amount_total','confirmation_date','create_date','date_order','order_line','state','validity_date','take_no','take_time'],'order':'name'})

		orderDetail = {}
		orderDetail['id'] = sale_orders[0]['id']
		orderDetail['orderNo'] = sale_orders[0]['name']
		orderDetail['createTime'] = sale_orders[0]['create_date']
		orderDetail['takeTime'] = sale_orders[0]['take_time']
		orderDetail['sumMonney'] = sale_orders[0]['amount_total']
		orderDetail['cupNumber'] = len(sale_orders[0]['order_line'])
		orderDetail['status'] = sale_orders[0]['status']
		orderDetail['takeNo'] = sale_orders[0]['take_no']

		sale_order_line = XmlrpclibUtil().search_read('sale.order.line',[[('id','in',sale_orders[0]['order_line'])]],
			{'fields': ['id','product_id','product_uom_qty','price_unit','price_total','product_uom','state','display_name'],'order':'product_id'})

		cartList = []
		for orderLine in sale_order_line:
			orderLine['name'] = orderLine['display_name']
			orderLine['orderNum'] = orderLine['product_uom']
			orderLine['cnt'] = orderLine['product_uom_qty']
			orderLine['sum'] = orderLine['price_total']
			cartList.append(orderLine)

		orderDetail['cartList'] = cartList

		return json.dumps(orderDetail)

	# 生成订单
	def createOrder(self,request):
		print 'createOrder'
		print request
		
		session = request.args.get("session")
		openid = User().chkSession(session)

		data = json.loads(request.data)

		# 生成取餐号：四位数的字符串 当天订单数+1 
		count = XmlrpclibUtil().search_count('sale.order',[[('validity_date','=',data['validityDate']),('company_id','=',3)]])
		count = count + 1
		if (count < 10): 
			takeNo = 'A000'+str(count)
		elif (count < 100): 
			takeNo = 'A00'+str(count)
		elif (count < 1000): 
			takeNo = 'A0'+str(count)
		else:
			takeNo = 'A'+str(count)


		
		saleOrderData = {
			'currency_id':21,
	        'partner_id':212,
	        'partner_invoice_id':212,
	        'partner_shipping_id':212,
	        'company_id': 3,
	        'validity_date':data['validityDate'],
	        'take_time':data['takeTime'],
	        'amount_total':data['sumMonney'],
	        'amount_untaxed':data['sumMonney'],
	        'state':'sale',
	        'wx_openid':openid,
	        'take_no':takeNo
			}

		print 'saleOrderData-------------------------------'
		print saleOrderData
		saleOrderId = XmlrpclibUtil().create('sale.order',saleOrderData)
		# id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name': "New Partner",}])

		saleOrderlineDatas = []
		for cart in data['cartList']:
			# print cart
			saleOrderlineData = {
				'order_id':saleOrderId,
				'name':cart['name'],
				'price_unit':cart['list_price'],
				'product_id':cart['id'],
				'product_uom':1,
				'product_uom_qty':cart['cnt'],
				'state':'sale',
				'order_partner_id':212,
				'wx_openid':openid
			}
			# saleOrderlineDatas.append(saleOrderlineData)
			line_id = XmlrpclibUtil().create('sale.order.line',saleOrderlineData)
			saleOrderlineDatas.append(line_id)
		print "saleOrderlineDatas-------------------------------------"
		# print saleOrderlineDatas
		# XmlrpclibUtil().update('sale.order',saleOrderId,{'order_line':saleOrderlineDatas,'amount_total':data['sumMonney']})

		order = XmlrpclibUtil().search_read('sale.order',[[('id','=',saleOrderId)]],{'fields': ['name']})
		orderNo = order[0]['name']

		return json.dumps({'orderId':saleOrderId,'takeNo':takeNo,'orderNo':orderNo})

	# 获取客服的订单列表 
	def getServiceOrderList(self,request):

		session = request.args.get("session")
		validityDate = request.args.get("validityDate")

		print "validityDate:"+validityDate

		openid = User().chkSession(session)

		if(validityDate == 'all'):
			sale_orders = XmlrpclibUtil().search_read('sale.order',[[('status','=','1'),('company_id','=',3)]],
				{'fields': ['id','name','amount_total','confirmation_date','date_order','order_line','status','validity_date',
				'currency_id','partner_id','partner_invoice_id','partner_shipping_id','pricelist_id'],'order':'name'})
		if(validityDate != 'all'):
			sale_orders = XmlrpclibUtil().search_read('sale.order',[[('status','=','1'),('company_id','=',3),('validity_date','=',validityDate)]],
				{'fields': ['id','name','amount_total','confirmation_date','date_order','order_line','status','validity_date',
				'currency_id','partner_id','partner_invoice_id','partner_shipping_id','pricelist_id'],'order':'name'})


		for order in sale_orders:
			order['orderNo'] = order['name']
			order['bookTime'] = order['validity_date']
			order['sum'] = order['amount_total']
			order['cnt'] = len(order['order_line'])
			order['statusName'] = Sale().convertStatusName(order['status'])


			sale_order_line = XmlrpclibUtil().search_read('sale.order.line',[[('id','in',order['order_line'])]],
			{'fields': ['id','product_id','product_uom_qty','price_unit','price_subtotal','product_uom','state','display_name'],'order':'product_id'})

			foodList = []
			for orderLine in sale_order_line:
				orderLine['name'] = orderLine['display_name']
				orderLine['orderNum'] = orderLine['product_uom']
				orderLine['cnt'] = orderLine['product_uom_qty']
				orderLine['sum'] = orderLine['price_subtotal']
				# 获取可购数量
				
				print "--------------------getServiceOrderList-------------------"
				print orderLine
				orderNumData = json.loads(Product().getOrderNumberForFood(orderLine['product_id'][0],order['validity_date']))
				order_left_number = orderNumData['order_left_number']
				orderLine['orderLeftNumber'] = order_left_number


				foodList.append(orderLine)

			order['foodList'] = foodList


		print sale_orders
		# 使用operator包进行排序
		sale_orders.sort(key = lambda x:x["bookTime"])

		# print res_product
		return json.dumps(sale_orders)

	# 获取订单的统计信息
	def getOrderSts(self,request):

		validityDate = request.args.get("validityDate")

		if(validityDate == 'all'):
			cnt_all = XmlrpclibUtil().search_count('sale.order',[[('company_id','=',3)]])
			cnt_uncheck = XmlrpclibUtil().search_count('sale.order',[[('status','=','1'),('company_id','=',3)]])
			cnt_checked = XmlrpclibUtil().search_count('sale.order',[[('status','=','2'),('company_id','=',3)]])
			cnt_done = XmlrpclibUtil().search_count('sale.order',[[('status','=','3'),('company_id','=',3)]])
			cnt_untake = XmlrpclibUtil().search_count('sale.order',[[('status','=','4'),('company_id','=',3)]])
			cnt_taken = XmlrpclibUtil().search_count('sale.order',[[('status','=','5'),('company_id','=',3)]])
			cnt_uncancel = XmlrpclibUtil().search_count('sale.order',[[('status','=','6'),('company_id','=',3)]])
			cnt_canceled = XmlrpclibUtil().search_count('sale.order',[[('status','=','7'),('company_id','=',3)]])
		else:
			cnt_all = XmlrpclibUtil().search_count('sale.order',[[('company_id','=',3),('validity_date','=',validityDate)]])
			cnt_uncheck = XmlrpclibUtil().search_count('sale.order',[[('status','=','1'),('company_id','=',3),('validity_date','=',validityDate)]])
			cnt_checked = XmlrpclibUtil().search_count('sale.order',[[('status','=','2'),('company_id','=',3),('validity_date','=',validityDate)]])
			cnt_done = XmlrpclibUtil().search_count('sale.order',[[('status','=','3'),('company_id','=',3),('validity_date','=',validityDate)]])
			cnt_untake = XmlrpclibUtil().search_count('sale.order',[[('status','=','4'),('company_id','=',3),('validity_date','=',validityDate)]])
			cnt_taken = XmlrpclibUtil().search_count('sale.order',[[('status','=','5'),('company_id','=',3),('validity_date','=',validityDate)]])
			cnt_uncancel = XmlrpclibUtil().search_count('sale.order',[[('status','=','6'),('company_id','=',3),('validity_date','=',validityDate)]])
			cnt_canceled = XmlrpclibUtil().search_count('sale.order',[[('status','=','7'),('company_id','=',3),('validity_date','=',validityDate)]])

		return json.dumps({'cnt_all':cnt_all,'cnt_uncheck':cnt_uncheck,'cnt_checked':cnt_checked,'cnt_done':cnt_done,
			'cnt_untake':cnt_untake,'cnt_taken':cnt_taken,'cnt_uncancel':cnt_uncancel,'cnt_canceled':cnt_canceled})

	# 获取订单的统计信息
	def getOrderLineSts(self,request):

		validityDate = request.args.get("validityDate")

		if(validityDate == 'all'):
			orders = XmlrpclibUtil().search_read('sale.order',[[('status','=','2'),('company_id','=',3)]],
				{'fields': ['id'],'order':'product_id'})
		else:
			orders = XmlrpclibUtil().search_read('sale.order',[[('status','=','2'),('company_id','=',3),('validity_date','=',validityDate)]],
				{'fields': ['id'],'order':'product_id'})

		orderIds = []
		for order in orders:
			orderIds.append(order['id'])

		cnt_all = XmlrpclibUtil().search_count('sale.order.line',[[('company_id','=',3),('order_id','in',orderIds)]])
		cnt_uncheck = XmlrpclibUtil().search_count('sale.order.line',[[('status','=','1'),('company_id','=',3),('order_id','in',orderIds)]])
		cnt_todo = XmlrpclibUtil().search_count('sale.order.line',[[('status','=','2'),('company_id','=',3),('order_id','in',orderIds)]])
		cnt_done = XmlrpclibUtil().search_count('sale.order.line',[[('status','=','3'),('company_id','=',3),('order_id','in',orderIds)]])

		return json.dumps({'cnt_all':cnt_all,'cnt_uncheck':cnt_uncheck,'cnt_todo':cnt_todo,'cnt_done':cnt_done})

	# 获取店员的订单列表 
	def getWaiterOrderList(self,request):

		session = request.args.get("session")
		openid = User().chkSession(session)

		validityDate = request.args.get("validityDate")

		if(validityDate == 'all'):
			# sale_orders = XmlrpclibUtil().search_read('sale.order',[[('status','=','4'),('company_id','=',3)]],
			sale_orders = XmlrpclibUtil().search_read('sale.order',[[('status','=','4'),('company_id','=',3)]],
			{'fields': ['id','name','amount_total','confirmation_date','date_order','order_line','status','validity_date',
			'currency_id','date_order','name','partner_id','partner_invoice_id','partner_shipping_id','pricelist_id'],'order':'name'})
		else:
			# sale_orders = XmlrpclibUtil().search_read('sale.order',[[('status','=','4'),('company_id','=',3),('validity_date','=',validityDate)]],
			sale_orders = XmlrpclibUtil().search_read('sale.order',[[('status','=','4'),('company_id','=',3),('validity_date','=',validityDate)]],
			{'fields': ['id','name','amount_total','confirmation_date','date_order','order_line','status','validity_date',
			'currency_id','date_order','name','partner_id','partner_invoice_id','partner_shipping_id','pricelist_id'],'order':'name'})



		

		for order in sale_orders:
			order['orderNo'] = order['name']
			order['bookTime'] = order['validity_date']
			order['sum'] = order['amount_total']
			order['cnt'] = len(order['order_line'])

			sale_order_line = XmlrpclibUtil().search_read('sale.order.line',[[('id','in',order['order_line'])]],
			{'fields': ['id','product_id','product_uom_qty','price_unit','price_subtotal','product_uom','state','display_name'],'order':'product_id'})

			foodList = []
			for orderLine in sale_order_line:
				orderLine['name'] = orderLine['display_name']
				orderLine['orderNum'] = orderLine['product_uom']
				orderLine['cnt'] = orderLine['product_uom_qty']
				orderLine['sum'] = orderLine['price_subtotal']
				foodList.append(orderLine)

			order['foodList'] = foodList


		print sale_orders
		# 使用operator包进行排序
		sale_orders.sort(key = lambda x:x["bookTime"])

		# print res_product
		return json.dumps(sale_orders)

	# 获取厨师的取餐日期	
	def getChefValidityDates(self,request):
		takeTimes = XmlrpclibUtil().search_read('sale.order',[[('status','=','2'),('company_id','=',3),('take_time','!=',None)]],
			{'fields':['validity_date'],'order':'validity_date' })

		validityDates = ['all']
		for takeTime in takeTimes:
			if takeTime['validity_date'] not in validityDates:
				validityDates.append(takeTime['validity_date'])


		return json.dumps(validityDates)

	# 获取厨师的订单列表 
	def getChefOrderList(self,request):
		res_orders = []
		categorys = json.loads(Product().getFoods(request))

		validityDate = request.args.get("validityDate")
		print "------------------------------getChefOrderList----------------------------------------"
		print validityDate

		#获取目录
		for category in categorys:
			foods = category['foods']
			res_foods = []
			#获取食物
			for food in foods:
				#获取订单明细
				lines = XmlrpclibUtil().search_read('sale.order.line',[[('product_id','=',food['id']),('status','=','2')]],
				{'fields': ['id','order_id','product_id','product_uom_qty','price_unit','price_subtotal','product_uom','state','display_name'],'order':'product_id'})

				res_lines = []
				print "getChefOrderList lines"
				print lines

				if len(lines)>0:
					for line in lines:
						# 按日期过滤订单
						if(validityDate=='all'):
							order = XmlrpclibUtil().search_read('sale.order',[[('id','=',line['order_id'][0])]], 
							{'fields': ['id','name','status','memo','validity_date'],'order':'name'})
						else:
							order = XmlrpclibUtil().search_read('sale.order',[[('id','=',line['order_id'][0]),('validity_date','=',validityDate)]], 
							{'fields': ['id','name','status','memo','validity_date'],'order':'name'})
						print "getChefOrderList order"
						print order
						#插入符合条件的订单明细
						if(len(order)>0):
							line['orderNo'] = order[0]['name']
							line['takeTime'] = order[0]['validity_date']
							line['memo'] = order[0]['memo']
							res_lines.append(line)
					#插入符合条件的物品
					if(len(res_lines)>0):
						food['lines'] = res_lines
						food['foodId'] = food['id']
						food['open'] = True
						food['hasMemo'] = False

						res_foods.append(food)
			res_orders.append({'name':category['name'],'foods':res_foods})

		return json.dumps(res_orders)



	# 修改订单状态
	def changeOrderStatus(self,request):

		data = json.loads(request.data)
		status = data['status']
		orderId = data['orderId']

		print "changeOrderStatus"
		print data

		XmlrpclibUtil().update('sale.order',orderId,{'status':status})

		# 确认时 同步修改订单明细的状态
		if(status == '2'):
			orderLine = data['orderLine']
			for lineId in orderLine:
				XmlrpclibUtil().update('sale.order.line',lineId,{'status':status})


		return json.dumps({})

	# 修改订单明细状态
	def changeOrderLineStatus(self,request):
		data = json.loads(request.data)
		orderId =  data['orderId']
		lineId =  data['lineId']
		status = data['status']

		XmlrpclibUtil().update('sale.order.line',lineId,{'status':status})

		# 判断是否修改订单状态
		count = XmlrpclibUtil().search_count('sale.order.line',[[('order_id','=',orderId),('status','=','2')]])
		
		if(count == 0):          
			XmlrpclibUtil().update('sale.order',orderId,{'status':status})

		return json.dumps({})

	#保存订单二维码
	def saveQRCodeToOrder(self,request):
		data = json.loads(request.data)
		orderId =  data['orderId']
		aqrcode =  data['base64']

		XmlrpclibUtil().update('sale.order',orderId,{'wx_aqrcode':aqrcode})

		return json.dumps({})







	#获取statusName
	def convertStatusName(self,status):
		if status == '1':
			return '待确认'
		if status == '2':
			return '已确认'
		if status == '3':
			return '已制作'
		if status == '4':
			return '待取餐'
		if status == '5':
			return '已取餐'
		if status == '6':
			return '待取消'
		if status == '7':
			return '已取消'










