# coding=utf-8
from flask import Flask, request
import xmlrpclib
import json

from wxServices import Product,Sale,User


app = Flask(__name__)


@app.route('/')	
def root():
    return " ----- welcome to shuyun! ----- "

# 获取seesionKey
@app.route('/getSession')
def getSession():
	return User().getSession(request)

#获取用户信息
@app.route('/getUserByOpenid')
def getUserByOpenid():
	return User().getUserByOpenid(request)

# 获取所有的产品列表
@app.route('/getFoods')
def products():
    return Product().getFoods(request)

# 获取所有的订单列表
@app.route('/getOrders')
def getOrders():
    return Sale().getOrders(request)

# 获取所有的订单列表
@app.route('/getOrderDetail')
def getOrderDetail():
    return Sale().getOrderDetail(request)

# 创建订单
@app.route('/createOrder', methods=['POST'])
def createOrder():
    return Sale().createOrder(request)

# 获取客服的订单列表 
@app.route('/getServiceOrderList')
def getServiceOrderList():
    return Sale().getServiceOrderList(request)

# 获取订单统计结果
@app.route('/getOrderSts')
def getOrderSts():
    return Sale().getOrderSts(request)

# 获取订单明旭的统计结果
@app.route('/getOrderLineSts')
def getOrderLineSts():
    return Sale().getOrderLineSts(request)

# 获取店员的订单列表 
@app.route('/getWaiterOrderList')
def getWaiterOrderList():
    return Sale().getWaiterOrderList(request)

# 获取厨师的订单列表 
@app.route('/getChefValidityDates')
def getChefValidityDates():
    return Sale().getChefValidityDates(request)

# 获取厨师的订单列表 
@app.route('/getChefOrderList')
def getChefOrderList():
    return Sale().getChefOrderList(request)

# 修改订单状态 
@app.route('/changeOrderStatus', methods=['POST'])
def changeOrderStatus():
    return Sale().changeOrderStatus(request)

# 修改订单状态 
@app.route('/changeOrderLineStatus', methods=['POST'])
def changeOrderLineStatus():
    return Sale().changeOrderLineStatus(request)

# 保存订单二维码 
@app.route('/saveQRCodeToOrder', methods=['POST'])
def saveQRCodeToOrder():
    return Sale().saveQRCodeToOrder(request)



if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=5000)
    	