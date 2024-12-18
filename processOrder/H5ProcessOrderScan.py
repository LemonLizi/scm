from main import ApiAutomation, base_url, Auth2

from processOrder.processProcedures import get_process_order

processOrderScan = ApiAutomation(base_url, auth=Auth2)


#飞书H5进行加工单对应的工序加工操作步骤
def processing_produce():
    #第一步：获取扫码加工单号得到对应待加工工序的数据
    processOrderNo = get_process_order()["processOrder"]
    post_data = {
        "processOrderNo": processOrderNo
    }
    api_url = 'scm/scm/h5/processOrderScan/getH5ProcessOrderScanDetail'
    post_response = processOrderScan.post_request(api_url, post_data)
    print(post_response)
    if post_response['code'] == 'SUCCESS':
        #processOrderId = post_response['data']['processOrderId']
        receiptNum = post_response['data']['processNum']
        processOrderProcedures = post_response['data']['processOrderProcedures']
        #processOrderId = ['data']['processOrderId']

        #第二步，加工单进行所有工序的逐个确认接货-开始加工-完成加工操作
        for item in processOrderProcedures:
            processOrderProcedureId = item['processOrderProcedureId']
            print(f"加工工序: {processOrderProcedureId}")

            #2.1：工序进行确认接货操作：默认接货数=加工单对应的加工数
            post_data = {
                "processOrderProcedureId": processOrderProcedureId,
                "processOrderNo": processOrderNo,
                "receiptNum": receiptNum
            }
            api_url = 'scm/scm/processOrderScan/confirmReceive'
            post_response = processOrderScan.post_request(api_url, post_data)
            if post_response['code'] == 'SUCCESS':
                print(f"确认接货成功: {processOrderProcedureId}")

                #2.2：加工单当前工序进行开始加工操作
                post_data = {
                    "processOrderNo": processOrderNo,
                    "processOrderProcedureId": processOrderProcedureId
                }
                api_url = 'scm/scm/h5/processOrderScan/beginProcedure'
                post_response = processOrderScan.post_request(api_url, post_data)
                if post_response['code'] == 'SUCCESS':
                    print(f"开始加工成功: {processOrderProcedureId}")


                    # 第四步，加工单当前工序完成加工操作成功
                    post_data = {
                        "processOrderProcedureId": processOrderProcedureId,
                        "processOrderNo": processOrderNo,
                        "qualityGoodsCnt": receiptNum,
                        "defectiveGoodsCnt": 0
                    }
                    api_url = 'scm/scm/processOrderScan/completeProcedure'
                    post_response = processOrderScan.post_request(api_url, post_data)
                    if post_response['code'] == 'SUCCESS':
                        print(f"完成加工成功: {processOrderProcedureId}")
                    """    
                    else:
                        print(f"完成加工失败: {processOrderProcedureId}")
                else:
                    print(f"开始加工失败: {processOrderProcedureId}")
            else:
                print(f"确认接货失败: {processOrderProcedureId}")
            """
        return {"processOrderNo": processOrderNo}
    else:
        return {"error": "Failed to processing produces by page", "response": post_response}


#加工单进行完工交接操作
def finish_handover():
    #第一步：通过加工单列表获取加工单对应的加工单号Id,当前加工单的版本号
    processOrderNoList = processing_produce()['processOrderNo']
    post_data = {
         "pageNo": 1,
         "pageSize": 50,
         "processOrderNoList": [processOrderNoList]
    }
    api_url = 'scm/scm/processOrder/getByPage'
    post_response = processOrderScan.post_request(api_url, post_data)
    if post_response['code'] == 'SUCCESS':
        processOrderId = post_response['data']['records'][0]['processOrderId']
        version = post_response['data']['records'][0]['version']

        #加工单进行完工交接操作：绑定JG01仓库空闲容器与加工单Id
        post_data = {
            "containerCode": "RQJG0100010",
             "processOrderId": processOrderId,
             "version": version
        }
        api_url = 'scm/scm/processOrder/completeHandover'
        post_response = processOrderScan.post_request(api_url, post_data)
        if post_response['code'] == 'SUCCESS':
            print(f"加工单完工交接成功: {processOrderNoList}")

        """
        else:
            print(f"加工单完工交接失败: {processOrderNoList}")
        """

        return {"processOrderNo": processOrderNoList}

    else:
        return {"error": "Failed to get processDetails by page", "response": post_response}

processing_produce()
finish_handover()