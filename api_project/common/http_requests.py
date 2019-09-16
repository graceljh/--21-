# -*- coding: utf-8 -*-
# @Time    : 2019/8/31 18:39
# @File    : http_request.py
# @Software: PyCharm
#@author：liu
import requests
"""
封装的目的：
1、是为了根据用力中的请求方法，来巨鼎发起什么类型的请求
2、输出login日志
"""
class HTTPRequest(object):
	def request(self,method,url,data,headers=None):
		method=method.lower()
		if method=='post':
			#判断是否使用json来传参(适用于项目中接口参数有使用json传参的）
			return requests.post(url=url,data=data,headers=headers)
		elif method=='get':
			return requests.get(url=url, params=data, headers=headers)

class HTTPSession(object):
	#使用session对象发送请求，自动记录cookies信息
	def __init__(self):
		self.session=requests.session()
	def request(self, method, url, data, headers=None):
		method = method.lower()
		if method == 'post':
			# 判断是否使用json来传参(适用于项目中接口参数有使用json传参的）
			return self.session.post(url=url, data=data, headers=headers)
		elif method == 'get':
			return self.session.get(url=url, params=data, headers=headers)
	def close(self):#一定要记得关闭session
		self.session.close()