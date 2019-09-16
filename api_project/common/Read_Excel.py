# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 22:27
# @File    : Read_excel.py
# @Software: PyCharm
#@author：liu
#将excel数据存为对象，通过对象调用属性值的方法，使用excel数据
#获取excel数据时，使用列表推导式，精简代码

import openpyxl
class CaseData(object):
	def __init__(self,zip_obj):
		for i in list(zip_obj):#遍历传递的参数
			setattr(self,i[0],i[1])#反射机制设置实例属性，表头作为属性名称，其他行作为属性值
#setattr(object, name, value)object -- 对象。name -- 字符串，对象属性。value -- 属性值
#定义一个专门读取excel的类
class ReadExcel(object):
	#读取excel中的文件
	def __init__(self,file_name,sheet_name):
		"""
		:param file_path: excel文件名
		:param sheet_name: excel表单名
		"""
		self.file_name=file_name
		self.sheet_name=sheet_name

	def open(self):
		# 打开文件，返回一个工作簿对象
		self.wb = openpyxl.load_workbook(self.file_name)
		# 通过工作簿，选择表单对象
		self.sh =self.wb[self.sheet_name]
	def read_data_obj(self):
		#打开文件和表单
		self.open()
		#创建一个列表cases,存放所有的用例数据
		cases=[]
		#读取文件中的数据
		rows=list(self.sh.rows)
		#获取表头，使用列表推导式，将第一行数据作为表头
		title=[row.value for row in rows[0]]
		#遍历其他的数据行，和表头进行打包，转换为字典，放到cases这个列表中
		for row in rows[1:]:
			data=[r.value for r in row]
			zip_obj=zip(title,data)
			#通过Case类来创建一个对象，传了一个参数zip_obj
			case_data=CaseData(zip_obj)
			cases.append(case_data)
		return cases

	def write_data(self,row,column,value):
		'''
		:param row: 写入的行
		:param column: 写入的列
		:param value: 写入的值
		:return:
		'''
		self.open()
		#按照传入的行、列、内容进行写入
		self.sh.cell(row=row,column=column,value=value)
		#保存
		self.wb.save(self.file_name)


if __name__=="__main__":
	pass
	cases=ReadExcel(r"C:\Users\sks\api_project\data\cases1.xlsx","add").read_data_obj()
	for i in cases:
		print(i.excepted)
		#print(i.data)
	print(type(cases))
	#print(cases)