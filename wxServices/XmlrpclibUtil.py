# coding=utf-8

import xmlrpclib
import json

# TODO 放到Util目录中
class XmlrpclibUtil(object):
	# 数据库连接信息
	root = 'http://%s:%d/xmlrpc/' % ("127.0.0.1", 8069)
	db = "odoorun"
	user = "504351365@qq.com"
	password = "123456"
	models = xmlrpclib.ServerProxy(root + 'object',allow_none=True)
	uid = xmlrpclib.ServerProxy(root + 'common').login(db, user, password)

	# models.execute_kw(db,uid,password,'op.student','unlink',[[21,22,23,24,25,26,27,28,29,30,31,33]])
	# print "deleted success"

	def search_read(self,model,filters,fields):
		return self.models.execute_kw(self.db, self.uid, self.password, model, 'search_read', filters, fields)


	def create(self,model,data):
		print "---------------------create-------------------"
		print data
		print type(data)
		id = self.models.execute_kw(self.db, self.uid, self.password, model, 'create', [data])
		return id

	def update(self,model,id,data):
		print "---------------------update-------------------"
		self.models.execute_kw(self.db, self.uid, self.password, model, 'write', [[id],data])


	def search_count(self,model,filters):
		print "---------------------search_count-------------------"
		return self.models.execute_kw(self.db, self.uid, self.password, model, 'search_count', filters)

