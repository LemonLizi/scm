import datetime

import requests
import json

from main import ApiAutomation, base_url, headers
from stockOrder import stockOrderList
from stockOrder.stockOrderList import stockOrder_List

# 初始化类
createStockorder = ApiAutomation(base_url, headers)

# 定义要求回货时间日期字段
date_str = '2024-11-20'
# 将日期字符串转换为 datetime 对象
date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
# 设置时间为 23:59:59
end_of_day = date_obj.replace(hour=23, minute=59, second=59)
# 将 datetime 对象转换为秒级时间戳
timestamp_seconds = end_of_day.timestamp()
# 转换为毫秒级别时间戳
timestamp_milliseconds = int(timestamp_seconds * 1000)
print("要求回货时间对应时间戳为:", timestamp_milliseconds)

# 发送POST请求,创建半成品备货单，输入商品SKU，下单数，供应商code进行下单

post_data = {
    "stockUpCreateItemList": [
        {
            "sku": "MU4501361387",
            "skuEncode": "20240422lrltest",
            "placeOrderCnt": 2,
            "supplierCode": '123',
            "requestReturnGoodsDate": timestamp_milliseconds
        }
    ]
}
api_url = "scm/scm/stockup/createStockUp"
post_response = createStockorder.post_request(api_url, post_data)
print(post_response['code'])
#print("接口入参要求回货时间对应时间戳为:", post_data['requestReturnGoodsDate'])
if (post_response['code'] == 'SUCCESS') :

    print("创建备货单成功,备货单号为：" + stockOrder_List()[0] + '，状态=' + stockOrder_List()[2])

else:
    print("创建备货单失败" + post_response['message'])
    #获取当前没有绑定对照关系的SKU和供应商code
    def getSku():
        unbindSku = post_data['stockUpCreateItemList'][0]['sku']
        unbindSupplier = post_data['stockUpCreateItemList'][0]['supplierCode']
        unbindSkuEncode = post_data['stockUpCreateItemList'][0]['skuEncode']
        return unbindSku, unbindSupplier, unbindSkuEncode
