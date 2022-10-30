from getNPV import getNPVforMaturity
from fromExcel import fromExcel
from greeks import greeks

if __name__ == "__main__":
    # getworkingdate=getWorkingDate('2022-10-05','2021-04-22',10)
    # getnpv=getNPVforMaturity('2022-09-29(')
    # getswapcontract=swapContracts('2021-04-22','2022-10-05',10,10000000000,3.82,1)

    contractInfo = {'contractDate': '2022-09-28', 'swapRate': 3.885, 'notional': 10000000000, 'tenor': 10,'direction':-1}
    getnpv = getNPVforMaturity('2022-09-29', contractInfo)
    fromexcel = fromExcel()
    greeks = greeks()

    #cfList = getnpv.get_CFdays('2022-09-29', 10)
    # 이걸 가지고 날짜들사이의 날짜 뽑을 수 있는지 확인
    print(fromexcel.getSwapRatePlus10bp())
    #print(getnpv.getSwapNPV())
    #print(greeks.getPlus10bp())


'''
def getDate(start, end):
    start = datetime.strptime(start, '%Y%m%d')
    end = datetime.strptime(end, '%Y%m%d')
    dates = [(start + timedelta(days=i)).strftime('%Y%m%d') for i in range((end - start).days + 1)]
    print(dates)
    dates = [stock.get_nearest_business_day_in_a_week(d) for d in dates]
    print(dates)
    return dates

print(getDate('20220930','20221231'))
'''