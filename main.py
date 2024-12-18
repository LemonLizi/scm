# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


#def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.#
#    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
#    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import requests
import json

#API请求类定义
class ApiAutomation:
    def __init__(self, base_url, auth):
        self.base_url = base_url
        #self.headers = headers
        self.headers = {
            "Content-Type": "application/json",
            "hetectx-authorization": auth
        }

    def get_request(self, endpoint, requests=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers)
        #API的响应体response通过.json()将API中json格式返参由json格式反序列化为Python的字典格式
        return response.json()

    def post_request(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        #request.post的请求体data通过json.dumps()将python语句中的dict-字典序列化为接口的json格式
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        return response.json()



#公共网关请求头和账号鉴权信息的获取
# 使用示例
base_url = "https://bit-test.htwig.com:30023/api"
#Auth = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyQ29kZSI6IlUwOTMyMjQiLCJpYXQiOjE3MzEyOTMyMzYsImV4cCI6MTczMTM3OTc1Nn0.SYkqNb7PWtNNJdRu8SXZb31sRQodGM2nOSzHl47_-Eo"

Auth1 = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyQ29kZSI6IlUwNDQwNzIiLCJpYXQiOjE3MzE5ODIwMjQsImV4cCI6MTczMjA2ODU0NH0.iuhOQLtbRuhlIMC9WxdSkEI18QhzrzxXO0zCEYwNXzE"  #SCM页面操作端使用的用户鉴权
Auth2 = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyQ29kZSI6IlUwNDQwNzIiLCJpYXQiOjE3MzE5ODIwMjQsImV4cCI6MTczMjA2ODU0NH0.iuhOQLtbRuhlIMC9WxdSkEI18QhzrzxXO0zCEYwNXzE"  #飞书-H5工序加工环节使用的用户鉴权
