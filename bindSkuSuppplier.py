from main import ApiAutomation, base_url, headers
from stockOrder import createStockorder

#定义SKU与供应商对照关系绑定的类
getCompareDate = ApiAutomation(base_url, headers)
#先获得需要绑定SKU的当前已绑定的对照关系的数据
post_data1 = {
    "sku": createStockorder.getSku()[0]
}
api_url1 = "scm/scm/supplierProductCompare/getDetail"
post_response1 = getCompareDate.post_request(api_url1, post_data1)
print(post_response1['code'])
if (post_response1['code'] == 'SUCCESS') :
    #print(post_response['data']['cycle'])
    #定义一个方法，提取绑定对照关系中需要用到的参数数据
    def getSkuSupplier():
        plmSkuId = post_response1['data']['plmSkuId']
        singleCapacity = post_response1['data']['singleCapacity']
        version = post_response1['data']['version']
        return plmSkuId, singleCapacity, version
    #print(getSkuSupplier())
else:
    print(post_response1['message'])


print(getSkuSupplier()[0],getSkuSupplier()[1],getSkuSupplier()[2])
bindSkuSupplier = ApiAutomation (base_url, headers)
post_data2 = {
    "supplierProductCompareEditList":[
        {
            "supplierCode": createStockorder.getSku()[1],
            "supplierProductName": createStockorder.getSku()[2],
            "type": 'controlled'
        }
        ],
    "plmSkuId": getSkuSupplier()[0],
    "singleCapacity": getSkuSupplier()[1],
    "version": getSkuSupplier()[2]
}
api_url2 = "scm/scm/supplierProductCompare/edit"
post_response2 = bindSkuSupplier.post_request(api_url2, post_data2)
print(post_data2)
print(post_response2)