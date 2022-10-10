import numpy as np
import pandas as pd
from getWorkingDate import getWorkingDate
from fromExcel import fromExcel
import math


class getNPVforMaturity():

    def __init__(self, npvDate):
        #스왑 npv를 구하는데 필수적인 요소들
        self.npvDate = pd.to_datetime(npvDate)
        self.tenor = 20#그냥 20년짜리 고정 다 구하는거임

        getcfdate = getWorkingDate(self.npvDate)
        self.getCFdate=getcfdate.get_CFdays()
        self.swapDF=pd.DataFrame()#빈 데이터프레임 선언한 뒤

        self.swapDF=getcfdate.get_DFofDateAndCount()#일단 날짜랑 날짜수 이 클래스로 가져오기는 성공
        #self.swapDF = pd.DataFrame(
         #                     columns=['날짜','기간','만기별스왑금리', '만기별할인계수', '만기별무이표금리', '일별무이표금리', '일별할인계수', '고정금리CF', '개별변동금리','변동금리CF')

        #excel에서 받은 스왑금리 가져오기
        getSwapRate=fromExcel()
        self.swapRate=getSwapRate.getSwapRate()

    def printing(self):
        print(self.swapDF)

    # def getFixedrateCF(self):
    #     numOfDays=self.swapDF['기간'].dt.days
    #
    #     #10월 9일 ['기간']이거 정수로 어떻게 바꿀까 고민하다 잠듬 ->정답:timedelta를 정수로 바꾸고 싶을때에는 dt.days
    #     fixedCF = [0 for i in range(self.tenor*4)]#문제가 많은데 일단 모두 list로 넣고 그 다음 series로 하기
    #     for i in range(self.tenor*4):
    #         #self.swapDF.loc[i]['고정금리CF']=(self.swapRate/100)*(numOfDays[i]/365) #이렇게 하지말고 시리즈를 복사해보자
    #         fixedCF[i]=(self.swapRate/100)*(numOfDays[i]/365)*(self.notionalAmount)
    #
    #     fixedCF = pd.Series(fixedCF, name='고정금리CF')
    #     self.swapDF = pd.concat([self.swapDF, fixedCF], axis=1)
    #     return self.swapDF

    def getSwapRateByInterpolation(self):#기존 만기는 getWorkingDate 클래스에서 가져오고, 보간법 스왑금리는 여기서 함

        for i in self.swapDF.index:
            if self.swapDF.loc[i,'스왑금리']==0:
                j=1
                while self.swapDF.loc[i+j,'스왑금리']==0:
                    j=j+1
                    if self.swapDF.loc[i+j,'스왑금리']>0:
                        break
                self.swapDF.loc[i,'스왑금리']=self.swapDF.loc[i-1,'스왑금리']+(self.swapDF.loc[i+j,'스왑금리']-self.swapDF.loc[i-1,'스왑금리'])/(j+1)

        return self.swapDF

    def getDiscountByMaturity(self): #getSwapRateByInterpolation 끝나고 하기

        self.swapDF=self.getSwapRateByInterpolation() #위에서 스왑금리 보간한거 들고오기
        discountList=[0 for i in range(self.tenor*4)] #할인계수 list 추가

        discountList=pd.Series(discountList,name='할인계수')

        numOfDays = self.swapDF['기간'].dt.days.values.tolist()  #loc로 바로 쓰려고 했는데 안되는듯
        swapRate=self.swapDF['스왑금리'].values.tolist()

        print(swapRate)


        for i in self.swapDF.index:
            if i==0:
                discountList[i]=1/(1+(swapRate[i]/100*numOfDays[i]/365))
            else:
                discountList[i] = (1 - ((swapRate[i]/100)/365 * sum(numOfDays[0:i]))*sum(discountList[0:i]))/(1+ (swapRate[i]/100)*numOfDays[i]/365)

        # for i in self.swapDF.index:
        #     if i==0:
        #         discountList[i]=(1/((1+self.swapDF.loc[i,'스왑금리']/100)*(numOfDays[i]/365)))
        #     else:
        #         # discountList[i]=(1-(self.swapDF.loc[i,'스왑금리'])/100*sum(numOfDays[0:i]))
        #         discountList[i] = (1 - ((self.swapDF.loc[i, '스왑금리']/ 100) /365 * sum(numOfDays[0:i]))*sum(discountList[0:i]))/(1+(self.swapDF.loc[i, '스왑금리']/ 100)*numOfDays[i]/365)

        return discountList

    def getZeroRateByMaturity(self):

        numOfDays=self.swapDF['기간'].dt.days#series[i:j]오류떠가지고 list로 바꿔줬음
        discountList=self.getDiscountByMaturity()

        print(discountList[1])

        zeroCurveByMaturity=[0 for i in range(self.tenor)]
        for i in range(len(zeroCurveByMaturity)):
            zeroCurveByMaturity[i]=-math.log(discountList[i])*365/numOfDays[i]

        return zeroCurveByMaturity



