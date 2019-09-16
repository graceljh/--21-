# -*- coding: utf-8 -*-
# @Time    : 2019/8/28 22:02
# @File    : config.py
# @Software: PyCharm
#@author：liu
from configparser import ConfigParser
from common.constant import CONF_DIR
import os
switch_file_path=os.path.join(CONF_DIR,"env.ini")
class MyConfig(ConfigParser):
	def __init__(self):
		super().__init__()
		c=ConfigParser()
		s=c.read(switch_file_path,encoding='utf8')
		env=c.getint('env','switch')
		#根据开关的值，分别去读取不同环境的配置文件
		if env==1:
		#初始化的时候，打开配置文件(要转码到utf8，否则会报错)
			self.read(os.path.join(CONF_DIR,"conf.ini"),encoding='utf8')
		elif env==2:
			self.read(os.path.join(CONF_DIR, "conf1.ini"), encoding='utf8')
		else:
			self.read(os.path.join(CONF_DIR, "conf.ini"), encoding='utf8')

myconf=MyConfig()
# def myconfig():
# 	conf=ConfigParser()
# 	conf.read(r'C:\Users\sks\api_project\common\config.py',encoding='utf8')
# 	return conf
# myconf=MyConfig()