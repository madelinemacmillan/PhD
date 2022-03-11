from io import BytesIO
from zipfile import ZipFile
import urllib.request
import pandas as pd
import sys
import os
import csv
    
####read data
# import pandas as pd
# import glob

# path = r'C:\Users\mmacmill\Documents\PhD Materials\PhD\Wildfires\load' # use your path
# all_files = glob.glob(path + "/*.csv")

# li = []
# n=0
# for filename in all_files:
#     df = pd.read_csv(filename, index_col=None, header=0)
#     li.append(df)
#     n=n+1
#     print(n)

# frame = pd.concat(li, axis=0, ignore_index=True)


# frame=frame.drop(labels=["INTERVALSTARTTIME_GMT","INTERVALENDTIME_GMT","EXECUTION_TYPE","XML_DATA_ITEM","MARKET_RUN_ID",
# "OPR_INTERVAL","LOAD_TYPE","LABEL","GROUP","POS"],axis=1) #remove all unnecessary columns
# load= frame[frame.TAC_AREA_NAME == 'PGE-TAC'] #filter out all TAC except for relevant utility, PGE
# load.to_csv('load.csv')

####normalize column names
load=pd.read_csv('load.csv')
load[['Month','Day','Year']] = load['OPR_DT'].str.split('-',expand=True)
load=load.drop(columns=['OPR_DT'])




####merge data, drop duplicates



