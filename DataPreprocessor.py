import datetime
import pandas as pd
import sys
import os.path
import json

def preprocess(current_date):
    '''
        current_date - current_date is a tuple of (year, month, day). This is the date from which we want to check the trend in past

        The funtion will take a current date and find the current week number. Now it will try to recover all the data from this date till last 11 weeks (including this week). The data can be recovered from files for each day. 

        Once a file is opened, its data will be stored in a dictionary where key will be the symbol (short name) of the stock and data will be a tuple of its concerning open, close, high, low and other data
    '''
    ignoreSymbolsDict = {'NSENIFTY':True, 'NIFTYJUNIOR':True, 'NIFTYMIDCAPLIQ15':True, 'NSE100':True, 'NIFTY200':True, 'NSEMIDCAP150':True, 'MIDCAP50':True, 'NSEMIDCAP':True, 'NSESMLCAP100':True, 'NIFTYLARGEMIDCAP250':True, 'NIFTYAUTO':True, 'BANKNIFTY':True, 'NIFTYFINSERVICE':True, 'NIFTYFMGC':True, 'NSEIT':True, 'NIFTYMEDIA':True, 'NIFTYMETAL':True, 'NIFTYPHARMA':True, 'NIFTYPVTBANK':True, 'NIFTYPSUBANK':True, 'NIFTYREALTY':True, 'NIFTYCOMMODITIES':True, 'NIFTYCONSUMPTION':True, 'NIFTYCPSE':True, 'NIFTYENERGY':True, 'NIFTY100ESG':True, 'NIFTY100ENHESG':True, 'NIFTYINFRA':True, 'NIFTYMNC':True, 'NIFTYPSE':True, 'NIFTYSMEEMERGE':True, 'NIFTYSERVSECTOR':True, 'NIFTYSHARIAH25':True, 'NIFTY50SHARIAH':True, 'NIFTY500SHARIAH':True, 'NIFTYABGROUP':True, 'NIFTYMAHINDRA':True, 'NIFTYTATA':True, 'NIFTYTATA25CAP':True, 'NIFTYABGROUP':True, 'NIFTYLIQ15':True, 'NIFTY500VALUE50':True, 'NIFTYQUALLOWVOL30':True, 'NIFTYALPHAQUALLOWVOL30':True, 'NIFTYALPHAQUALVALLOWVOL30':True, 'NIFTY50EQUALWEIGHT':True, 'NIFTY100EQUALWEIGHT':True, 'NIFTY100LOWVOL30':True, 'NSEDEFTY':True, 'NIFTY50DIVPOINT':True, 'NIFTYDIVOPPS50':True, 'NIFTYALPHA50':True, 'NIFTY50ARBITRAGE':True, 'NIFTY50FUTINDEX':True, 'NIFTY50FUTTRINDEX':True, 'NIFTYHIGHBETA50':True, 'NIFTYLOWVOL50':True, 'NIFTY50VALUE20':True, 'NIFTYGROWSECT15':True, 'NIFTY50TR2XLEV':True, 'NIFTY50PR2XLEV':True, 'NIFTY50TR1XINV':True, 'NIFTY50PR1XINV':True, 'NIFTY-GS-COMPSITE':True, 'NIFTY-GS-4-8YR':True, 'NIFTY-GS-8-13YR':True, 'NIFTY-GS-10YR':True, 'NIFTY-GS-10YR-CLN':True, 'NIFTY-GS-11-15YR':True, 'NIFTY-GS-15YRPLUS':True, 'VIX':True}

    weeklyDict = dict()
    current_week = datetime.date(current_date[0], current_date[1], current_date[2]).isocalendar()[1]
    # Use this only for the loop
    current_year = current_date[0]
    ### CHANGE TO 20 weeks
    last_week = current_week - 21 if current_week >= 21 else current_week - 22
    
    week_count = 0

    for weekInPast in range(current_week, last_week, -1):
        if weekInPast == 0:
            continue

        # Convert negative week to positive week number by looping around number of weeks
        if weekInPast > 0:
            week = weekInPast % (datetime.date(current_year, 12, 28).isocalendar()[1] + 1)
        else:
            current_year = current_date[0] - 1
            week = weekInPast % (datetime.date(current_year, 12, 28).isocalendar()[1] + 1)   
        
        firstDayOfWeek = datetime.date.fromisocalendar(current_year, week, 1)
        lastDayOfWeek = datetime.date.fromisocalendar(current_year, week, 5)
        daterange = pd.date_range(firstDayOfWeek, lastDayOfWeek)
        
        weeklyStockDataDict = dict()
        for date in daterange:
            filename = 'TestData/' + date.strftime("%Y-%m-%d") + '-NSE-EQ.txt'
            # File doesn't exist, then skip
            if not os.path.exists(filename): 
                continue

            f = open(filename)
            lines = f.readlines()
            
            for line in range(1, len(lines)):
                strings = lines[line].split(",")
                if strings[0] in ignoreSymbolsDict: continue
                dailyDataSegregation(weeklyStockDataDict, strings, firstDayOfWeek, lastDayOfWeek, date)

        weeklyDict[week_count] = weeklyStockDataDict
        week_count += 1

    return weeklyDict
    #filenm = datetime.date(current_date[0], current_date[1], current_date[2]).strftime("%Y-%m-%d") + '-weekly-data-dict.txt'
    #with open(filenm, 'w') as file:
    #    file.write(json.dumps(weeklyDict)) # use `json.loads` to do the reverse       

def dailyDataSegregation(weeklyStockDataDict, strings, firstDayOfWeek, lastDayOfWeek, date):
    '''
        weeklyStockDataDict - Given week's open, high, low and close data for all stocks
        strings - a line from the data file
        firstDayOfWeek - Datetime.date class type for first working day of the week
        lastDayOfWeek - Datetime.date class type for last working day of the week
        date - current date that is being processed
    '''
    # If the stock exists in the dictionary
    if strings[0] not in weeklyStockDataDict:
        weeklyStockDataDict[strings[0]] = (-1,sys.float_info.min,sys.float_info.max,-1)

    (openp, highp, lowp, closep) = weeklyStockDataDict[strings[0]]
    # If highest price reached today is higher than previous days highs, then replace it 
    highp = highp if highp > float(strings[3]) else float(strings[3])
    # If lowest price reached today is lower than previous days lows, then replace it 
    lowp = lowp if lowp < float(strings[4]) else float(strings[4])
    closep = float(strings[5])

    # If first day of the week, use the open price of this day as the open price for the week
    if date.date() == firstDayOfWeek:
        weeklyStockDataDict[strings[0]] = (float(strings[2]), highp, lowp, closep)
    # If last day of the week, use the close price of this day as the close price for the week
    # If any day other than first day
    else:
        if openp == -1: openp = float(strings[2])
        weeklyStockDataDict[strings[0]] = (openp, highp, lowp, closep)

if __name__ == '__main__':
    preprocess((2021, 3, 19))