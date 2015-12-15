#! -*- coding: utf-8 -*-
import pandas as pd
import tushare as ts
import sae.kvdb as sdb
from datetime import datetime

# 建立 KVDB 连接
kvdb = sdb.Client()

# 股票代码前缀
K15 = '15'
K60 = '60'
KDAY = 'D'
KWEEK = 'W'
# KVDB 中键名常量, 全部以'K_'开始
# 中证500成分股列表
K_ZZ500 = 'zz500s'
# 沪深300成分股列表
K_HS300 = 'hs300s'
# 沪深股市全部股票列表
K_HSA = 'hsa'
# 交易日列表开始时间
K_BEGIN_DATE = '2015-09-01'
# 交易日列表
K_TRX_DATE = 'trx_date'
# 最后交易日
K_LAST_TRX_DATE = 'last_trx_date'


def update_trx_date():
    """
    更新自 2015/9/1 以来的交易日列表. 交易日**9:30**以后调取此接口可以可将当日添加到此列表
    中.该函数**每日9:45**调用.(**部分待测试)
    :return: None
    """
    # kvdb 中尚无交易日列表
    if kvdb.get(K_TRX_DATE) is None:
        # 通过沪指获取交易日期
        trx_date = ts.get_h_data('000001', start=K_BEGIN_DATE, index=True).index
        trx_date_list = [date.strftime('%Y-%m-%d') for date in trx_date]
        kvdb.set(K_TRX_DATE, trx_date_list)
    else:
        trx_date_list = kvdb.get(K_TRX_DATE)
        today = ts.get_h_data('000001',
                              start=datetime.now().strftime('%Y-%m-%d'),
                              index=True)
        if today is not None:
            trx_date_list.insert(0, today.index[0].strftime('%Y-%m-%d'))
    # 更新最后交易日
    kvdb.set(K_LAST_TRX_DATE, trx_date_list[0])


def update_stock_list():
    """
    更新沪深股票/沪深300/中证500股票列表, 每日**9:30**调用该函数进行更新
    :return: None
    """
    # 更新沪深A股
    hsa = ts.get_stock_basics().index
    kvdb.set(K_HSA, hsa)
    # 更新沪深300
    hs300 = ts.get_hs300s().code
    kvdb.set(K_HS300, hs300)
    # 更新中证500
    zz500 = ts.get_zz500s()
    kvdb.set(K_ZZ500, zz500)


def update_stock_data(code, ktype, date=None):
    """
    更新股票K线数据
    :param code: 股票代码
    :param ktype: K线类型, ('15', '60', 'D', 'W')
    :param date: 日期, 默认最后交易日
    :return:
    """
    if date is None:
        date = kvdb.get(K_LAST_TRX_DATE)
    key = ktype + '-' + code
    old_data = kvdb.get(key)
    # No old data
    if old_data is None:
        trx_date = kvdb.get(K_TRX_DATE)
        # Number of Transaction Date
        ntd = len(trx_date)
        if ktype == '15':
            start_date = trx_date[min(5, ntd - 1)]
        elif ktype == '60':
            start_date = trx_date[min(20, ntd - 1)]
        elif ktype == 'D':
            start_date = trx_date[min(30, ntd - 1)]
        elif ktype == 'W':
            start_date = trx_date[min(40, ntd - 1)]
        new_data = ts.get_hist_data(code, start_date, ktype=ktype, pause=1)
    else:
        _ = ts.get_hist_data(code, datetime.now().strftime('%Y-%m-%d'),
                             ktype=ktype, pause=1)
        new_index = [i for i in _.index if i not in old_data.index]
        new_data = pd.concat([_.ix[new_index], old_data],
                             verify_integrity=True)
    # new_data 只保留最近数据
    if ktype == '15':
        # number of records
        nor = 80
    elif ktype == '60':
        nor = 60
    elif ktype == 'D':
        nor = 30
    elif ktype == 'W':
        nor = 8
    new_data = new_data.ix[new_data.index[0:nor]]
    kvdb.set(key, new_data)


def get_stock_data(code, ktype):
    """
    返回数据库中存储的股票数据
    :param code: 股票代码, str
    :param ktype: K线类型, ('15', '60', 'D', 'W'), str
    :return: K线数据, DataFrame
    """
    key = str(ktype) + '-' + str(code)
    return kvdb.get(key)


if __name__ == '__main__':
    update_trx_date()
    print kvdb.get(K_LAST_TRX_DATE)
    update_stock_data('601989', ktype='W')
    print len(kvdb.get('W-601989').index)
    update_stock_data('601989', ktype='W')
    print len(kvdb.get('W-601989').index)
    print get_stock_data('601989', 'W')
