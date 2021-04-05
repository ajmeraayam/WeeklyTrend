from DataPreprocessor import preprocess
from WeeklyTrend import WeeklyTrend

def main():
    weeklyIndexDict = preprocess((2021, 3, 19))
    # Date, weekly data, acceptable stop loss, bought stocks - symbol and buy price
    (entryStocks, exitStocks) = WeeklyTrend((2021, 3, 19), weeklyIndexDict, 40, 10, 'NSE500')
    print(exitStocks)


if __name__ == '__main__':
    main()
