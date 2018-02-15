# coding=utf-8
from XmlrpclibUtil import XmlrpclibUtil
import json

class Faculty:
	def getFacultyById(self,request):

		res = XmlrpclibUtil().search_read('op.faculty',
			[[('id', '=', request.args.get('faculty_id'))]],
			{'fields': ['name', 'gender', 'phone', 'birth_date'], 'limit': 10})

		return json.dumps({'success':True, 'result':res, 'msg':''})


	def insertFaculty(self,request):
		id = XmlrpclibUtil().create('op.faculty',json.loads(request.data))

		return json.dumps({'success': True, 'result': {'id': id}, 'msg': ''})