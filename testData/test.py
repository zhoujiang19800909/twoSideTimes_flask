# -*- coding: UTF-8 -*-
import json

#数组
# l = [1,2,3,4,5,6,7,8]
l = [1,2,3,4,5,6,7,8]
# print type(a)

#json
j = {'name':'zhouj','xb':'男','nl':33}
print j['name']

#json数组
jl = [{'name':'zhouj','xb':'男','nl':33},{'name':'xiel','xb':'女','nl':13}]
for d in jl:
	print d



#两个循环格式
for a in l:
	print a


#写while需注意避免死循环
print "--------------------------------------------"
c = 1
while c < 1000:
	# print c
	d = 2
	flg = True
	while d < c:
		# print c,d,c % d
		if ((c%d == 0)):
			flg = False
		d = d + 1
	if(flg):
			print c

	c = c+ 1