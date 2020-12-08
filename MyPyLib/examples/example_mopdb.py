# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 15:33:03 2019

@author: blaumax
"""

#import relevant packages
from moalib.mopdb import mopdb as mopdb
import pandas as pd



#create MOPDB object
mopdb = mopdb()
#establish connection to MOPDB via credentials stored in RegKey for current windows user
conn=mopdb.conn

#define the query to be executed in MOPDB:
sql_query="select 'it works' as example from dual"

#run query on MOPDB, store in a pandas object and print output in console
print(pd.read_sql(sql_query,conn))

#close database connection
conn.close()