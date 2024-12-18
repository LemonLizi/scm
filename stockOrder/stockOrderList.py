from main import ApiAutomation, base_url, headers

stockOrderList = ApiAutomation(base_url, headers)

#发送POST请求，查询刚刚创建成功的备货单号
post_data = {
    "pageNo": 1,
    "pageSize": 50
    }
api_url = "scm/scm/stockup/searchStockUp"
post_response = stockOrderList.post_request(api_url, post_data)
if (post_response['code'] == 'SUCCESS') :
    print(post_response)
    def stockOrder_List():
            stockUpOrderNo = post_response['data']['records'][0]['stockUpOrderNo']
            version = post_response['data']['records'][0]['version']
            stockUpOrderStatusRemark = post_response['data']['records'][0]['stockUpOrderStatusRemark']
            return stockUpOrderNo, version, stockUpOrderStatusRemark
    print("备货单号：" + stockOrder_List()[0] )
else:
    print(post_response['message'])
