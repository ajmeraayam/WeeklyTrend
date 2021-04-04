from DataPreprocessor import preprocess
from WeeklyTrend import WeeklyTrend

def main():
    weeklyDict = preprocess((2021, 3, 19))
    # Date, weekly data, acceptable stop loss, bought stocks - symbol and buy price
    WeeklyTrend((2021, 3, 19), weeklyDict, 40, [])


if __name__ == '__main__':
    main()
