# -*- coding: utf-8 -*-
# @Time    : 2019/8/31 9:58
# @File    : test_login.py
# @Software: PyCharm
#@author：liu
"""
测试用例模块
"""
import unittest
import os
import random
from pack_lib.ddt import ddt,data
from common.Read_Excel import ReadExcel
from common.http_requests import HTTPRequest
from common.my_logging import log
from common.constant import DATA_DIR
from common.config import myconf
from common.text_replace import replace
@ddt
class LoginTestCase(unittest.TestCase):
	"""登录接口"""
	excel=ReadExcel(os.path.join(DATA_DIR,"cases1.xlsx"),"login")
	cases=excel.read_data_obj()
	http=HTTPRequest()  #类属性

	@data(*cases)
	def test_case_login(self,case):
		"""登录接口用例执行的逻辑"""
		#准备测试用例
		url=myconf.get('url',"url")+case.url#字符串连接用+
		#url=case.url
		#data=eval(case.data)
		method=case.method
		excepted=eval(case.excepted)
		row=case.case_id + 1
		# 替换用例参数
		# if "#phone#" in case.data:   #手机号和密码都要替换，这样比较繁琐，封装正则类来替换
		# 	case.data.replace("#phone#",myconf.get("data","phone"))
		data=replace(case.data)
		#发送请求到接口，获取结果
		log.info("正在请求地址{}".format(url))
		response=self.http.request(method=method,url=url,data=eval(data))
		res=response.json()
		#对比预期结果
		#self.assertEqual(excepted,res)
		try:
			self.assertEqual(excepted,res)
		except AssertionError as e:
			"""测试用例未通过"""
			self.excel.write_data(row, 8, '未通过')
			log.debug("{},该条用例执行未通过".format(case.title))
			log.error(e)
			raise e
		else:
			self.excel.write_data(row, 8, '通过')
			log.debug("{},该条用例执行通过".format(case.title))

