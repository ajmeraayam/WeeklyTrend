def EntryPoint(prev_20_week, curr_20_week):
    '''
        prev_10_week - Array of closing and highest high values of given stock/index for each week of last 10 weeks. It contains data of 20 weeks in past starting from previous week.
        curr_10_week - Array of closing and highest high values of given stock/index for each week of last 10 weeks. It contains data of 20 weeks in past starting from this week.

        *Both arrays have data in descending order of time. Current data at start.*

        This function calculates if current stock is ideal for entry or not.
    '''

    mov_avg_cond = False
    ROC_cond = False
    highest_high_cond = True

    mov_avg_cond = MovingAverageTrend(prev_20_week[0:9], curr_20_week[0:9])

    # Point 2 - 20 week ROC must be above 30%
    # FORMULA - ((current closing price - closing price 20 weeks ago) / closing price 20 weeks ago) * 100
    roc = ((curr_20_week[0][0] - curr_20_week[-1][0])/curr_20_week[-1][0]) * 100

    if roc > 30:
        ROC_cond = True

    # Point 3 - Stock must close above a new 20 week high
    # Current closing price should be above highest highs that have occured in last 20 weeks
    curr_highest_high = curr_20_week[0][1]

    for i in range(1, len(curr_20_week)):
        if curr_highest_high <= curr_20_week[i][1]:
            highest_high_cond = False
            break
    
    # If all the 3 conditions have been satisfied then this stock can be bought
    if mov_avg_cond and ROC_cond and highest_high_cond:
        return True
    
    return False

def MovingAverageTrend(prev_10_week, curr_10_week):
    # Calculate 10 week average for current week to last 10 weeks and previous week to last 10 weeks
    sum = 0
    for closing, hh in prev_10_week:
        sum = sum + closing

    avg_prev_10_weeks = sum / 10
    
    sum = 0
    for closing, hh in curr_10_week:
        sum = sum + closing
    
    avg_curr_10_weeks = sum / 10

    # Point 1 - 10 week moving average of the stock/index must be greater than last week
    if avg_curr_10_weeks > avg_prev_10_weeks:
        return True
    
    return False

def ExitSignal(buyPrice, AcceptableStopLoss, current_price):
    if ((buyPrice - current_price)/buyPrice) * 100 >= AcceptableStopLoss:
        return True

    return False

def WeeklyTrend(AllStockNames, BoughtStocks, AcceptableStopLoss):
    '''
        AllStockNames - List of all the names of the stocks that are under a given Market Exchange
        BoughtStocks - List of all the names of the stocks that are bought by the user with the buy price 
    '''
    entryStocks = []
    exitStocks = []
    stopLoss = AcceptableStopLoss
    # Convert the list of names to dictionary and initialize them to false
    StockNameDict = dict.fromkeys(AllStockNames, False)

    # If a stock is bought by the user then change the value to true
    for stock, buyPrice in BoughtStocks:
        if stock in StockNameDict:
            StockNameDict[stock] = True

    BoughtStocksDict = dict(BoughtStocks)

    ### Use the stock names to open the respective data files and read the data
    #### Downward trend
    prev_20_week = [(20.0, 25.0), (21.0, 21.0), (21.5, 21.9), (21.2, 21.3), (21.9, 22.1), (22.8, 22.9), (22.5, 22.7), (22.9, 23.0), (22.4, 22.7), (22.3, 22.4), (23.2, 23.5), (23.9, 25.0), (24.5, 25.0), (24.9, 25.5), (25.7, 28.0), (27.1, 27.5), (27.2, 27.8), (27.5, 27.5), (27.3, 27.8), (27.2, 27.3)]
    curr_20_week = [(19.8, 21.0), (20.0, 25.0), (21.0, 21.0), (21.5, 21.9), (21.2, 21.3), (21.9, 22.1), (22.8, 22.9), (22.5, 22.7), (22.9, 23.0), (22.4, 22.7), (22.3, 22.4), (23.2, 23.5), (23.9, 25.0), (24.5, 25.0), (24.9, 25.5), (25.7, 28.0), (27.1, 27.5), (27.2, 27.8), (27.5, 27.5), (27.3, 27.8)]
    #### Upward trend
    #prev_20_week = [(27.2, 27.3), (27.3, 27.8), (27.5, 27.5), (27.2, 27.8), (27.1, 27.5), (25.7, 28.0), (24.9, 25.5), (24.5, 25.0), (23.9, 25.0), (23.2, 23.5), (22.3, 22.4), (22.4, 22.7), (22.9, 23.0), (22.5, 22.7), (22.8, 22.9), (21.9, 22.1), (21.2, 21.3), (21.5, 21.9), (21.0, 21.0), (20.0, 25.0)]
    #curr_20_week = [(27.6, 28.9), (27.2, 27.3), (27.3, 27.8), (27.5, 27.5), (27.2, 27.8), (27.1, 27.5), (25.7, 28.0), (24.9, 25.5), (24.5, 25.0), (23.9, 25.0), (23.2, 23.5), (22.3, 22.4), (22.4, 22.7), (22.9, 23.0), (22.5, 22.7), (22.8, 22.9), (21.9, 22.1), (21.2, 21.3), (21.5, 21.9), (21.0, 21.0)]

    # Loop the entry and exit checks for each stock. 
    # Check entry condition only for the stocks that are not bought.
    # Check exit condition only for the stocks that are bought.
    for key, value in StockNameDict.items():
        # If stock is not bought
        if not value:
            entry = EntryPoint(prev_20_week, curr_20_week)
            if entry:
                entryStocks.append(key)
            print('Stock - {}, Entry - {}'.format(key, entry))
        # If stock is bought
        else:
            mov_avg = MovingAverageTrend(prev_20_week[0:9], curr_20_week[0:9])
            if not mov_avg:
                stopLoss = 10

            exitSig = ExitSignal(BoughtStocksDict[key], stopLoss, curr_20_week[0][0])
            if exitSig:
                exitStocks.append(key)
            print('Stock - {}, Exit - {}'.format(key, exitSig))
    #pass

if __name__ == '__main__':
    # Test sample of stock names
    # Get name of the stocks from a file. Assuming the bought stocks come in a list
    names = ["ABC", "AHD", "BAS", "SND", "EUN", "ZIN", "IWE", "EIJ", "AJJ", "AJE", "POE", "FJN", "GJK", "NED", "BEP", "IDM", "QMA", "WIO", "FIP"]
    boughtStocks = [("AHD", 50.0), ("EUN", 25.0), ("WIO", 30.0), ("IDM", 35.0), ("IWE", 15.0), ("AJE", 23.0), ("POE", 28.0)]
    AcceptableStopLoss = 40
    WeeklyTrend(names, boughtStocks, AcceptableStopLoss)