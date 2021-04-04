import datetime
import json

def IndexTrend(prev_20_week, curr_20_week):
    '''
        prev_20_week - Array of closing and highest high values of given stock/index for each week of last 20 weeks. It contains data of 20 weeks in past starting from previous week.
        curr_20_week - Array of closing and highest high values of given stock/index for each week of last 20 weeks. It contains data of 20 weeks in past starting from this week.

        *Both arrays have data in descending order of time. Current data at start.*

        This function checks the current trend of the index.
    '''
    return MovingAverageTrend(prev_20_week, curr_20_week)

def ROCCheck(curr_20_week):
    return ((curr_20_week[0][0] - curr_20_week[-1][0])/curr_20_week[-1][0]) * 100

    #if roc > 30:
    #    return True

    #return False

def BreakoutCheck(curr_20_week):
    curr_highest_high = curr_20_week[0][1]

    for i in range(1, len(curr_20_week)):
        if curr_highest_high <= curr_20_week[i][1]:
            return False
            #break
    
    return True

# def EntryPoint(prev_20_week, curr_20_week):
#     '''
#         prev_20_week - Array of closing and highest high values of given stock/index for each week of last 20 weeks. It contains data of 20 weeks in past starting from previous week.
#         curr_20_week - Array of closing and highest high values of given stock/index for each week of last 20 weeks. It contains data of 20 weeks in past starting from this week.

#         *Both arrays have data in descending order of time. Current data at start.*

#         This function calculates if current stock is ideal for entry or not.
#     '''

#     mov_avg_cond = False
#     ROC_cond = False
#     highest_high_cond = True

#     mov_avg_cond = MovingAverageTrend(prev_20_week[0:9], curr_20_week[0:9])

#     # Point 2 - 20 week ROC must be above 30%
#     # FORMULA - ((current closing price - closing price 20 weeks ago) / closing price 20 weeks ago) * 100
#     roc = ((curr_20_week[0][0] - curr_20_week[-1][0])/curr_20_week[-1][0]) * 100

#     if roc > 30:
#         ROC_cond = True

#     # Point 3 - Stock must close above a new 20 week high
#     # Current closing price should be above highest highs that have occured in last 20 weeks
#     curr_highest_high = curr_20_week[0][1]

#     for i in range(1, len(curr_20_week)):
#         if curr_highest_high <= curr_20_week[i][1]:
#             highest_high_cond = False
#             break
    
#     # If all the 3 conditions have been satisfied then this stock can be bought
#     if mov_avg_cond and ROC_cond and highest_high_cond:
#         return True
    
#     return False

def MovingAverageTrend(prev_20_week, curr_20_week):
    # Calculate 20 week average for current week to last 20 weeks and previous week to last 20 weeks
    sum = 0
    for closing, hh in prev_20_week:
        sum = sum + closing

    avg_prev_20_weeks = sum / len(prev_20_week)
    
    sum = 0
    for closing, hh in curr_20_week:
        sum = sum + closing
    
    avg_curr_20_weeks = sum / len(prev_20_week)

    # Point 1 - 20 week moving average of the stock/index must be greater than last week
    if avg_curr_20_weeks > avg_prev_20_weeks:
        return True
    
    return False

def ExitSignal(buyPrice, AcceptableStopLoss, current_price):
    if ((buyPrice - current_price)/buyPrice) * 100 >= AcceptableStopLoss:
        return True

    return False

def IndexDataSegregation(WeeklyDict, indexName):
    prev_20_week = []
    curr_20_week = []

    for key, value in WeeklyDict.items():
        if indexName in value: (openp, highp, lowp, closep) = value[indexName]
        else: continue
        
        if key == 0:
            curr_20_week.append((closep, highp))
        elif key == 20:
            prev_20_week.append((closep, highp))
        else:
            curr_20_week.append((closep, highp))
            prev_20_week.append((closep, highp))

    return (prev_20_week, curr_20_week)

#def WeeklyTrend(AllStockNames, BoughtStocks, AcceptableStopLoss):
def WeeklyTrend(date, WeeklyDict, AcceptableStopLoss, BoughtStocks, indexName):
    '''
        date - Current date in a tuple (year, month, day)
        WeeklyDict - Dictionary with key as week number from current date, dating back to 11 weeks and value as dictionary of all the stocks and corresponding open, close, high, low prices.
        AcceptableStopLoss - Stop loss percentage
        BoughtStocks - List of all the names of the stocks that are bought by the user with the buy price 
    '''
    entryStocks = []
    exitStocks = []
    stopLoss = AcceptableStopLoss
    # Convert the list of names to dictionary and initialize them to false
    StockNameDict = {key: False for (key, value) in WeeklyDict[0].items()}
    StockNameDict.pop(indexName, None)

    # If a stock is bought by the user then change the value to true
    for stock, buyPrice in BoughtStocks:
        if stock in StockNameDict:
            StockNameDict[stock] = True

    BoughtStocksDict = dict(BoughtStocks)

    ### Use the stock names to open the respective data files and read the data
    #### Downward trend
    #prev_20_week = [(20.0, 25.0), (21.0, 21.0), (21.5, 21.9), (21.2, 21.3), (21.9, 22.1), (22.8, 22.9), (22.5, 22.7), (22.9, 23.0), (22.4, 22.7), (22.3, 22.4), (23.2, 23.5), (23.9, 25.0), (24.5, 25.0), (24.9, 25.5), (25.7, 28.0), (27.1, 27.5), (27.2, 27.8), (27.5, 27.5), (27.3, 27.8), (27.2, 27.3)]
    #curr_20_week = [(19.8, 21.0), (20.0, 25.0), (21.0, 21.0), (21.5, 21.9), (21.2, 21.3), (21.9, 22.1), (22.8, 22.9), (22.5, 22.7), (22.9, 23.0), (22.4, 22.7), (22.3, 22.4), (23.2, 23.5), (23.9, 25.0), (24.5, 25.0), (24.9, 25.5), (25.7, 28.0), (27.1, 27.5), (27.2, 27.8), (27.5, 27.5), (27.3, 27.8)]
    #### Upward trend
    #prev_20_week = [(27.2, 27.3), (27.3, 27.8), (27.5, 27.5), (27.2, 27.8), (27.1, 27.5), (25.7, 28.0), (24.9, 25.5), (24.5, 25.0), (23.9, 25.0), (23.2, 23.5), (22.3, 22.4), (22.4, 22.7), (22.9, 23.0), (22.5, 22.7), (22.8, 22.9), (21.9, 22.1), (21.2, 21.3), (21.5, 21.9), (21.0, 21.0), (20.0, 25.0)]
    #curr_20_week = [(27.6, 28.9), (27.2, 27.3), (27.3, 27.8), (27.5, 27.5), (27.2, 27.8), (27.1, 27.5), (25.7, 28.0), (24.9, 25.5), (24.5, 25.0), (23.9, 25.0), (23.2, 23.5), (22.3, 22.4), (22.4, 22.7), (22.9, 23.0), (22.5, 22.7), (22.8, 22.9), (21.9, 22.1), (21.2, 21.3), (21.5, 21.9), (21.0, 21.0)]

    (prev_20_week_index, curr_20_week_index) = IndexDataSegregation(WeeklyDict, indexName)
    indexMA = IndexTrend(prev_20_week_index, curr_20_week_index)

    #f = open('test.txt', 'a')

    # Loop the entry and exit checks for each stock. 
    # Check entry condition only for the stocks that are not bought.
    # Check exit condition only for the stocks that are bought.
    for key, value in StockNameDict.items():
        curr_20_week = []
        prev_20_week = []

        # Find the data for given 'key' symbol for each week. Take this data and append to the list
        for k, v in WeeklyDict.items():
            if key in v: (openp, highp, lowp, closep) = v[key]
            else: continue
            
            if k == 0:
                curr_20_week.append((closep, highp))
            elif k == 20:
                prev_20_week.append((closep, highp))
            else:
                curr_20_week.append((closep, highp))
                prev_20_week.append((closep, highp))

        # If stock is not bought
        if not value:
            #entry = EntryPoint(prev_20_week, curr_20_week)
            roc = ROCCheck(curr_20_week)
            breakout = BreakoutCheck(curr_20_week)
            #s = 'Name = ' + key + ', IndexMA = ' + str(indexMA) + ', Breakout = ' + str(breakout) + ', ROC = ' + str(roc) + '\n'
            #f.write(s)

            if indexMA and roc > 30 and breakout:
                entryStocks.append(key)
            #print('Stock - {}, Entry - {}'.format(key, entry))
        # If stock is bought
        else:
            mov_avg = MovingAverageTrend(prev_20_week[0:9], curr_20_week[0:9])
            if not mov_avg:
                stopLoss = 10

            exitSig = ExitSignal(BoughtStocksDict[key], stopLoss, curr_20_week[0][0])
            if exitSig:
                exitStocks.append(key)
            #print('Stock - {}, Exit - {}'.format(key, exitSig))
    
    return (entryStocks, exitStocks)

if __name__ == '__main__':
    # Test sample of stock names
    # Get name of the stocks from a file. Assuming the bought stocks come in a list
    names = ["ABC", "AHD", "BAS", "SND", "EUN", "ZIN", "IWE", "EIJ", "AJJ", "AJE", "POE", "FJN", "GJK", "NED", "BEP", "IDM", "QMA", "WIO", "FIP"]
    boughtStocks = [("AHD", 50.0), ("EUN", 25.0), ("WIO", 30.0), ("IDM", 35.0), ("IWE", 15.0), ("AJE", 23.0), ("POE", 28.0)]
    AcceptableStopLoss = 40
    
    filenm = datetime.date(2021, 3, 19).strftime("%Y-%m-%d") + '-weekly-data-dict.txt'
    with open(filenm, 'r') as file:
        weeklydict = json.loads(filenm) # use `json.loads` to do the reverse

    print(weeklydict)
    #WeeklyTrend(names, boughtStocks, AcceptableStopLoss)