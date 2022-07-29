# region imports
from AlgorithmImports import *
# endregion

class JumpingAsparagusGull(QCAlgorithm):

    def Initialize(self):
        
        #Estos son los valores que pueden alterar
        self.periods = 14 #El numero de periodos del RSI
        self.ticker = "AAPL" #El ticker de la empresa que quieran hacer el backtest
        self.resolution = Resolution.Daily #La resolucion de los datos: Daily,Hour,Minute,Second
        
        self.SetStartDate(2022, 1, 1)  # Set Start Date
        #self.SetEndDate(2022, 1, 1)
        self.SetCash(100000)  # Set Strategy Cash
        self.equity = self.AddEquity(self.ticker, self.resolution).Symbol

        self.rsi = self.RSI(self.equity,self.periods)
        self.SetWarmup(self.periods)
        self.buy = False
        

    def OnData(self, data: Slice):
        if self.IsWarmingUp:
            return
        
        if not self.Portfolio.Invested:
            if self.rsi.Current.Value <= 30:
                self.buy = True
                return
            if self.buy:
                self.SetHoldings(self.equity,1)
                self.buy = False
                return
        else:
            if self.rsi.Current.Value >= 70:
                self.Liquidate() 