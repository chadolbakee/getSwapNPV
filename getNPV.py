import numpy as np
import pandas as pd
from getWorkingDate import getWorkingDate
from fromExcel import fromExcel
import math
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import *


class getNPVforMaturity():

    def __init__(self, npvDate, contractInfo):

        # 스왑 npv 를 구하는데 필수적인 요소들
        self.npvDate = pd.to_datetime(npvDate)
        # 계약정보들
        self.contractDate = pd.to_datetime(contractInfo['contractDate'])
        self.contractNotional = contractInfo['notional']
        self.contractTenor = contractInfo['tenor']
        self.contractSwapRate = contractInfo['swapRate']
        self.direction = contractInfo['direction']

        # ★ contractTenor 구할때 remainingTenor 도 구해주는게 좋을 듯 하다!!

        self.tenor = 20
        # 그냥 npv 는 고정으로 20년짜리 고정 다 구하는거임

        # excel 에서 받은 스왑금리 가져오기
        getSwapRate=fromExcel()
        self.swapRateForTenor = getSwapRate.getSwapRate()
        self.CDrate = getSwapRate.getCdRate()
        self.holidayList = getSwapRate.getHolidayList()

#  ★ 날짜 구하는데 필요한 함수들

    def get_effectiveDate(self, date):
        #이것도 실제 계약 결제일과, 구하고자 하는 npv 기준일의 금리가 다르다

        startDate = pd.to_datetime(date)
        effectiveDate = startDate + BusinessDay()

        return effectiveDate

    def check_weekend(self,date):
        date = pd.to_datetime(date)
        return (date.weekday() == 5)|(date.weekday() == 6)

    def getWeekendPlus(self, date):
        date = pd.to_datetime(date)

        if date.weekday() == 5:
            weekDayPlus = date + relativedelta(days=2)
        elif date.weekday() == 6:
            weekDayPlus = date + relativedelta(days=1)

        if weekDayPlus.month != date.month:

            if date.weekday() == 5:
                weekDayPlus = date - relativedelta(days=1)
            elif date.weekday() == 6:
                weekDayPlus = date - relativedelta(days=2)

        return weekDayPlus
# CD Fixing date 을 위한 하나 빼는 함수
    def getWeekendMinus(self, date):
        weekDayMinus = pd.to_datetime(date)

        if date.weekday() == 5:
            weekDayMinus = date - relativedelta(days=1)
        elif date.weekday() == 6:
            weekDayMinus = date - relativedelta(days=2)

        return weekDayMinus

    def get_CFdays(self, date, tenor):

        global CDFixingDate

        effectiveDate = self.get_effectiveDate(date)
        numOfCF = tenor * 4  # 총 CF가 발생하는 횟수
        listOfCF = list()

        for i in range(numOfCF):
            temp_date = effectiveDate + relativedelta(months=3) * (i + 1)  # 우선 3개월 더한걸로 구해주고

            temp_date = self.checkHolidays(temp_date)
            # 공휴일 먼저 확인하고

            if (self.check_weekend(temp_date)):
                #listOfCF.append(self.getWeekendPlus(temp_date))
                listOfCF.append(self.getWeekendPlus(temp_date))
            else:
                #listOfCF.append(temp_date)
                listOfCF.append(temp_date)

        # 여기서부터는 지나간 날짜 빼주는 함수

        j = 0
        while listOfCF[j] < self.npvDate:
            j = j + 1
            if listOfCF[j] >= self.npvDate:
                break
        # j값을 뽑아낸 후, 과거날짜를 위로 채워주기

        if j != 0:  # 지나간 과거날짜는 모두 삭제해주기
            CDFixingDate = listOfCF[j-1]
            del listOfCF[0:j]

        else :
            CDFixingDate = effectiveDate

        return listOfCF

    def checkHolidays(self, date):

        date = pd.to_datetime(date)

        holidayList = self.holidayList
        holidayList = pd.to_datetime(holidayList)
        i = 0
        if date in holidayList:
            holidaySkip = date
            while holidaySkip in holidayList:
                holidaySkip = holidaySkip + relativedelta(days=1)
                i = i+1

                if holidaySkip.month != date.month:
                    holidaySkip = date - relativedelta(days=i)
                    break
            return holidaySkip

        else:
            return date


    def getNumOfDAYSbetween(self, dateList,flag):
        #  날짜 수 구하는 함수 (ex 91/365, 92/365, 90/365 이런거 구할 때

        numOfDays = [0 for i in range(len(dateList))]

        #  flag==1이면 각 계약의 날짜 기준으로 첫재칸
        #  flag==0이면 구하고자 하는 npv 날짜로 구함!!

        if flag == 1:
            # numOfDays[0]은 유효일에서 빼준거여야 함!!
            numOfDays[0] = (dateList[0]-self.get_effectiveDate(self.contractDate)).days

        elif flag == 0:
            numOfDays[0] = (dateList[0] - self.get_effectiveDate(self.npvDate)).days #으아 모르겠당


        for i in range(1, len(dateList), 1):
            #numOfDays[i-1]=dateList[i]-dateList[i-1]
            numOfDays[i] = (dateList[i] - dateList[i - 1]).days

        return numOfDays

    def getNumOfDaysAccumulate(self, dateList):
        #  실제 계약의 날짜와, npv 구하는 날짜의 effective date의 차이
        numOfDays = list()
        numOfDays = [0 for i in range(len(dateList))]

        for i in range(0, len(dateList), 1):
            numOfDays[i] = (dateList[i]-self.get_effectiveDate(self.npvDate)).days

        return numOfDays

    def getNumOfDaysTwoList(self, npvList, dateList):
        #  실제 계약의 날짜와, npv 구하는 날짜의 effective date의 차이
        numOfDays = list()

        numOfDays = [0 for i in range(len(dateList))]

        numOfDays[0] = (dateList[0]-self.get_effectiveDate(self.npvDate)).days

        for i in range(1, len(dateList), 1):
            numOfDays[i] = (dateList[i]-npvList[i-1]).days

        return numOfDays


#  ★고정금리 cf 구하는 함수

    def getFixedRateCF(self):
        numOfDays = self.getNumOfDAYSbetween(self.get_CFdays(self.contractDate, self.tenor),1)

        #numOfDays=int(numOfDays)
        #numOfDays=map(int, numOfDays)

        fixedCF = [0 for i in range(self.contractTenor*4)]

        for i in range(self.contractTenor*4):

            fixedCF[i] = (self.contractSwapRate/100)*(numOfDays[i]/365)*self.contractNotional

        return fixedCF
# ★만기별 스왑금리 보간하기
# 우선 20년짜리 스왑금리를 위한 리스트를 만들어주는게 우선
    def getDictForSwapRate(self):
        swapRateForTenor = self.swapRateForTenor
        swapListForInterpolation=[0 for i in range(20*4)]

        swapListForInterpolation[0]=swapRateForTenor['CD']
        swapListForInterpolation[1] = swapRateForTenor['6M']
        swapListForInterpolation[2] = swapRateForTenor['9M']
        swapListForInterpolation[3] = swapRateForTenor['1Y']
        swapListForInterpolation[5] = swapRateForTenor['18M']
        swapListForInterpolation[7] = swapRateForTenor['2Y']
        swapListForInterpolation[11] = swapRateForTenor['3Y']
        swapListForInterpolation[15] = swapRateForTenor['4Y']
        swapListForInterpolation[19] = swapRateForTenor['5Y']
        swapListForInterpolation[23] = swapRateForTenor['6Y']
        swapListForInterpolation[27] = swapRateForTenor['7Y']
        swapListForInterpolation[31] = swapRateForTenor['8Y']
        swapListForInterpolation[35] = swapRateForTenor['9Y']
        swapListForInterpolation[39] = swapRateForTenor['10Y']
        swapListForInterpolation[47] = swapRateForTenor['12Y']
        swapListForInterpolation[59] = swapRateForTenor['15Y']
        swapListForInterpolation[79] = swapRateForTenor['20Y']

        return swapListForInterpolation

    def getSwapRateByInterpolation(self):
        #  기존 만기는 getWorkingDate 클래스에서 가져오고, 보간법 스왑금리는 여기서 함
        swapRateForTenor = self.getDictForSwapRate()

        for i in range(len(swapRateForTenor)):
            if swapRateForTenor[i] == 0:
                j = 1
                while swapRateForTenor[i+j] == 0:
                    j = j+1
                    if swapRateForTenor[i+j]>0:
                        break
                swapRateForTenor[i] = swapRateForTenor[i-1]+(swapRateForTenor[i+j]-swapRateForTenor[i-1])/(j+1)

        return swapRateForTenor

    # def getSwapRateByInterpolation(self):
    #     #  기존 만기는 getWorkingDate 클래스에서 가져오고, 보간법 스왑금리는 여기서 함
    #
    #     for i in self.swapDF.index:
    #         if self.swapDF.loc[i,'스왑금리']==0:
    #             j=1
    #             while self.swapDF.loc[i+j,'스왑금리']==0:
    #                 j=j+1
    #                 if self.swapDF.loc[i+j,'스왑금리']>0:
    #                     break
    #             self.swapDF.loc[i,'스왑금리']=self.swapDF.loc[i-1,'스왑금리']+(self.swapDF.loc[i+j,'스왑금리']-self.swapDF.loc[i-1,'스왑금리'])/(j+1)
    #
    #     return self.swapDF

    def getDiscountByMaturity(self): #getSwapRateByInterpolation 끝나고 하기

        swapRateInterpolation = self.getSwapRateByInterpolation()
        # 위에서 스왑금리 보간한거 들고오기
        swapNumOfDays = self.getNumOfDAYSbetween(self.get_CFdays(self.npvDate, 20),0)
        # npv 기준날짜로 list 날짜 sum 한거 가져오기

        discountList = [0 for i in range(20*4)]

        sumProductList = [0 for i in range(20*4)]

        # 만기별 할인계수와 썸프로덕은 하나씩 밀려가면서 동시에 구해야 한다

        discountList[0] = 1/(1+swapRateInterpolation[0]*swapNumOfDays[0]/365)
        sumProductList[0] = discountList[0]*swapNumOfDays[0]

        for i in range(1, len(sumProductList), 1):

            discountList[i] = (1-swapRateInterpolation[i]*sumProductList[i-1]/365)/(1+swapRateInterpolation[i]*swapNumOfDays[i]/365)
            sumProductList[i] = sumProductList[i-1] + (swapNumOfDays[i]*discountList[i])

        return discountList


# ★제로금리 구하는 함수

    def getZeroRateByMaturity(self):
        # 만기별 무이표금리 구하는 함수
        discountList=self.getDiscountByMaturity()
        swapNumOfDaysAccum = self.getNumOfDaysAccumulate(self.get_CFdays(self.npvDate,20))

        zeroRateList = [0 for i in range(20*4)]

        for i in range(len(zeroRateList)):
            zeroRateList[i] = -math.log(discountList[i])*365 / swapNumOfDaysAccum[i]

        return zeroRateList

    def getForwardRateByContract(self):

        discountList = self.getDiscountByContract()
        swapNumOfDays = self.getNumOfDAYSbetween(self.get_CFdays(self.contractDate, self.contractTenor), 1)

        forwardRateList = [0 for i in range(len(swapNumOfDays))]
        # ★10월 23일 여기까지 했음

        forwardRateList[0] = self.swapRateForTenor['CD']

        for i in range(1, len(forwardRateList), 1):
            forwardRateList[i] = ((discountList[i-1]/discountList[i])-1) * (365/swapNumOfDays[i])

        return forwardRateList

# ★무이표금리 계약별로

    def getZeroRateByContract(self):

        zeroByMaturityList = self.getZeroRateByMaturity()
        callRate = self.swapRateForTenor['Call']
        # 첫 무이표금리를 위한 콜금리 설정

        swapNumOfDays = self.getNumOfDAYSbetween(self.get_CFdays(self.npvDate, 20), 0)
        swapNumOfDaysBetween = self.getNumOfDaysTwoList(self.get_CFdays(self.npvDate, 20),self.get_CFdays(self.contractDate, self.contractTenor))

        numOfDaysRemaining = len(self.get_CFdays(self.contractDate, self.contractTenor))

        zeroByContract = [0 for i in range(numOfDaysRemaining)]

        zeroByContract[0] = callRate + (zeroByMaturityList[0] - callRate) * (swapNumOfDaysBetween[0]/swapNumOfDays[0])
        # 첫번째는 callRate로 계산

        for i in range(1, len(zeroByContract), 1):
            zeroByContract[i] = zeroByMaturityList[i-1] + (zeroByMaturityList[i] - zeroByMaturityList[i-1]) * (swapNumOfDaysBetween[i]/swapNumOfDays[i])
        # 이거 리스트 길이 임시방편임! remaining tenor 구해지면 그걸로 갈아끼워주기

        return zeroByContract

# ★할인계수 계약별로 구하기
    def getDiscountByContract(self):

        swapNumOfDaysAccumulate = self.getNumOfDaysAccumulate(self.get_CFdays(self.contractDate, self.contractTenor))

        zeroRateList = self.getZeroRateByContract()

        numOfDaysRemaining = len(self.get_CFdays(self.contractDate, self.contractTenor))

        discountByContract = [0 for i in range(numOfDaysRemaining)]

        for i in range(0, len(discountByContract), 1):
            discountByContract[i] = 1/(np.exp(zeroRateList[i]*swapNumOfDaysAccumulate[i]/365))

        return discountByContract

# ★변동금리 CF 구하기

    def getFloatingRateCF(self):
        CfDaysList = self.get_CFdays(self.contractDate, self.contractTenor)

        numOfDays = self.getNumOfDAYSbetween(self.get_CFdays(self.contractDate, self.tenor),1)

        CDfixingDate = self.getWeekendMinus(CDFixingDate) # CDFixingDate 는 글로벌변수

        CDfixingDate = CDfixingDate.strftime("%Y-%m-%d")

        CDrateForContract = self.CDrate[CDfixingDate]

        floatingCF = [0 for i in range(len(CfDaysList))]

        floatingCF[0] = (CDrateForContract/100)*self.contractNotional*(numOfDays[0]/365) # 첫빠는 CD 금리로 정하기

        forwardList = self.getForwardRateByContract()

        for i in range(1, len(forwardList), 1):
            floatingCF[i] = self.contractNotional*forwardList[i]*(numOfDays[i]/365)

        return floatingCF

    def getSwapNPV(self):
        fixedCFList = self.getFixedRateCF()
        floatingCFList = self.getFloatingRateCF()

        discountList = self.getDiscountByContract()

        npvList = [0 for i in range(len(fixedCFList))]

        for i in range(len(fixedCFList)):
            npvList[i]=(fixedCFList[i]-floatingCFList[i])*discountList[i]

        if self.direction == -1:
            return sum(npvList)

        else:
            return -sum(npvList)