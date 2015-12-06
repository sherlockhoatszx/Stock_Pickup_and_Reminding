# -*- coding: utf-8 -*-
#!/usr/bin/env python
#Done: filter the date when close price cross the ma5 line
#todo1:the defination of "the 'first time' cross ma5 line" 
#todo2:replace the end date with today automatically
#2AM Dec-7-2015,sherlock


import tushare as ts
import time
from datetime import date

#enddate = now 

today =date.today()
x = ts.get_hist_data('601318',ktype='60',start ='2015-12-01',end = '2015-12-05')
#error happens:' can't compare datetime.date to unicode',when i try to replace the end value 
#with today 
print x 




x['judger']=x['close']-x['ma5']
x['judger']=x['judger']*1
x['increaseRate']=x['judger']/x['ma5'] 
y = x[x.increaseRate>0.02]
#above is to filter the dataframe with the condition:
#close price is 2% more than ma5 



print x


print y

print today
