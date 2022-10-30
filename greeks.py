import pandas as pd
import numpy as np
from fromExcel import fromExcel
import math

class greeks:

    def __init__(self):
        getSwapRate = fromExcel()
        self.swapRateForTenor = getSwapRate.getSwapRate()

    def getPlus10bp(self):
        swapRate=self.swapRateForTenor
        swapPlus10bp=[0 for i in range(len(swapRate))]
        # swapPlus10bp=[i+0.001 for i in self.swapRateForTenor]
        return print(swapRate)
