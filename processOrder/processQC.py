import time

from main import ApiAutomation, base_url, Auth2
from processOrder.H5ProcessOrderScan import finish_handover

processQC = ApiAutomation(base_url, auth=Auth2)


#加工单进行质检，共经历以下步骤：完成交接-完成质检-质检审核通过（如果质检单单存在次品）
def process_qc():
    qcSourceOrderNo = finish_handover()['processOrderNo']
    #print("通过加工单：" + qcSourceOrderNo + "查询质检单开始")


    #第一步：通过加工单号查询到对应的质检单
    post_data = {
        "qcSourceOrderNo": qcSourceOrderNo,
        "qcSourceOrderType": "PROCESS_ORDER_NO",
        "pageNo": 1,
        "pageSize": 50
    }
    api_url = 'scm/scm/qc/searchQc'
    post_response = processQC.post_request(api_url, post_data)
    print(post_response)


    # 设置重试机制
    max_retries = 5  # 最大重试次数
    retry_delay = 2  # 每次重试之间的等待时间（秒）

    for attempt in range(max_retries):
        post_response = processQC.post_request(api_url, post_data)

        # 检查接口返回的质检单数据是否为空
        if post_response['code'] == 'SUCCESS' and post_response['data']['records']:
            try:
                qcOrderNo = post_response['data']['records'][0]['qcOrderNo']  #获取质检单数据
                break
            except (KeyError, IndexError) as e:
                return {"error": "qcOrderNo not found in response data", "exception": str(e)}
        else:
            print(f"Attempt {attempt + 1}/{max_retries} - 'records' is empty, retrying...")
            time.sleep(retry_delay)  # 等待一段时间再重试
    else:
        # 如果超过最大重试次数，则返回错误
        return {"error": "Failed to retrieve process material receipt after multiple retries","response": post_response}

    if post_response['code'] == 'SUCCESS':
        try:
            qcOrderNo = post_response['data']['records'][0]['qcOrderNo']  # 获取质检单数据成功
            print(qcOrderNo)
        except (KeyError, IndexError) as e:
            return {"error": "processMaterialReceiptId not found in response data", "exception": str(e)}

        #第二步：加工质检单进行完成交接操作
        post_data = {
            "qcOrderNoList": [qcOrderNo]
        }
        api_url = 'scm/scm/qc/completeHandover'
        post_response = processQC.post_request(api_url, post_data)
        #print(post_data['qcOrderNoList'])
        #print(post_response)
        if post_response['code'] == 'SUCCESS':
            print(f"加工质检单完成交接成功: {qcOrderNo}")

            #第三步：获取加工质检单对应待质检明细数据、质检单Id、质检单对应版本号
            post_data = {
                "qcOrderNo": qcOrderNo
            }
            api_url = 'scm/scm/qc/qcDetail'
            post_response = processQC.post_request(api_url, post_data)
            #print(post_response)
            if post_response['code'] == 'SUCCESS':
                qcDetailHandItemList = post_response['data']['qcDetailHandItemList']
                version = post_response['data']['version']
                qcOrderId = post_response['data']['qcOrderId']
                waitAmount = post_response['data']['amount']   #查询到当前加工质检单对应待质检数量,后续改写质检完成时，有正品、有次品的场景要用
                #print("获取到需要的质检单数据")
                #print(qcDetailHandItemList)
                #print(version)
                #print(qcOrderId)

                for item in qcDetailHandItemList:
                    item['passAmount'] = item['amount']  #将待质检明细中的待质检数量 amount 赋值给质检单的正品数 passAmount
                    #print("看看处理后的质检明细拿到了没有：")
                    #print(qcDetailHandItemList)
                #第四步：加工质检单进行质检完成
                post_data = {
                    "qcOrderId": qcOrderId,
                    "version": version,
                    "qcOperate": "COMPLETED",
                    "qcDetailHandItemList": qcDetailHandItemList,
                    "qcUnPassDetailItemList": []
                }
                api_url = 'scm/scm/qc/completedQc'
                post_response = processQC.post_request(api_url, post_data)
                #print("质检完成接口请求成功了吗")
                if post_response['code'] == 'SUCCESS':
                    print(f"加工质检单质检完成操作成功: {qcOrderNo}")
                else:
                    return post_response
            else:
                return post_response
        else:
            return post_response

        return {"qcOrderNo": qcOrderNo}
    else:
        return {"error": "Failed to get qcOrder by page", "response": post_response}

print(process_qc())