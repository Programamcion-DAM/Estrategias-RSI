# region imports
from AlgorithmImports import *
# endregion

class WellDressedVioletRabbit(QCAlgorithm):

    def Initialize(self):
        
        #Estos son los valores que pueden alterar
        self.periods = 14 #El numero de periodos del RSI
        self.ticker = "AAPL" #El ticker de la empresa que quieran hacer el backtest
        self.resolution = Resolution.Hour #La resolucion de los datos: Daily,Hour,Minute,Second
        
        self.SetStartDate(2022, 1, 1)  # Set Start Date
        #self.SetEndDate(2022, 1, 1)
        self.SetCash(100000)  # Set Strategy Cash
        self.equity = self.AddEquity(self.ticker, self.resolution).Symbol

        self.rsi = self.RSI(self.equity,self.periods,self.resolution)
        self.SetWarmup(self.periods)
        self.buy = False
        self.position = "None"

        self.topPrice = 0
        self.bottomPrice = 0

    def OnData(self, data: Slice):
        if self.IsWarmingUp:
            return
        
        if data[self.equity]:
            price = data[self.equity].Close
        else:
            return

        if not self.Portfolio.Invested:
            if self.rsi.Current.Value <= 20:
                self.position = "long"
                return
            if self.rsi.Current.Value >= 80:
                self.position = "short"
                return
            
            if self.position == "long":
                self.SetHoldings(self.equity,1)
                self.topPrice = price * 1.015
                self.bottomPrice = price * 0.985
                return
            
            if self.position == "short":
                self.SetHoldings(self.equity,-1)
                self.topPrice = price * 1.015
                self.bottomPrice = price * 0.985
                return
            return 
        
        if not self.bottomPrice < price < self.topPrice:
            self.Liquidate()
            return 
        