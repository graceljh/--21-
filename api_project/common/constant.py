# -*- coding: utf-8 -*-
# @Time    : 2019/8/31 11:18
# @File    : constant.py
# @Software: PyCharm
#@author：liu
import os
"""
常量模块，获取项目目录的路径，保存

项目路径：
用例类所在的路径
配置文件的路径
用例数据的路径
日志文件的路径
测试报告的路径
"""
#公共模块所在的目录
print(__file__)
res=os.path.dirname(__file__)
print(res)
#项目目录的路径
BASE_DIR=os.path.dirname(os.path.dirname(__file__))
print(BASE_DIR)

#测试用例所在的目录路径
CASES_DIR=os.path.join(BASE_DIR,"testcases")
print(CASES_DIR)

#测试报告所在的目录路径
REPORT_DIR=os.path.join(BASE_DIR,"reports")

#日志文件所在的目录路径
LOG_DIR=os.path.join(BASE_DIR,"logs")

#配置文件所在的目录路径
CONF_DIR=os.path.join(BASE_DIR,"conf")

#测试报告所在的目录路径
DATA_DIR=os.path.join(BASE_DIR,"data")



