import xlwings as xw
import pandas as pd

class fromExcel:

    def getSwapRate(self):

        workbook = xw.Book('swaprate.xlsx')
        sheet1 = workbook.sheets['sheet1'].used_range.value
        df = pd.DataFrame(sheet1,columns=['만기','금리'])

        return df

# if __name__ == "__main__":
#     fromexcel=fromExcel()
#     print(fromexcel.getSwapRate())