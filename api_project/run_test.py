# -*- coding: utf-8 -*-
# @Time    : 2019/8/31 9:51
# @File    : run_test.py
# @Software: PyCharm
#@author：liu
import unittest
import os
import time
from HTMLTestRunnerNew import HTMLTestRunner
from common.my_logging import log
from common.constant import CASES_DIR,REPORT_DIR
log.info("正在开启测试运行程序")
#创建测试套件
suite=unittest.TestSuite()
#将用例添加到套件中
loader=unittest.TestLoader()
suite.addTest(loader.discover(CASES_DIR))
#now=time.strftime("%Y-%m-%d %H-%M-%S")
#拼接测试报告的路径
#report_file_path=os.path.join(REPORT_DIR,now+"_reports.html")
report_file_path=os.path.join(REPORT_DIR,"reports.html")
#执行测试用例
with open(report_file_path,"wb") as fb:
	runner=HTMLTestRunner(stream=fb,
						  verbosity=2,
						  title="21期接口项目",
						  description="项目实战",
						  tester="graceljh")
	runner.run(suite)
log.info("所有用例执行完毕")