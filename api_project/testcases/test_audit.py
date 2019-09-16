# -*- coding: utf-8 -*-
# @Time    : 2019/9/2 16:47
# @File    : test_register.py
# @Software: PyCharm
#@author：liu
import unittest
import os
from pack_lib.ddt import ddt,data
from common.Read_Excel import ReadExcel
from common.http_requests import HTTPSession
from common.my_logging import log
from common.constant import DATA_DIR
from common.do_mysql import ReadSQL
from common.config import myconf
from common.text_replace import ConText
from common.text_replace import replace
@ddt
class AuditTestCase(unittest.TestCase):
	"""审核接口"""
	excel=ReadExcel(os.path.join(DATA_DIR,"cases1.xlsx"),"audit")
	cases=excel.read_data_obj()
	http=HTTPSession()  #类属性
	db=ReadSQL()#创建db对象

	@data(*cases)
	def test_case_audit(self,case):
		"""审核接口用例执行的逻辑"""
		#准备测试用例
		url = myconf.get('url','url') + case.url  # 拼接完整的URL地址
		row=case.case_id + 1
		# 替换用例参数
		case.data = replace(case.data)

		# 判断是否有*memberId*的参数需要替换
		if "*loan_id*" in case.data:
			max_id = self.db.find_one("select max(id) from loan")[0]  # findone()返回的是元组，要加下标才能获取到元素
			loan_id = max_id + 1  # 在数据库中查找到最大的id号，加1后替换给*memberId*
			case.data = case.data.replace("*loan_id*", str(loan_id))

		#发送请求到接口，获取结果
		log.info("正在请求地址{}".format(url))
		response=self.http.request(method=case.method,url=url,data=eval(case.data))
		res=response.json()
		print(res)

		#判断是否是执行的加标用例
		if case.interface=="加标":
			loan_id = self.db.find_one(
				"select id from loan where memberId ='{}' order by id desc".format(myconf.get("data","memberId")))[0]
			#"SELECT Id FROM loan WHERE MemberId='{}' ORDER BY id DESC".format(myconf.get('data', 'memberId')))
		# 将添加的标id，保存为临时变量
			setattr(ConText, 'loan_id', loan_id)#对象（类）属性名 属性值

		#对比预期结果
		try:
			self.assertEqual(str(case.excepted_code),res['code'])
			# 判断是否需要进行SQL校验
			if case.check_sql:
				case.check_sql = replace(case.check_sql)#要记的把参数化的sql语句替换为实际的值
				#获取返回的状态码
				status = self.db.find_one(case.check_sql)[0]#查询语句默认返回的是元组，要加下标
				self.assertEqual(eval(case.data)["status"], status)

		except AssertionError as e:
			"""测试用例未通过"""
			self.excel.write_data(row, 8, '未通过')
			log.info("{},该条用例执行未通过".format(case.title))
			log.exception(e)
			raise e
		else:
			self.excel.write_data(row, 8, '通过')
			log.info("{},该条用例执行通过".format(case.title))
