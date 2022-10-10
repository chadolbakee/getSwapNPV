import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import *
from fromExcel import fromExcel

class getWorkingDate():

    def __init__(self, npvDate):
        # 날짜 구하는데 필수적인 변수들
        self.npvDate=pd.to_datetime(npvDate) #npv를 구하고 싶은 실제 기준 날짜 , 스왑금리 뽑는 날짜
        self.npvTenor=20 #그냥 만기=20년

        #six_months = pd.to_datetime(start_date) + relativedelta(months=+3)
        getSwapRate = fromExcel()
        self.swapRate = getSwapRate.getSwapRate()


    def get_effectiveDate(self,date): #이것도 실제 계약 결제일과, 구하고자 하는 npv 기준일의 금리가 다르다

        startDate = pd.to_datetime(date)
        effectiveDate = startDate + BusinessDay()

        return effectiveDate



    def is_business_day(self,date):
        return bool(len(pd.bdate_range(date, date)))

    def checkWeekend(self,date):
        date = pd.to_datetime(date)
        return ((date.weekday() == 5)|(date.weekday() == 6))

    def getWeekendPlus(self, date):
        date = pd.to_datetime(date)


        if date.weekday() == 5:
            WeekDayPlus = date + relativedelta(days=2)
        elif date.weekday() == 6:
            WeekDayPlus = date + relativedelta(days=1)

        if WeekDayPlus.month != date.month:

            if date.weekday() == 5:
                WeekDayPlus = date - relativedelta(days=1)
            elif date.weekday() == 6:
                WeekDayPlus = date - relativedelta(days=2)

        return WeekDayPlus

    def get_CFdays(self):

        effectiveDate=self.get_effectiveDate(self.npvDate)
        numOfCF= self.npvTenor * 4 #총 CF가 발생하는 횟수
        listOfCF=list()

        for i in range(numOfCF):
            temp_date=effectiveDate+relativedelta(months=3)*(i+1) #우선 3개월 더한걸로 구해주고
            #공휴일인지 먼저 체크하기
            if (self.checkWeekend(temp_date)):
                listOfCF.append(self.getWeekendPlus(temp_date))
            else:
                listOfCF.append(temp_date)

        return listOfCF




    def getNumOfDAYSbetween(self): #날짜 수 구하는 함수 (ex 91/365, 92/365, 90/365 이런거 구할 때
        numOfDays=[0 for i in range(self.npvTenor * 4)]
        effectiveDate=self.get_effectiveDate(self.npvDate)

        dateList = self.get_CFdays()
        numOfDays[0]=dateList[0]-effectiveDate

        for i in range(1, len(dateList), 1):
            numOfDays[i]=dateList[i]-dateList[i-1]

        return numOfDays

    def getSwapTenorSeries(self):
        # 시리즈로 일단 0으로 넣고, 필요한 index에 넣기 + 여기서 주어진 스왑금리를 넣어주는게 좋을거 같다.
        # swapTenorIndex=pd.Series(np.zeros(self.tenor*4),name='만기INDEX') #이걸 데이터프레임으로 바꾸고 만기금리도 같이 넣어주자

        swapTenorIndex = pd.DataFrame(np.zeros(self.npvTenor * 4 * 2).reshape(self.npvTenor * 4, 2), columns=['만기INDEX', '스왑금리'])
        swapTenorIndex.loc[0,'만기INDEX'] = '3M'
        swapTenorIndex.loc[0, '스왑금리'] = self.swapRate.loc[1,'금리']
        swapTenorIndex.loc[1,'만기INDEX'] = '6M'
        swapTenorIndex.loc[1, '스왑금리'] = self.swapRate.loc[2, '금리']
        swapTenorIndex.loc[2, '만기INDEX'] = '9M'
        swapTenorIndex.loc[2, '스왑금리'] = self.swapRate.loc[3, '금리']
        swapTenorIndex.loc[3, '만기INDEX'] = '1Y'
        swapTenorIndex.loc[3, '스왑금리'] = self.swapRate.loc[4, '금리']
        swapTenorIndex.loc[5, '만기INDEX'] = '18M'
        swapTenorIndex.loc[5, '스왑금리'] = self.swapRate.loc[5, '금리']
        swapTenorIndex.loc[7, '만기INDEX'] = '2Y'
        swapTenorIndex.loc[7, '스왑금리'] = self.swapRate.loc[6, '금리']
        swapTenorIndex.loc[11, '만기INDEX'] = '3Y'
        swapTenorIndex.loc[11, '스왑금리'] = self.swapRate.loc[7, '금리']
        swapTenorIndex.loc[15, '만기INDEX'] = '4Y'
        swapTenorIndex.loc[15, '스왑금리'] = self.swapRate.loc[8, '금리']
        swapTenorIndex.loc[19, '만기INDEX'] = '5Y'
        swapTenorIndex.loc[19, '스왑금리'] = self.swapRate.loc[9, '금리']

        if self.npvTenor>5:#5년 이상인 애들은 조건문을 주자
            swapTenorIndex.loc[23, '만기INDEX'] = '6Y'
            swapTenorIndex.loc[23, '스왑금리'] = self.swapRate.loc[10, '금리']
            swapTenorIndex.loc[27, '만기INDEX'] = '7Y'
            swapTenorIndex.loc[27, '스왑금리'] = self.swapRate.loc[11, '금리']
            swapTenorIndex.loc[31, '만기INDEX'] = '8Y'
            swapTenorIndex.loc[31, '스왑금리'] = self.swapRate.loc[12, '금리']
            swapTenorIndex.loc[35, '만기INDEX'] = '9Y'
            swapTenorIndex.loc[35, '스왑금리'] = self.swapRate.loc[13, '금리']
            swapTenorIndex.loc[39, '만기INDEX'] = '10Y'
            swapTenorIndex.loc[39, '스왑금리'] = self.swapRate.loc[14, '금리']

        if self.npvTenor>10:
            swapTenorIndex.loc[47, '만기INDEX'] = '12Y'
            swapTenorIndex.loc[47, '스왑금리'] = self.swapRate.loc[15, '금리']
            swapTenorIndex.loc[59, '만기INDEX'] = '15Y'
            swapTenorIndex.loc[59, '스왑금리'] = self.swapRate.loc[16, '금리']

        if self.npvTenor>15:
            swapTenorIndex.loc[79, '만기INDEX'] = '20Y'
            swapTenorIndex.loc[79, '스왑금리'] = self.swapRate.loc[17, '금리']

        return swapTenorIndex

    def get_DFofDateAndCount(self):#return:데이터프레임, 칼럼: [cf발생 날짜, CF 날짜별 기간, 해당 만기 INDEX]
        # 이 클래스에서 날짜랑 기간 모두 만들고 getNPV클래스로 넘기는게 나을듯

        dateList=self.get_CFdays()
        dateList = pd.Series(dateList, name='날짜') #concat 함수를 쓰라는데 이건 또 series로만 가능하다네

        numOfDays=self.getNumOfDAYSbetween()
        numOfDays = pd.Series(numOfDays, name='기간')

        #만기 인덱스
        swapTenorIndex=self.getSwapTenorSeries()

        swapDF = pd.DataFrame()

        swapDF = pd.concat([swapDF, dateList], axis=1)
        swapDF = pd.concat([swapDF, numOfDays], axis=1) #데이터프레임 칼럼을 미리 선언하고 그 칼럼 안에 concat하는 방식은 없는걸까??
        swapDF = pd.concat([swapDF, swapTenorIndex], axis=1)

        return swapDF


# ## 공휴일 불러오는 api
#     def get_request_query(url, operation, params, serviceKey):
#         params = urlparse.urlencode(params)
#         request_query = url + '/' + operation + '?' + params + '&' + 'serviceKey' + '=' + serviceKey
#         return request_query
#
#     def get_holiday(self):
#         mykey = "AVdytU6CZkv3oLbMfnfCVkbVcSuBSuUDiKc80Ri%2BHMPrMjHwmb%2FfqFv0nFqwWBIyT59ApoZ9HC5pL4xnNHdRww%3D%3D"
#         url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService'
#         operation = 'getRestDeInfo'
#
#         df = pd.DataFrame()
#
#         for year in [2022,2023,2024,2025,2026,2027,2028,2029,2030]:
#             for month in range(1, 500):
#
#                 if month < 10:
#                     month = '0' + str(month)
#                 else:
#                     month = str(month)
#                 params = {'solYear': year, 'solMonth': month}
#
#                 request_query = get_request_query(url, operation, params, mykey)
#
#                 res = requests.get(request_query)
#                 soup = BeautifulSoup(res.text, 'lxml')
#                 items = soup.find_all('item')
#
#                 for item in items:
#                     day = item.locdate.get_text()
#                     name = item.datename.get_text()
#                     data = {'휴일이름': name, '날짜': day}
#                     df = df.append(data,ignore_index=True)
#
#         print(df['날짜'])
