import datetime
import time

from main import ApiAutomation, base_url, Auth1

processProcedures = ApiAutomation(base_url, auth=Auth1)


# 定义期望上架时间日期字段
expect_date = '2024-11-25'
# 将日期字符串转换为 datetime 对象
date_obj = datetime.datetime.strptime(expect_date, '%Y-%m-%d')
# 设置时间为 23:59:59
end_of_day = date_obj.replace(hour=23, minute=59, second=59)
# 将 datetime 对象转换为秒级时间戳
timestamp_seconds = end_of_day.timestamp()
# 转换为毫秒级别时间戳
timestamp_milliseconds = int(timestamp_seconds * 1000)
print("期望上架时间对应时间戳为:", timestamp_milliseconds)


# 创建加工单
def create_process_order():
    post_data = {
            "processOrderType": "OVERSEAS_REPAIR",
            "warehouseCode": "test02",
            "deliverDate": timestamp_milliseconds,
            "sku": "MU7530720720",
            "skuEncode": "Test Produce data Good",
            "processNum": 1,
            "deliveryWarehouseCode": "JY01",
            "productQuality": "GOOD",
            "fileCodeList": [],
            "mainImageUrl": "https://mall-test-pub.htwig.com/plm_sale/1847088153484120064ZemCe1p0FFr6Hezn.jpeg",
            "processOrderMaterials": [
                {
                    "deliveryNum": 1,
                    "sku": "L5-PV-BW-24-NC-G50",
                    "materialSkuTypeRemark": "商品SKU",
                    "materialSkuType": "COMMODITY_SKU"
                }
            ],
            "processOrderProcedures": [
                {
                    "commission": 7,
                    "processId": "1623214274942091265",
                    "sort": 0
                },
                {
                    "commission": 6,
                    "processId": "1623215155074842625",
                    "sort": 1
                }
            ],
            "warehouseName": "test02",
            "warehouseTypeList": [
                "国内自营"
            ],
            "spu": "L11970397",
            "processOrderDescs": [],
            "processOrderItems": [],
            "deliveryWarehouseName": "金塬01仓",
            "platform": "PC001",
            "platCode": "PC001"
    }
    api_url = "scm/scm/processOrder/create"
    post_response = processProcedures.post_request(api_url, post_data)
    if post_response['code'] == 'SUCCESS':
        return post_response
    else:
        return post_response['message']



#获取加工单列表，以获取刚刚创建成功的加工单数据
def get_process_order():
    post_data = {
        "pageNo": 1,
        "pageSize": 50,
        "processOrderTypes": ["LIMITED"]
    }
    api_url = "scm/scm/processOrder/getByPage"
    post_response = processProcedures.post_request(api_url, post_data)
    if post_response['code'] == 'SUCCESS':
        processOrder = post_response['data']['records'][0]['processOrderNo']
        version = post_response['data']['records'][0]['version']
        processOrderStatus = post_response['data']['records'][0]['processOrderStatus']
        return {
            "processOrder": processOrder,
            "version": version,
            "processOrderStatus": processOrderStatus
        }
    else:
        return post_response['message']



#变更加工单为无需排产
def not_need_process_plan():
    post_data = {
        "processOrderNos": [get_process_order()["processOrder"]],
    }
    api_url = "scm/scm/processOrder/updateProcessOrderNeedProcessPlan"
    post_response = processProcedures.post_request(api_url, post_data)
    print(post_data['processOrderNos'])
    if post_response['code'] == 'SUCCESS':
        return post_response
    else:
        return post_response



#加工单对应原料出库:先查询到加工单对应的出库单，先进行加工分拣
def material_picking():
    post_data = {
        "warehouseType": "warehouseCodeList",
        "easySearch": "relatedOrderNoList",
        "easySearchResult": [get_process_order()["processOrder"]],
        "relatedOrderNoList": [get_process_order()["processOrder"]],
        "pageNo": 1,
        "pageSize": 50
    }
    api_url = "wms/deliveryOrder/getByPageForWms"
    post_response = processProcedures.post_request(api_url, post_data)
    print(post_data['easySearchResult'], post_data['relatedOrderNoList'])
    if post_response['code'] == 'SUCCESS':
        deliveryOrderId = post_response['data']['records'][0]['deliveryOrderId']
        deliveryOrderNo = post_response['data']['records'][0]['deliveryOrderNo']
        post_data = {
            "deliveryOrderIdList": [deliveryOrderId]
        }
        api_url = "wms/deliveryOrder/batchCreatePickingOrder"
        post_response = processProcedures.post_request(api_url, post_data)
        if post_response['code'] == 'SUCCESS':
            print("原料出库单：" + deliveryOrderNo + "生成分拣单成功！")
        return {
            "deliveryOrderId": deliveryOrderId,
            "deliveryOrderNo": deliveryOrderNo
        }
    else:
        return post_response



#PDA进行原料分拣单分拣完成：通过出库单查询到分拣单，分拣单查询到对应的分拣单ID
def get_picking_orderId(pickingOrderId=None):
    #第一步:通过出库单入参查询出库单列表数据，获取当前出库单对应的分拣单号
    post_data = {
        "warehouseType": "warehouseCodeList",
        "easySearch": "relatedOrderNoList",
        "easySearchResult": [material_picking()["deliveryOrderNo"]],
        "deliveryOrderNoList": [material_picking()["deliveryOrderNo"]],
        "pageNo": 1,
        "pageSize": 50
    }
    api_url = "wms/deliveryOrder/getByPageForWms"
    post_response = processProcedures.post_request(api_url, post_data)
    #print(post_data['easySearchResult'], post_data['deliveryOrderNoList'])
    targetWarehouseCode = post_response['data']['records'][0]['targetWarehouseCode']
    if post_response['code'] == 'SUCCESS':
        pickingOrderNo = post_response['data']['records'][0]['pickingOrderNo']

        #第二步：获取分拣单号数据成功，发起第二个请求，通过分拣单获取到对应的分拣单Id
        post_data = {
                "pageNo": 1,
                "pageSize": 10,
                "sortByIdAsc": False,
                "pickingOrderNo": pickingOrderNo,
                "operatorUserCode": "",
                "floor": "",
                "deliveryType": "PROCESS",
                "pickingOrderState": [
                    "TO_BE_PICKED",
                    "ONGOING"
                ],
                "warehouseCode": targetWarehouseCode
        }
        api_url = 'wms/pickingOrder/getByPage'
        post_response = processProcedures.post_request(api_url, post_data)
        #print(post_response)
        if post_response['code'] == 'SUCCESS':
            pickingOrderId = post_response['data']['records'][0]['pickingOrderId']
            #print("获取分拣单：" + post_data.pickingOrderNo + '对应分拣单ID成功！')
            return {
                "pickingOrderNo": pickingOrderNo,
                "pickingOrderId": pickingOrderId
            }
    else:
        return post_response


#通过分拣单数据，完成分拣单分拣：分拣单绑定拣货车，获取分拣单对应分拣明细，填写分拣明细对应分拣下架数量，完成分拣操作
#2024-12-10重新编写了分拣单进行分拣下架的逻辑，目前还在验证中
def finish_picking():
    pickingId = get_picking_orderId()["pickingOrderId"]
    pickingOrder = get_picking_orderId()["pickingOrderNo"]
    print("开始绑拣货车：")
    #第一步：分拣单绑定拣货车：拣货车code与分拣单Id进行绑定
    post_data = {
        "pickingCartCode": "JHCJY010402",
        "pickingOrderId": pickingId
    }
    api_url = 'wms/pickingOrder/bindPickingCar'
    post_response = processProcedures.post_request(api_url, post_data)
    print("拣货车绑定成功了")
    if post_response['code'] == 'SUCCESS':
        #print("拣货车：" + post_data.pickingCartCode + "与分拣单：" + pickingOrder + "绑定成功")

        print("查询分拣单的详情")
        #第二步：通过分拣单号查询到分拣单待分拣明细详情
        post_data = {
            "pickingOrderNo": pickingOrder
        }
        api_url = 'wms/pickingOrder/getDetailForPdaByPickingOrderNo'
        post_response = processProcedures.post_request(api_url, post_data)
        print("chaxunchenggong")
        print(post_response)
        if post_response['code'] == 'SUCCESS':
            version = post_response['data']['version']  # 获取当前分拣单对应版本号
            pickingLocations = post_response['data']['pickingLocations']   #获取库位分拣明细

            #对每一个库位的分拣明细进行分拣下架操作：需要对库位里面的批次码明细进行分别下架，等到所有库位里面的所有批次都分拣下架完成才算完成
            for item in pickingLocations:
                waitPickingNum = item['planAmount']  # 获取待分拣数量
                pickingLocationCode = item['pickingLocationCode']  # 获取待分拣库位
                pickingDetails = item['pickingDetails']

                for i in pickingDetails:
                    batchCode = i['batchCode']   #获取库位里面待分拣下架的原料SKU批次码
                    batchPlanAmount = i['planAmount']   #获取库位里面待分拣下架的原料SKU批次码的待分拣数量

                    print(waitPickingNum,pickingLocationCode,batchCode)
                    print("开始分拣明细")

                    #第三步：根据明细，进行分拣单明细数据分拣下架
                    post_data = {
                        "amount": batchPlanAmount,
                        "batchCode": batchCode,
                        "pickingOrderId": pickingId,
                        "warehouseLocation": pickingLocationCode
                    }
                    api_url = 'wms/pickingOrder/pickingOffShelf'
                    post_response = processProcedures.post_request(api_url, post_data)
                    print(post_data['amount'],post_data['batchCode'],post_data['pickingOrderId'],post_data['warehouseLocation'])
                    print("明细分拣完成")
                    print(post_response)
                    if post_response['code'] == 'SUCCESS':
                        print("当前批次分拣完成")

                # 第四步：通过分拣单Id确认当前分拣单已完成分拣
                post_data = {
                    "pickingOrderId": pickingId,
                    "version": version
                }
                api_url = 'wms/pickingOrder/confirmFinish'
                post_response = processProcedures.post_request(api_url, post_data)
                print("分拣完成")
                return post_response
    else:
        return post_response

#出库单签出
def out_board():
    post_data = {
        "deliveryOrderIdList": [material_picking()["deliveryOrderId"]]
    }
    api_url = 'wms/deliveryOrder/batchSignOffConfirm'
    post_response = processProcedures.post_request(api_url, post_data)
    if post_response['code'] == 'SUCCESS':
        print("签出成功")
        return post_response,post_data['deliveryOrderIdList']
    else:
        return post_response


def receipt_material():
    #第一步：通过加工单获取到对应原料收货单ID
    processOrderNo = get_process_order()["processOrder"]
    post_data = {
        "pageNo": 1,
        "pageSize": 50,
        "processOrderNo": processOrderNo
    }
    api_url = 'scm/scm/processMaterialReceipt/getByPage'

    # 设置重试机制
    max_retries = 5  # 最大重试次数
    retry_delay = 2  # 每次重试之间的等待时间（秒）

    for attempt in range(max_retries):
        post_response = processProcedures.post_request(api_url, post_data)
        print(post_response['data'])

        # 检查 'records' 是否为空
        if post_response['code'] == 'SUCCESS' and post_response['data']['records']:
            try:
                processMaterialReceiptId = post_response['data']['records'][0]['processMaterialReceiptId']
                break
            except (KeyError, IndexError) as e:
                return {"error": "processMaterialReceiptId not found in response data", "exception": str(e)}
        else:
            print(f"Attempt {attempt + 1}/{max_retries} - 'records' is empty, retrying...")
            time.sleep(retry_delay)  # 等待一段时间再重试
    else:
        # 如果超过最大重试次数，则返回错误
        return {"error": "Failed to retrieve process material receipt after multiple retries",
                "response": post_response}
    print(post_response['data'])
    if post_response['code'] == 'SUCCESS':
        try:
            processMaterialReceiptId = post_response['data']['records'][0]['processMaterialReceiptId']
        except (KeyError, IndexError) as e:
            return {"error": "processMaterialReceiptId not found in response data", "exception": str(e)}

        #第二步：通过原料收货单ID查询对应的原料收货单详情
        post_data = {
            "processMaterialReceiptId": processMaterialReceiptId
        }
        api_url = 'scm/scm/processMaterialReceipt/detail'
        post_response = processProcedures.post_request(api_url, post_data)
        if post_response['code'] == 'SUCCESS':
            try:
                processMaterialReceiptVersion = post_response['data']['version']
                materialReceiptItems = post_response['data']['materialReceiptItems']
                print(materialReceiptItems)  #打印详情接口返回的原料收货单明细数据

                # 遍历列表中的每个字典：读取收货单需要进行收货的每一个原料SKU的明细数据
                for item in materialReceiptItems:
                    item['receiptNum'] = item['deliveryNum']  # 将 receiptNum 赋值为 deliveryNum 的值：按收货单对应明细进行完全收货处理，那么收货数量需要=出库数量
            except (KeyError, IndexError) as e:
                return {"error": "Failed to retrieve processMaterialReceipt details.", "response": post_response, "exception": str(e)}


            #第三步：进行原料明细收货
            post_data = {
                "version": processMaterialReceiptVersion,
                "processMaterialReceiptId": processMaterialReceiptId,
                "processMaterialReceiptItems": materialReceiptItems
            }
            api_url = 'scm/scm/processMaterialReceipt/confirmReceipt'
            post_response = processProcedures.post_request(api_url, post_data)
            if post_response['code'] == 'SUCCESS':
                params = post_data['processMaterialReceiptItems']
                return {
                    "processMaterialReceiptId": processMaterialReceiptId,
                    "materialReceiptItems": materialReceiptItems, #改写后的原料收货单明细
                    "processMaterialReceiptVersion": processMaterialReceiptVersion,
                    "params": params  #收货单请求确认收货Api时，入参的收货单明细数据
                }
            else:
                return {"error": "Failed to retrieve process material receipt details", "response": post_response}
    else:
        return {"error": "Failed to retrieve process material receipt by page", "response": post_response}


"""
#H5-加工工序完成加工
def processing_produce():
    #第一步：获取扫码加工单号得到对应待加工工序的数据
    processOrderNo = get_process_order()["processOrder"]
    post_data = {
        "processOrderNo": processOrderNo
    }
    api_url = 'scm/scm/h5/processOrderScan/getH5ProcessOrderScanDetail'
    post_response = processProcedures.post_request(api_url, post_data)
    print('post_response')
    if post_response['code'] == 'SUCCESS':
        receiptNum = post_response['data']['maxAvailableReceiptNum']
        processOrderProcedures = post_response['data']['processOrderProcedures']
        #processOrderId = ['data']['processOrderId']

        for item in processOrderProcedures:
            #第二步，加工单进行所有工序的逐个确认接货-开始加工-，操作
            post_data = {
                "processOrderProcedureId": "",
                "processOrderNo": processOrderNo,
                "receiptNum": receiptNum
            }
            api_url = 'scm/scm/processOrderScan/confirmReceive'
            post_response = processProcedures.post_request(api_url, post_data)
"""


print(create_process_order())
print(get_process_order()["processOrder"])
print(not_need_process_plan())
print(material_picking())
print(get_picking_orderId())
print(finish_picking())
print(out_board())
result = receipt_material()
print(result)


