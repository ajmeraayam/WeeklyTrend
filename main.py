from DataPreprocessor import preprocess
from WeeklyTrend import WeeklyTrend

def main():
    weeklyIndexDict = preprocess((2021, 3, 19), 'NSE500')
    # Date, weekly data, acceptable stop loss, bought stocks - symbol and buy price
    (entry, exitst) = WeeklyTrend((2021, 3, 19), weeklyIndexDict, 40, [], 'NSE500')
    #print(entry)


if __name__ == '__main__':
    main()
