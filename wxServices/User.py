# -*- coding: utf-8 -*-

# from .utils.Utils import Utils
from XmlrpclibUtil import XmlrpclibUtil
import json
import urllib,urllib2
import time
import random
import os


class User(object):

	# 获取微信平台第三方Session，并保存到服务器路径下
	def getSession(self,request):

		code = request.args.get("code")

		url='https://api.weixin.qq.com/sns/jscode2session'
		textmod ={'appid':'wx0c968d297f10614b','secret':'c37e47687189473eebe7d3459aa5a0b3','grant_type':'authorization_code','js_code':code}
		textmod = urllib.urlencode(textmod)
		print(textmod)
		#输出内容:password=admin&user=admin
		req = urllib2.Request(url = '%s%s%s' % (url,'?',textmod))
		res = urllib2.urlopen(req)
		res = res.read()
		print(res)
		res = json.loads(res)
		#输出内容:登录成功
		#生成第三方session
		openid = res["openid"]
		session_key = res["session_key"]
		session_time = time.localtime( time.time())
		#本地的session key采用时间+随机数
		rand = random.randrange (10000000,99999999,1)
		third_session = str(session_time.tm_yday)+"_"+str(session_time.tm_hour)+str(session_time.tm_min)+"_"+str(rand)

		#需要将session存储到data目录下
		#保存位置  TODO global
		path = "D:/workspace/odoo/data/third_sessions/"
		fileName =  path + third_session + ".session"
		file = open( fileName, "w")
		file.write(openid+","+session_key)
		file.close()

		


		return json.dumps({"third_session":third_session})


	#读取session并判断是否过期
	def chkSession(self,third_session):

		# 查询session，如果查询不到返回false,如果能够查询判断是否过期，如果没有过期返回true，如果过期返回false
		#保存位置  TODO global
		path = "D:/workspace/odoo/data/third_sessions/"
		fileName =  path + third_session + ".session"
		if(os.path.exists(fileName)):
			t_file = os.path.getctime(fileName)
			t_curr = time.time()
			t_diff =  t_curr - t_file
			t_max = 1000 # TODO global
			print "t_diff---------------------->:"+str(t_diff)
			if (t_diff < t_max):
				file = open( fileName, "r")
				file_context = file.read()
				file.close()
				
				openid = file_context.split(",")[0] 

				return openid
			else:
				return None
		else:
			return None

	#获取微信openid绑定的用户信息及角色
	def getUserByOpenid(self,request):

		session = request.args.get("session")
		openid = User().chkSession(session)

		#获取用户信息
		wxusers = XmlrpclibUtil().search_read('wx.user',[[('wx_openid','=',openid)]],{'fields':['id','user_id','wx_nickname','wx_city','phone','addr']})
		if(len(wxusers) == 0):
			return None

		userid = wxusers[0]['user_id'][0]

		print '-----------------------users-------------------------'
		print userid

		#获取角色信息
		users = XmlrpclibUtil().search_read('res.users',[[('id','=',userid)]],{'fields':['id','name','groups_id']})
		if(len(users) == 0):
			return None
		groupids = users[0]['groups_id']


		return json.dumps({'wxuser':wxusers[0], 'user':users[0]})


