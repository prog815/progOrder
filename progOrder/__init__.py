def kach(PR,TR,dTP,dSL):
    import numpy as np
    return np.mean(PR*(TR*dTP-(1-TR)*dSL))

# ----------------------------------------------------

def bs2y(b,s): 
    return b*2+s

# ----------------------------------------------------

def y2bs(y):
    s = y % 2
    b = ( y - s ) // 2
    return (b,s)

# ----------------------------------------------------

def getBuySellForData(ohlc, orderLifeLen = 50, dSL = 0.001, dTP = 0.0005, SP = 0.07):
    """
    Расчет ордеров на покупку и продажу
    
    Аргументы:
        ohlc - матрица Open,High,Low,Close
        orderLifeLen - время жизни ордера
        dSL - доля на stop-loss (относительно close[-1])
        dTP - доля на take-profit (относительно close[-1])
        SP - своп абсолютно
    
    Вовращает:
        buy,sell - два вектора (покупка и продажа):
            1 - удачный ордер
            0 - неудачный ордер
    
    Замечание:
        Ордер ставится по закрытию close(n) после окончания точки (n).
        Если поставил ордер после окончания точки (n) то результат отработки будет buy(n) и sell(n).
        Смещать ряды не нужно.
    
    Пример:
        b,s = getBuySellForData(ohlc,dSL=0.01)
    """
    import numpy as np
    
    rows = ohlc.shape[0]

    Open = ohlc[:,0]
    Heigh = ohlc[:,1]
    Low = ohlc[:,2]
    Close = ohlc[:,3]

    buy = np.zeros_like(ohlc[:,0])
    sell = np.zeros_like(ohlc[:,0])

    for n in range(rows-1):
        
        OP = Close[n]

        buyTP = OP * ( 1. + dTP ) + SP
        buySL = OP * ( 1. - dSL ) + SP

        sellTP = OP * ( 1. - dTP ) - SP
        sellSL = OP * ( 1. + dSL ) - SP

        orderBuyOpened = False
        orderSellOpened = False

        orderBuyClosed = False
        orderSellClosed = False
        
        for k in range(n+1,min(n+orderLifeLen,rows)):
            
            if (not orderBuyOpened) and (Low[k] <= OP):
                orderBuyOpened = True

            if (not orderSellOpened) and (Heigh[k] >= OP):
                orderSellOpened = True

            if orderBuyOpened:
                if not orderBuyClosed:
                    if Heigh[k] >= buyTP:
                        orderBuyClosed = True
                        buy[n] = 1
                        
                    if Low[k] <= buySL:
                        orderBuyClosed = True
                        buy[n] = 0
            
            if orderSellOpened:
                if not orderSellClosed:
                    if Low[k] <= sellTP:
                        orderSellClosed = True
                        sell[n] = 1
                        
                    if Heigh[k] >= sellSL:
                        orderSellClosed = True
                        sell[n] = 0

    return buy,sell
