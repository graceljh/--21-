# -*- coding: utf-8 -*-
# @Time    : 2019/9/3 21:32
# @File    : do_mysql.py
# @Software: PyCharm
#@author：liu
"""
为什么要封装？方便使用
封装的需求是什么？对应的逻辑代码封装成方法，关键的数据做参数化处理
"""
import pymysql
from common.config import myconf
class ReadSQL(object):
	'''操作mysql的类'''
	def __init__(self):
		# 第一步，连接到数据库，创建游标
		self.conn = pymysql.connect(host=myconf.get("mysql","host"),  # 数据库地址
							port=myconf.getint("mysql","port"),  # 端口
							user=myconf.get("mysql","user"),
							password=myconf.get("mysql","password"),
							database=myconf.get("mysql","database"),  # 数据库名
							charset="utf8"#指定编码格式
							   )
		# 创建游标
		self.cur = self.conn.cursor()
	def close(self):
		#关闭游标
		self.cur.close()
		#断开连接
		self.conn.close()
	def find_one(self,sql):
		#查询一条数据
		self.conn.commit()
		self.cur.execute(sql)
		return self.cur.fetchone()
	def find_all(self,sql):
		#返回所有的结果
		self.conn.commit()
		self.cur.execute(sql)
		return self.cur.fetchall()
	def find_count(self,sql):
		self.conn.commit()#一定要记得提交修改
		count=self.cur.execute(sql)
		return count

if __name__=="__main__":
	sql = "select LeaveAmount from member where mobilephone = '15677889600';"
	sql2 = "SELECT * FROM member LIMIT 5;"
	sql3="select RegName from member where mobilephone = '15677889600';"
	db=ReadSQL()
	RES=db.find_one(sql)
	a=float(RES[0])
	print(RES)#返回的是元组，因此要取元组的第一个值，就是[0]
	print(RES[0])
	# b=ReadSQL().find_count(sql)
	# print(b)
