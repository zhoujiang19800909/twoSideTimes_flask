# coding=utf-8
from flask import Flask, request
import xmlrpclib
import json

from wxServices import Register,Student,Product,Parent,Faculty,Employee,Timetable


app = Flask(__name__)


@app.route('/')
def root():
    return " ----- welcome to shuyun! ----- "

# 获取所有的产品列表
@app.route('/products')
def products():
    return Product().getProducts()

# 根据openid获取用户在Odoo中的用户账号
@app.route('/getOdooUserByOpenid')
def getOdooUserByOpenid():
    return Register().getOdooUserByOpenid(request)

# 根据openid获取用户在Odoo中的用户账号
@app.route('/insertWxuser', methods=['POST'])
def insertWxuser():
    return Register().insertWxuser(request)

# 根据openid获取用户在Odoo中的用户账号	
@app.route('/getStudentById')
def getStudentById():
    return Student().getStudentById(request)

# 创建学生
@app.route('/insertStudent', methods=['POST'])
def insertStudent():
    return Student().insertStudent(request)

# 创建家长
@app.route('/insertParent', methods=['POST'])
def insertParent():
    return Parent().insertParent(request)

# 创建教师
@app.route('/insertFaculty', methods=['POST'])
def insertFaculty():
    return Faculty().insertFaculty(request)

# 创建员工
@app.route('/insertEmployee', methods=['POST'])
def insertEmployee():
    return Employee().insertEmployee(request)

# 查询课程表
@app.route('/getSessions', methods=['GET'])
def getSessions():
    return Timetable().getSessions(request)

# 查询课程表时间段
@app.route('/getTimingStartEnd', methods=['GET'])
def getTimingStartEnd():
    return Timetable().getTimingStartEnd(request)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=5000)
    