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

    # Calculate 10 week average for current week to last 10 weeks and previous week to last 10 weeks
    sum = 0
    for i in range(0, 10):
        sum = sum + prev_20_week[i][0]

    avg_prev_10_weeks = sum / 10
    
    sum = 0
    for i in range(0, 10):
        sum = sum + curr_20_week[i][0]

    avg_curr_10_weeks = sum / 10

    # Point 1 - 10 week moving average of the stock/index must be greater than last week
    if avg_curr_10_weeks > avg_prev_10_weeks:
        mov_avg_cond = True

    print('Current moving average - {}, Previous moving average - {}'.format(avg_curr_10_weeks, avg_prev_10_weeks))
    print('Moving average condition - {}'.format(mov_avg_cond))    
    # Point 2 - 20 week ROC must be above 30%
    # FORMULA - ((current closing price - closing price 20 weeks ago) / closing price 20 weeks ago) * 100
    roc = ((curr_20_week[0][0] - curr_20_week[-1][0])/curr_20_week[-1][0]) * 100

    if roc > 30:
        ROC_cond = True

    print('ROC in percentage - {}'.format(roc))
    print('ROC condition - {}'.format(ROC_cond))
    # Point 3 - Stock must close above a new 20 week high
    # Current closing price should be above highest highs that have occured in last 20 weeks
    curr_highest_high = curr_20_week[0][1]

    for i in range(1, len(curr_20_week)):
        if curr_highest_high <= curr_20_week[i][1]:
            highest_high_cond = False
            break
    
    print('Highest high condition - {}'.format(highest_high_cond))

    # If all the 3 conditions have been satisfied then this stock can be bought
    if mov_avg_cond and ROC_cond and highest_high_cond:
        return True
    
    return False

def WeeklyTrend():
    #prev_20_week = [(20.0, 25.0), (21.0, 21.0), (21.5, 21.9), (21.2, 21.3), (21.9, 22.1), (22.8, 22.9), (22.5, 22.7), (22.9, 23.0), (22.4, 22.7), (22.3, 22.4), (23.2, 23.5), (23.9, 25.0), (24.5, 25.0), (24.9, 25.5), (25.7, 28.0), (27.1, 27.5), (27.2, 27.8), (27.5, 27.5), (27.3, 27.8), (27.2, 27.3)]
    #curr_20_week = [(19.8, 21.0), (20.0, 25.0), (21.0, 21.0), (21.5, 21.9), (21.2, 21.3), (21.9, 22.1), (22.8, 22.9), (22.5, 22.7), (22.9, 23.0), (22.4, 22.7), (22.3, 22.4), (23.2, 23.5), (23.9, 25.0), (24.5, 25.0), (24.9, 25.5), (25.7, 28.0), (27.1, 27.5), (27.2, 27.8), (27.5, 27.5), (27.3, 27.8)]
    
    prev_20_week = [(27.2, 27.3), (27.3, 27.8), (27.5, 27.5), (27.2, 27.8), (27.1, 27.5), (25.7, 28.0), (24.9, 25.5), (24.5, 25.0), (23.9, 25.0), (23.2, 23.5), (22.3, 22.4), (22.4, 22.7), (22.9, 23.0), (22.5, 22.7), (22.8, 22.9), (21.9, 22.1), (21.2, 21.3), (21.5, 21.9), (21.0, 21.0), (20.0, 25.0)]
    curr_20_week = [(27.6, 28.9), (27.2, 27.3), (27.3, 27.8), (27.5, 27.5), (27.2, 27.8), (27.1, 27.5), (25.7, 28.0), (24.9, 25.5), (24.5, 25.0), (23.9, 25.0), (23.2, 23.5), (22.3, 22.4), (22.4, 22.7), (22.9, 23.0), (22.5, 22.7), (22.8, 22.9), (21.9, 22.1), (21.2, 21.3), (21.5, 21.9), (21.0, 21.0)]

    entry = EntryPoint(prev_20_week, curr_20_week)
    print(entry)
    #pass

if __name__ == '__main__':
    WeeklyTrend()