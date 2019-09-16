# -*- coding: utf-8 -*-
# @Time    : 2019/9/16 15:45
# @File    : test_websevice.py
# @Software: PyCharm
#@author：liu
from suds import client

#创建一个webservice对象，来调用webservice里面的各类接口
user_url = "http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl"  # 这里是你的webservice访问地址
c = client.Client(url=user_url)
# Client里面直接放访问的URL，可以生成一个webservice对象
#打印出这个wsdl地址里面的所有接口信息：
print(c)  # 打印所webservice里面的所有接口方法名称，结果如下截图所示：


#利用soapui来看看webservice某个接口的组成和参数
#如何传递参数值：
data = {"client_ip": 1, "tmpl_id": "1", "mobile": "15388887681"}  # 用字典的方式传值
res=c.service.sendMCode(data)
print(res)
#
# #如何在Python中调用注册这个接口服务：
# result = client.service.userRegister(t)
# # client这个对象 ，调用service这个方法，然后再调用userRegister这个接口函数，函数里面传递刚刚我们准备
# # 好的得参数字典 t
# print(result)  # 打印返回结果
