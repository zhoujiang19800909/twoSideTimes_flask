# coding=utf-8
from XmlrpclibUtil import XmlrpclibUtil
import json

class Register:

	def getOdooUserByOpenid(self,request):
		res_wxuser = XmlrpclibUtil().search_read('weixin.user',
			[[('wx_openid', '=', request.args.get('openid'))]],
			{'fields': ['wx_openid', 'wx_nickname', 'user_type', 'student_id','parent_id','faculty_id','employee_id'], 'limit': 1})
		print "-------------res_wxuser-------------"
		print res_wxuser
		#获取不同用户类型的信息
		if len(res_wxuser) > 0:
			user_type = res_wxuser[0]['user_type']
			if user_type == 'student':
				res_students = XmlrpclibUtil().search_read('op.student',
				[[('id', '=', res_wxuser[0].get('student_id')[0])]],
				{'fields': ['name', 'gender', 'phone', 'birth_date', 'image_small'],'limit': 1})

				res_student = res_students[0]
				res_student['image_small'] = 'data:image/png;base64,' + res_student['image_small'].replace("\n", "%0A")
				return json.dumps({'success': True, 'result': res_student, 'msg': '', 'rowCnt':1})
			if user_type == 'parent':
				res_parent = XmlrpclibUtil().search_read('op.parent',
				[[('id', '=', res_wxuser[0].get('parent_id')[0])]],
				# TODO 需要继承partner
				{'fields': ['name', 'gender', 'phone', 'birth_date', 'image_small'],'limit': 1})
				# {'fields': ['name', 'gender', 'phone', 'birth_date', 'image_small'],'limit': 1})

				res_parent = res_parent[0]
				res_parent['image_small'] = 'data:image/png;base64,' + res_parent['image_small'].replace("\n", "%0A")
				return json.dumps({'success': True, 'result': res_parent, 'msg': '', 'rowCnt':1})
			if user_type == 'faculty':
				res_faculty = XmlrpclibUtil().search_read('op.faculty',
				[[('id', '=', res_wxuser[0].get('faculty_id')[0])]],
				{'fields': ['name', 'gender', 'phone', 'birth_date', 'image_small'],'limit': 1})

				res_faculty = res_faculty[0]
				res_faculty['image_small'] = 'data:image/png;base64,' + res_faculty['image_small'].replace("\n", "%0A")
				return json.dumps({'success': True, 'result': res_faculty, 'msg': '', 'rowCnt':1})
			if user_type == 'employee':
				res_employee = XmlrpclibUtil().search_read('hr.employee',
				[[('id', '=', res_wxuser[0].get('employee_id')[0])]],
				{'fields': ['name', 'gender', 'phone', 'birth_date', 'image_small'],'limit': 1})

				res_employee = res_employee[0]
				res_employee['image_small'] = 'data:image/png;base64,' + res_employee['image_small'].replace("\n", "%0A")
				return json.dumps({'success': True, 'result': res_employee, 'msg': '', 'rowCnt':1})
		else:
			return json.dumps({'success': True, 'result': {}, 'msg': '', 'rowCnt':0})


	def insertWxuser(self,request):
		id = XmlrpclibUtil().create('weixin.user', json.loads(request.data))

		return json.dumps({'success':True, 'result':{'id':id}, 'msg':''})




    
