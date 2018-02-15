# coding=utf-8
from XmlrpclibUtil import XmlrpclibUtil
import json

class Student:
	def getStudentById(self,request):

		res = XmlrpclibUtil().search_read('op.student',
			[[('id', '=', request.args.get('student_id'))]],
			{'fields': ['name', 'gender', 'phone', 'birth_date'], 'limit': 10})

		return json.dumps({'success':True, 'result':res, 'msg':''})


	def insertStudent(self,request):
		id = XmlrpclibUtil().create('op.student',json.loads(request.data))

		return json.dumps({'success': True, 'result': {'id': id}, 'msg': ''})