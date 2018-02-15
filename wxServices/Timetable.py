# coding=utf-8
from XmlrpclibUtil import XmlrpclibUtil
import json

class Timetable:
	def getSessions(self,request):

		res = XmlrpclibUtil().search_read('op.session',
			[[]],
			{'fields': ['name', 'start_datetime', 'end_datetime', 'course_id'], 'limit': 10})

		return json.dumps({'success':True, 'result':res, 'msg':''})

	# 获取课程表的开始和结束小时
	def getTimingStartEnd(self,request):

		res_timing = XmlrpclibUtil().search_read('op.timing',
			[[]],
			{'fields': ['name', 'am_pm', 'hour', 'minute'], 'limit': 100})

		# UNDO 待实现,暂时用假数据返回
		res_mock = {'startHour':8,'endHour':18}
		res = res_mock

		return json.dumps({'success':True, 'result':res, 'msg':''})