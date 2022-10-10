#여기는 개별 swapContract들의 무이표 할인금리,
import pandas as pd
import numpy as np
from getWorkingDate import getWorkingDate
from fromExcel import fromExcel
from getNPV import getNPVforMaturity
from dateutil.relativedelta import relativedelta

class swapContracts:

    def __init__(self, startDate, npvDate, tenorContract, notionalAmount, swapRate, direction):

        self.startDate=pd.to_datetime(startDate)
        self.npvDate=pd.to_datetime(npvDate)
        self.tenorContract=tenorContract
        self.notionalAmount=notionalAmount
        self.swapRate=swapRate
        self.direction=direction #long인경우 1, short인 경우 -1

        self.getcfdate = getWorkingDate(self.npvDate)
        self.getnpvMaturity=getNPVforMaturity(self.npvDate)

        self.getCFdate = self.getcfdate.get_CFdays() #오늘 구하려는 날짜의 고정된 cf만기
        self.swapDF = pd.DataFrame()  # 빈 데이터프레임 선언한 뒤


        self.swapDF=pd.concat([self.swapDF,self.getnpvMaturity.getSwapRateByInterpolation()],axis=1)

        print(self.swapDF) #이 클래스에서는 이제 이거만 가지고 요리하면 된다


    def get_CFdaysForEachContract(self): #이거 날짜 구하면서 days도 같이 구하자

        #effectiveDate=self.get_effectiveDate(date)
        effectiveDate = self.getcfdate.get_effectiveDate(self.startDate)
        numOfCF= self.tenorContract * 4 #총 CF가 발생하는 횟수
        listOfCF=list()
        numOfDaysBetween=[0 for i in range(self.tenorContract * 4)] #중간중간 날짜 구해주기



        for i in range(numOfCF):
            temp_date=effectiveDate+relativedelta(months=3)*(i+1) #우선 3개월 더한걸로 구해주고
            #공휴일인지 먼저 체크하기
            if (self.getcfdate.checkWeekend(temp_date)):
                listOfCF.append(self.getcfdate.getWeekendPlus(temp_date))
            else:
                listOfCF.append(temp_date)
        ##중간에 날짜도 함께 구해주기!!
        dateList = listOfCF
        numOfDaysBetween[0] = dateList[0] - effectiveDate

        for i in range(1, len(dateList), 1):
            numOfDaysBetween[i] = dateList[i] - dateList[i - 1]
        #여기까지 계약 시작일부터 만기일까지의 listOfCF를 모두 만들어줌
        #이제 이거 다음부터, 구하려는 NPV와 비교해서 지나간 날짜들은 지워줘야함

        j=0
        while listOfCF[j]<self.npvDate:
            j=j+1
            if listOfCF[j]>=self.npvDate:
                break
        #j값을 뽑아낸 후, 과거날짜를 위로 채워주기

        if j!=0: #지나간 과거날짜는 모두 삭제해주기
            del listOfCF[0:j]
            del numOfDaysBetween[0:j]

        df=pd.DataFrame({'계약CF날짜':listOfCF,'계약CF간기간':numOfDaysBetween})
        #
        # percentile_list = pd.DataFrame(
        #     {'lst1Title': lst1,
        #      'lst2Title': lst2,
        #      'lst3Title': lst3
        #      })

        return df


    def getFixedrateCF(self):
        # get_CFdaysForEachContract에서 만들어진 '계약CF간기간' 데이터를 이용해야함!!
        df=self.get_CFdaysForEachContract()

        numOfDays=df['계약CF간기간'].dt.days

        # 10월 9일 ['기간']이거 정수로 어떻게 바꿀까 고민하다 잠듬 ->정답:timedelta를 정수로 바꾸고 싶을때에는 dt.days
        fixedCF = [0 for i in range(len(numOfDays))]  # 문제가 많은데 일단 모두 list로 넣고 그 다음 series로 하기
        for i in range(len(numOfDays)):
            # self.swapDF.loc[i]['고정금리CF']=(self.swapRate/100)*(numOfDays[i]/365) #이렇게 하지말고 시리즈를 복사해보자
            fixedCF[i] = (self.swapRate / 100) * (numOfDays[i] / 365) * (self.notionalAmount)

        # fixedCF = pd.Series(fixedCF, name='고정금리CF')
        # self.swapDF = pd.concat([self.swapDF, fixedCF], axis=1)
        fixedCF=pd.Series(fixedCF,name='고정금리CF')

        return fixedCF

