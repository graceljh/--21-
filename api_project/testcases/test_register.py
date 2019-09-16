# -*- coding: utf-8 -*-
# @Time    : 2019/9/2 16:47
# @File    : test_register.py
# @Software: PyCharm
#@author：liu
import unittest
import os
import random
from pack_lib.ddt import ddt,data
from common.Read_Excel import ReadExcel
from common.http_requests import HTTPRequest
from common.my_logging import log
from common.constant import DATA_DIR
from common.do_mysql import ReadSQL
from common.config import myconf
from common.text_replace import replace
@ddt
class RegisterTestCase(unittest.TestCase):
	"""注册接口"""
	excel=ReadExcel(os.path.join(DATA_DIR,"cases1.xlsx"),"register")
	cases=excel.read_data_obj()
	http=HTTPRequest()  #类属性
	db=ReadSQL()#创建db对象

	@data(*cases)
	def test_case_register(self,case):
		"""登注册接口用例执行的逻辑"""
		#准备测试用例
		url = myconf.get('url','url') + case.url  # 拼接完整的URL地址
		method=case.method
		excepted=eval(case.excepted)
		row=case.case_id + 1
		# 替换用例参数
		case.data = replace(case.data)
		#随机生成手机号码
		phone=self.random_phone()
		print(phone)
		#替换动态化的参数，字符串替换方法
		case.data = case.data.replace("*phone*", phone)#加星号是为了避免替换掉其他的同名字符，如mobilephone
		#发送请求到接口，获取结果
		log.info("正在请求地址{}".format(url))
		response=self.http.request(method=method,url=url,data=eval(case.data))
		res=response.json()

		#对比预期结果
		try:
			self.assertEqual(excepted, res)
			# 判断是否需要进行SQL校验
			if case.check_sql:  # 如果此字段有数据，条件成立
				# 用随机生成的手机号替换需要校验的SQL语句中的手机号
				case.check_sql = case.check_sql.replace('*phone*',phone)
				db_res = self.db.find_count(case.check_sql)
				self.assertEqual(1, db_res)
		except AssertionError as e:
			"""测试用例未通过"""
			self.excel.write_data(row, 8, '未通过')
			log.info("{},该条用例执行未通过".format(case.title))
			log.exception(e)
			raise e
		else:
			self.excel.write_data(row, 8, '通过')
			log.info("{},该条用例执行通过".format(case.title))

	def random_phone(self):
		"""随机生成手机号"""
		while True:
			phone = "13"
			for i in range(9):
				num = random.randint(1, 9)
				phone += str(num)

			# 数据库中查找该手机号是否存在
			sql = "SELECT * FROM member WHERE MobilePhone='{}';".format(phone)
			if not self.db.find_count(sql):
				return phone
