import xlwings as xw
import pandas as pd
import decimal
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import *

class fromExcel:

    def getSwapRate(self):

        workbook = xw.Book('swaprate.xlsx')
        #sheet1 = workbook.sheets['sheet1'].used_range.value
        swapIndex=workbook.sheets['sheet1'].range('A1').expand('down').value
        swapRate = workbook.sheets['sheet1'].range('B1').expand('down').value

        swapRateDict=dict(zip(swapIndex, swapRate))
        #df = pd.DataFrame(sheet1,columns=['만기','금리'])

        return swapRateDict

    def getCdRate(self):
        workbook = xw.Book('swaprate.xlsx')
        # sheet1 = workbook.sheets['sheet1'].used_range.value
        date = workbook.sheets['sheet2'].range('A1').expand('down').value
        CDrate = workbook.sheets['sheet2'].range('B1').expand('down').value

        for i in range(len(date)):
            date[i] = date[i].strftime("%Y-%m-%d")

        CDrateDict = dict(zip(date, CDrate))
        # df = pd.DataFrame(sheet1,columns=['만기','금리'])

        return CDrateDict

    def getHolidayList(self):

        workbook = xw.Book('swaprate.xlsx')
        holidayList = workbook.sheets['sheet3'].range('A1').expand('down').value

        for i in range(len(holidayList)):
            holidayList[i] = holidayList[i].strftime("%Y-%m-%d")

        return holidayList

    def getSwapRatePlus10bp(self):

        workbook = xw.Book('swaprate.xlsx')
        #sheet1 = workbook.sheets['sheet1'].used_range.value
        swapIndex=workbook.sheets['sheet1'].range('A1').expand('down').value
        swapRate = workbook.sheets['sheet1'].range('B1').expand('down').value

        swapRate = [i+0.001 for i in swapRate]

        swapRateDict=dict(zip(swapIndex, swapRate))
        #df = pd.DataFrame(sheet1,columns=['만기','금리'])

        return swapRateDict

    def getSwapRateMinus10bp(self):

        workbook = xw.Book('swaprate.xlsx')
        #sheet1 = workbook.sheets['sheet1'].used_range.value
        swapIndex=workbook.sheets['sheet1'].range('A1').expand('down').value
        swapRate = workbook.sheets['sheet1'].range('B1').expand('down').value

        swapRate = [i-0.001 for i in swapRate]

        swapRateDict=dict(zip(swapIndex, swapRate))
        #df = pd.DataFrame(sheet1,columns=['만기','금리'])

        return swapRateDict

    # def getSwapRate(self):
    #
    #     workbook = xw.Book('swaprate.xlsx')
    #     sheet1 = workbook.sheets['sheet1'].used_range.value
    #     df = pd.DataFrame(sheet1,columns=['만기','금리'])
    #
    #     return df

# if __name__ == "__main__":
#     fromexcel=fromExcel()
#     print(fromexcel.getSwapRate())