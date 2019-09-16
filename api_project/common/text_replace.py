# -*- coding: utf-8 -*-
# @Time    : 2019/9/7 11:04
# @File    : text_replace.py
# @Software: PyCharm
#@author：liu
''''''
"""
封装一个替换数据的方法

封装的需求：
1、替换用例中的参数
2、简化替换的流程


实现思路：
1、获取用例数据
2、判断该条用例数据是否有需要替换的数据
3、对数据进行替换

"""
import re
from common.config import myconf
class ConText:
	"""用来（临时）保存接口之间依赖参数的类"""
	pass

def replace(data):
	while re.search(r"#(.+?)#",data):
		res =re.search(r"#(.+?)#",data)
		#提取要替换的内容
		r_data=res.group()
		#print(r_data)
		#获取要替换的字段
		key=res.group(1)
		#print(key)
		# 去配置文件中读取字段对应的数据
		#捕获异常，如果在配置文件中没有找到固定的值,就去临时变量里找
		try:
			value=myconf.get("data",key)
		except:
			value=getattr(ConText,key)
		#进行替换
		data=re.sub(r_data,str(value),data)#re.sub(正则式，替换的字符串，被替换的原始字符串）
	return data


if __name__=="__main__":
	s2='{"mobilephone"="#phone#","pwd"="#pwd#","regname"="#name#}'
	data=replace(s2)
	print(data)
	#给对象设置一个属性：对象（类）属性名 属性值
	setattr(ConText,"memberid",1999)
	print(ConText.memberid)
	#获取对象的属性：对象 属性名
	id=getattr(ConText,"memberid")
	print(id)