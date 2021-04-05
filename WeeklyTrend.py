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

def BreakoutCheck(curr_20_week):
    curr_highest_high = curr_20_week[0][1]

    for i in range(1, len(curr_20_week)):
        if curr_highest_high <= curr_20_week[i][1]:
            return False
    
    return True

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

def WeeklyTrend(date, WeeklyDict, AcceptableStopLoss, TrailingStopLoss, indexName):
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

    # Find if index is in uptrend or downtrend 
    (prev_20_week_index, curr_20_week_index) = IndexDataSegregation(WeeklyDict, indexName)
    indexMA = IndexTrend(prev_20_week_index, curr_20_week_index)

    #f = open('test.txt', 'a')
    #f2 = open('test2.txt', 'a')

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

        # Check Rate of Change for last 20 weeks
        roc = ROCCheck(curr_20_week)
        # Find if current closing price is greater than highest high for last 20 weeks
        breakout = BreakoutCheck(curr_20_week)
        #s = 'Name = ' + key + ', IndexMA = ' + str(indexMA) + ', Breakout = ' + str(breakout) + ', ROC = ' + str(roc) + '\n'
        #f.write(s)

        # If index is in uptrend, ROC is greater than 30% and current closing price is highest in last 20 weeks
        # then send a buy signal
        if indexMA and roc > 30 and breakout:
            entryStocks.append(key)

        # If index is in downtrend then change the stop loss to trailing loss  
        if not indexMA:
            stopLoss = TrailingStopLoss

        ex_roc = ROCCheck(curr_20_week[0:2])
        #s2 = 'Name = ' + key + ', IndexMA = ' + str(indexMA) + ', ROC = ' + str(ex_roc) + '\n'
        #f2.write(s2)
        # Check if Rate of Change for 2 weeks from current date is below stop loss.
        # If so, send a sell signal
        if ex_roc <= (-stopLoss):
            exitStocks.append(key)
    
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