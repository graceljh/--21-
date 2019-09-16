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
from common.text_replace import replace
@ddt
class AddTestCase(unittest.TestCase):
	"""加标接口"""
	excel=ReadExcel(os.path.join(DATA_DIR,"cases1.xlsx"),"add")
	cases=excel.read_data_obj()
	http=HTTPSession()  #类属性
	db=ReadSQL()#创建db对象

	@data(*cases)
	def test_case_add(self,case):
		"""加标接口用例执行的逻辑"""
		#准备测试用例
		url = myconf.get('url','url') + case.url  # 拼接完整的URL地址
		row=case.case_id + 1
		# 替换用例参数
		case.data = replace(case.data)
		#判断是否有*memberId*的参数需要替换
		if "*memberId*" in case.data:
			max_id=self.db.find_one("select max(id) from member")[0]#findone()返回的是元组，要加下标才能获取到元素
			memberid=max_id+1#在数据库中查找到最大的id号，加1后替换给*memberId*
			case.data=case.data.replace("*memberId*",str(memberid))#字符串替换的方法，要记得转换类型为str，否则会报错
		#判断是否需要SQL校验
		if case.check_sql:#如果case文件里的check_sql有数据，就做替换。
			case.check_sql= replace(case.check_sql)#调用封装好的替换类，把其中含有“#memberId#"的替换为从配置文件中获取的值
			# 获取当前用户加标前的标数量
			start_count = self.db.find_count(case.check_sql)

		#发送请求到接口，获取结果
		log.info("正在请求地址{}".format(url))
		response=self.http.request(method=case.method,url=url,data=eval(case.data))
		res=response.json()

		#对比预期结果
		try:
			self.assertEqual(str(case.excepted_code),res["code"])
			# 判断是否需要进行SQL校验
			if case.check_sql:
				# 获取当前用户加标后的标数量
				end_count = self.db.find_count(case.check_sql)
				self.assertEqual(1, end_count-start_count)
		except AssertionError as e:
			"""测试用例未通过"""
			self.excel.write_data(row, 8, '未通过')
			log.info("{},该条用例执行未通过".format(case.title))
			log.exception(e)
			raise e
		else:
			self.excel.write_data(row, 8, '通过')
			log.info("{},该条用例执行通过".format(case.title))
