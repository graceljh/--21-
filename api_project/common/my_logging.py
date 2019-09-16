# -*- coding: utf-8 -*-
# @Time    : 2019/8/27 20:32
# @File    : 日志封装.py
# @Software: PyCharm
#@author：liu

import logging
from common.config import myconf
import os
from common.constant import LOG_DIR
log_level=myconf.get("log","log_level")
sh_level=myconf.get("log","s_level")
fh_level=myconf.get("log","f_level")
name=myconf.get("log","filename")
#拼接日志文件路径
file_path=os.path.join(LOG_DIR,name)

class Mylogging(object):
	def __new__(cls,*args,**kwargs):
		#第一步：创建一个日志收集器，设置收集的等级
		mylog=logging.getLogger("my_log")
		mylog.setLevel(log_level)
		#第二步：创建日志输出渠道，设置输出等级
		sh=logging.StreamHandler()
		sh.setLevel(sh_level)

		fh=logging.FileHandler(file_path,encoding="utf8")
		fh.setLevel(fh_level)

		#第三步：将日志收集器和输出渠道进行绑定
		mylog.addHandler(sh)
		mylog.addHandler(fh)
		#指定日志输出格式
		fot="%(asctime)s- [%(filename)s-->line:%(lineno)d]-%(levelname)s:%(message)s"
		#创建日志格式对象
		formatter=logging.Formatter(fot)
		#输出格式绑定的输出渠道
		sh.setFormatter(formatter)
		fh.setFormatter(formatter)
		return mylog
#创建一个日志收集器对象
log=Mylogging()
if __name__=="__main__":
	log.debug("---debug等级的日志，一般用于调试")
	log.info("---info等级的日志，常规信息的输出")
	log.warning("---warning等级的日志，警告信息")
	log.error("---error等级的信息，错误信息")
	log.critical("---critical等级的信息，严重的错误，程序要崩溃")