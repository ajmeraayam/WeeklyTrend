import datetime

def preprocess(current_date):
    '''
        current_date - current_date is a tuple of (year, month, day). This is the date from which we want to check the trend in past

        The funtion will take a current date and find the current week number. Now it will try to recover all the data from this date till last 11 weeks (including this week). The data can be recovered from files for each day. 

        Once a file is opened, its data will be stored in a dictionary where key will be the symbol (short name) of the stock and data will be a tuple of its concerning open, close, high, low and other data
    '''
    #file = open("TestData/2021-01-04-NSE-EQ.txt")
    #for line in file:
    #    print(line)
    weeklyDict = dict()
    current_week = datetime.date(current_date[0], current_date[1], current_date[2]).isocalendar()[1]
    current_year = current_date[0]
    #print(type(datetime.date(2021, 1, 4).isocalendar()))
    print(datetime.date.fromisocalendar(2021, 0, 1))

    #for weekInPast in range(0, 11):
    #    firstDayOfWeek = datetime.date.fromisocalendar(current_year, current_week - weekInPast, 1)
    #    lastDayOfWeek = datetime.date.fromisocalendar(current_year, current_week - weekInPast, 5)

if __name__ == '__main__':
    preprocess((2021, 3, 19))