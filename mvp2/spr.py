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
    # print 'Processing %s (%s) ... ' % (code, count)
    count += 1
    data = ts.get_hist_data(code, ktype='30', start=begin)  # ktype-minute candlestick data
    # 有效突破 ma5: 超过 ma5 两个百分点
    data['chm'] = (data['close'] - 1.02 * data['ma10']) > 0
    nor = len(data.index)   # number of records
    if nor < 20:    # some stock may have no enough records due to IPO or suspension
        return False
    # 若最后一期未能有效突破 ma5 或在过去 19 期内已经有效突破 ma5 则滤掉
    if (not data['chm'][0]) \
       or any(data['chm'][1:20]):
        return False

    return True


def ver_hammer(code, begin):
    """Function to recognise if the chart fits the revers hammer
    criteria: before today ,the line is in decrease curve,high 6% more than low,
    and open is 2% more than low, and close is less than 1% above the low.
    :param code: stock's code string
    :param begin: beginning date
    :return:    True if the stock satisfies the criterion, or else False
    """
    global count
    # print 'Processing %s (%s) ... ' % (code, count)
    count += 1
    data = ts.get_hist_data(code, ktype='60', start=begin)  # ktype-minute candlestick
    nor = len(data.index)
    if nor < 4:
        return False
    
    x = data.loc[data.index[0],["open","close","high","low"]]
    y = data.close

    if y[1] < y[2] <y[3] \
            and x.high / x.low > 1.1 \
            and x.close / x.low < 1.01 \
            and x.open / x.close < 1.03:
        return True

    return False


def feature3(code,begin):
    '''15分钟价格第一次上穿ma60(ma60需要计算）或者ma20第一次上穿ma60
        在15分钟的k线数据中取最近60个close price算术平均值为ma60,ma20可以直接通过ts获取无需自行计算
        :param code: stock's code string
        :param begin: beginning date
        :param end: end date
        :return: True if the stock satisfies the criterion, or else False
    '''
    global count
    print 'Processing %s (%s) in feature3...' % (code, count)
    count = count + 1
    #取最近5天的数据计算ma60
    data_5days = ts.get_hist_data(code, ktype='15', start=begin)
    #获取15分钟k线用作判断价格是否穿越ma60,数据按照时间升序排列
    data_15_mins = ts.get_hist_data(code,ktype='15',start=begin).sort_index()
    #股票停牌导致没有数据?
    if len(data_15_mins.index) == 0:
        return False
    else:
        for i in range(len(data_15_mins.index)):
            #取最近60个记录的close算术均值
            ma60 = data_5days[i:60+i].mean()['close']
            if data_15_mins['close'][i] > ma60 \
                or data_15_mins['ma20'][i] > ma60:
                    return True
            else:
                    return False    
# 参见 https://github.com/sherlockhoatszx/Stock_Pickup_and_Reminding/issues/7
#filter_funcs = [stock_filter, ver_hammer,feature3]
filter_funcs = [feature3]   
    
def spr(filter_func, begin):
    """
    Main interface
    :param filter_func: 股票筛选函数,返回 True or False
    :param begin: beginning date
    :return: a filtered stock list
    """
    global count

    # get full stock list
    # print 'Getting stock list ...',
    stock_list = ts.get_zz500s().code
    # print 'Done: %s stocks' % len(stock_list)
    # filtering process
    count = 0
    print "筛选方式 %s" % filter_func.__name__
    return filter(lambda x: filter_func(x, begin), stock_list)


if __name__ == '__main__':
    today = date.today().strftime('%Y-%m-%d').encode()
    trx_date = ts.get_hist_data('sh').index

    if today in trx_date:
        # four days included today
        _begin = trx_date[3].encode()
    else:
        # four days excluded today
        _begin = trx_date[4].encode()
    print 'Starting from %s ...' % str(_begin)

    for func in filter_funcs:
        print spr(func, _begin)
