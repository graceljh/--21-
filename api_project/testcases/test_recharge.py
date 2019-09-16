# -*- coding: utf-8 -*-
# @Time    : 2019/9/4 16:25
# @File    : test_recharge.py
# @Software: PyCharm
#@author：liu
import decimal
import unittest
import os
from pack_lib.ddt import ddt,data
from common.Read_Excel import ReadExcel
from common.http_requests import HTTPSession
from common.my_logging import log
from common.constant import DATA_DIR
from common.do_mysql import ReadSQL
from common.config import myconf
from common.text_replace import replace
@ddt
class RechargeTestCase(unittest.TestCase):
	"""充值接口"""
	excel=ReadExcel(os.path.join(DATA_DIR,"cases1.xlsx"),"recharge")
	cases=excel.read_data_obj()
	http=HTTPSession()  #类属性
	db=ReadSQL()#创建db对象

	@data(*cases)
	def test_case_recharge(self,case):
		"""充值接口用例执行的逻辑"""
		#准备测试用例数据
		url = myconf.get('url', "url") + case.url  # 拼接完整的URL地址
		row=case.case_id + 1
		#替换用例参数
		case.data=replace(case.data)
		if case.check_sql:
			case.check_sql=replace(case.check_sql)
			start_money = ReadSQL().find_one(case.check_sql)[0]
			print('充值之前用户的余额为{}'.format(start_money))
		#发送请求到接口，获取结果
		log.info("正在请求地址{}".format(url))
		response=self.http.request(method=case.method,url=url,data=eval(case.data))
		res=response.json()

		#对比预期结果
		try:
			# 判断是否需要进行SQL校验
			if case.check_sql:  # 如果此字段有数据，条件成立
				# 获取充值用例执行之后的余额
				end_money = self.db.find_one(case.check_sql)[0]
				print('充值之后用户的余额为{}'.format(end_money))

				# 获取本次充值的金额
				money = eval(case.data)['amount']
				money = decimal.Decimal(str(money))
				print('本次充值的金额{}'.format(money))
				# 获取数据库变化的金额

				change_money = end_money - start_money
				self.assertEqual(money, change_money)

			self.assertEqual(str(case.excepted_code),res["code"])
		except AssertionError as e:
			"""测试用例未通过"""
			self.excel.write_data(row, 8, '未通过')
			log.info("{},该条用例执行未通过".format(case.title))
			log.exception(e)
			raise e
		else:
			self.excel.write_data(row, 8, '通过')
			log.info("{},该条用例执行通过".format(case.title))
