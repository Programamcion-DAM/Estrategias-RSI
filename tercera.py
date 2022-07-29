# region imports
from AlgorithmImports import *
# endregion

class UglyMagentaSalmon(QCAlgorithm):
    def Initialize(self):
        self.ticker = "BTCUSD" 
        self.barMinutes = 5
        self.SetStartDate(2022, 1, 1)  
        #self.SetEndDate(2021, 1, 1)
        
        self.SetCash(100000)  # Set Strategy Cash
        self.symbol = self.AddCrypto(self.ticker, Resolution.Minute).Symbol

        self.Consolidate(self.symbol, timedelta(minutes = self.barMinutes), self.BarHandler)

        self.sma = SimpleMovingAverage(200)
        self.RegisterIndicator(self.symbol, self.sma, timedelta(minutes=self.barMinutes))

        self.rsi = RelativeStrengthIndex(2, MovingAverageType.Simple)
        self.RegisterIndicator(self.symbol, self.rsi, timedelta(minutes=self.barMinutes))

        self.atr = AverageTrueRange(2)
        self.RegisterIndicator(self.symbol, self.atr, timedelta(minutes=self.barMinutes))

        self.bottomPrice = 0
        self.topPrice = 0

    def OnData(self, data: Slice):
        pass

    def BarHandler(self,consolidated):
        if not self.sma.IsReady:
            return
        
        price = self.Securities[self.symbol].Price
        
        if self.Portfolio.Invested:
            if not self.bottomPrice < price < self.topPrice:
                self.Liquidate()
            return
        
        if price > self.sma.Current.Value and self.rsi.Current.Value < 5:
            self.SetHoldings(self.symbol,1)
            self.topPrice = price + self.atr.Current.Value*1.5
            self.bottomPrice = price - self.atr.Current.Value*1.5
        
        if price < self.sma.Current.Value and self.rsi.Current.Value > 95:
            self.SetHoldings(self.symbol,1)
            self.topPrice = price + self.atr.Current.Value*1.5
            self.bottomPrice = price - self.atr.Current.Value*1.5
        