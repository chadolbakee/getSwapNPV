from datetime import datetime, timedelta
from pykrx import stock
from getWorkingDate import getWorkingDate
from getNPV import getNPVforMaturity
import pandas as pd
from swapContracts import swapContracts

if __name__ == "__main__":
    #getworkingdate=getWorkingDate('2022-10-05','2021-04-22',10)
    getnpv=getNPVforMaturity('2022-10-07')
    # getswapcontract=swapContracts('2021-04-22','2022-10-05',10,10000000000,3.82,1)

    #print(getworkingdate.get_CFdaysForEachContract())
    print(getnpv.getDiscountByMaturity())
    # print(getswapcontract.)

    #print(pd.to_datetime('2022-04-01')-pd.to_datetime('2022-01-01'))

'''
def getDate(start, end):
    start = datetime.strptime(start, '%Y%m%d')
    end = datetime.strptim e(end, '%Y%m%d')
    dates = [(start + timedelta(days=i)).strftime('%Y%m%d') for i in range((end - start).days + 1)]
    print(dates)
    dates = [stock.get_nearest_business_day_in_a_week(d) for d in dates]
    print(dates)
    return dates

print(getDate('20220930','20221231'))
'''