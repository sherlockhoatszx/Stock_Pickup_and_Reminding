# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Done: filter the date when close price cross the ma5 line
# todo1:the defination of "the 'first time' cross ma5 line"
# todo2:replace the end date with today automatically
# 2AM Dec-7-2015,sherlock
# # todo1:the defination of "the 'first time' cross ma5 line"   - Done
# # todo2:replace the end date with today automatically         - Done
# # 2AM Dec-7-2015,sherlock
#
# 1AM Dec-8-2015, siyuan


import tushare as ts
from datetime import date
from numpy import any

# today =date.today()
# x = ts.get_hist_data('601318',ktype='60',start ='2015-12-01',end = '2015-12-05')
# error happens:' can't compare datetime.date to unicode',when i try to replace the end value
# with today
# print x
# x['judger']=x['close']-x['ma5']
# x['judger']=x['judger']*1
# x['increaseRate']=x['judger']/x['ma5']
# y = x[x.increaseRate>0.02]
# above is to filter the dataframe with the condition:
# close price is 2% more than ma5


count = 0


def stock_filter(code, begin):

    """
    Function to decide whether a stock meets the criteria: 1) close price over ma[60] 2) first
     time 3) for 2 percent. To approximate, use ma5 in 15 minutes level to replace average
     in 60 minutes level. A stock will be counted only if its close price is over ma[60] for the
     first time in 20 consecutive 15-minute intervals, and the price is high than ma[60] by 2%.
    :param code: stock's code string
    :param begin: beginning date
    :return: True if the stock satisfies the criterion, or else False
    """
    global count
    print 'Processing %s (%s) ... ' % (code, count)
    count = count + 1
    data = ts.get_hist_data(code, ktype='15', start=begin)  # 15-minute candlestick data
    # 有效突破 ma5: 超过 ma5 两个百分点
    data['chm'] = (data['close'] - 1.02 * data['ma5']) > 0
    nor = len(data.index)   # number of records
    if nor < 20:    # some stock may have no enough records due to IPO or suspension
        return False
    # 若最后一期未能有效突破 ma5 或在过去 19 期内已经有效突破 ma5 则滤掉
    if (not data['chm'][0]) \
       or any(data['chm'][1:20]):
        return False

    return True


def spr():
    """
    Main interface
    :return: a filtered stock list
    """
    global count
    today = date.today().strftime('%Y-%m-%d').encode()
    trx_date = ts.get_hist_data('sh').index

    if today in trx_date:
        # four days included today
        begin = trx_date[2].encode()
    else:
        # four days excluded today
        begin = trx_date[3].encode()
    print 'Starting from %s ...' % str(begin)

    # get full stock list
    print 'Getting stock list ...',
    stock_list = ts.get_zz500s().code
    print 'Done: %s stocks' % len(stock_list)
    # filtering process
    count = 0
    return filter(lambda x: stock_filter(x, begin), stock_list)


if __name__ == '__main__':
    stocks = spr()
    print stocks
