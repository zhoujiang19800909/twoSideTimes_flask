# coding=utf-8
from XmlrpclibUtil import XmlrpclibUtil
import json

class Parent:
	def getParentById(self,request):

		res = XmlrpclibUtil().search_read('op.parent',
			[[('id', '=', request.args.get('parent_id'))]],
			{'fields': ['name', 'gender', 'phone', 'birth_date'], 'limit': 10})

		return json.dumps({'success':True, 'result':res, 'msg':''})


	def insertParent(self,request):
		id = XmlrpclibUtil().create('op.parent',json.loads(request.data))

		return json.dumps({'success': True, 'result': {'id': id}, 'msg': ''})