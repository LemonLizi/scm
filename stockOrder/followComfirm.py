
from main import ApiAutomation, base_url, headers
from stockOrder import createStockorder
from stockOrder.createStockorder import getStockOrder
from stockOrder.stockOrderList import stockOrderList

followComfirm = ApiAutomation(base_url, headers)

# 发送POST请求,将已经创建成功的备货单号做为入参，输入对应SKU对应的预计单价，完成跟单确认操作
post_data = {
    "stockUpFollowConfirmItemList": [
            {
                "stockUpOrderNo": getStockOrder()[0],
                "stockUpPrice": 10.30,
                "followRemark": "Python自动接单",
                "version": getStockOrder()[1]
            }
            ]
    }
api_url = "scm/scm/stockup/followConfirm"
post_response = followComfirm.post_request(api_url, post_data)
if (post_response['code'] == 'SUCCESS') :
    print("备货单：" + post_data['stockUpFollowConfirmItemList'][0]['stockUpOrderNo'] + "跟单确认操作成功")
else:
    print(post_response['message'])