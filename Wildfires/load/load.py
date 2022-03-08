from io import BytesIO
from zipfile import ZipFile
import urllib.request
import pandas as pd
import sys
import os
import csv
    
# years=['2010']#,'2011','2012','2013','2014','2015','2016','2017','2018','2019']
# months=['01','02','03']#,'04','05','06','07','08','09','10','11','12']
# #days_in_month=['31','28','31','30','31','30','31','31','30','31','30','31']

# index_months=[0,1,2]#,3,4,5,6,7,8,9,10,11]
# index_years=[0]#,1,2,3,4,5,6,7,8,9]
# data=[]
# for y in index_years:
#     for m in index_months:
#         if m != 11: #going to next year
#             print(m,y)
#             url = urllib.request.urlopen("http://oasis.caiso.com/oasisapi/SingleZip?queryname=SLD_FCST&market_run_id=ACTUAL&resultformat=6&startdatetime="+years[y]+months[m]+"01T08:00-0000&enddatetime="+years[y]+months[m+1]+"01T07:00-0000&version=1")
#             with ZipFile(BytesIO(url.read())) as my_zip_file:
#                 for contained_file in my_zip_file.namelist():
#                     for line in my_zip_file.open(contained_file).readlines():
#                         data.append(line)
#         else:
#             print(m,y)
#             url = urllib.request.urlopen("http://oasis.caiso.com/oasisapi/SingleZip?queryname=SLD_FCST&market_run_id=ACTUAL&resultformat=6&startdatetime="+years[y]+months[m]+"01T08:00-0000&enddatetime="+years[y+1]+months[0]+"01T07:00-0000&version=1")
#             with ZipFile(BytesIO(url.read())) as my_zip_file:
#                 for contained_file in my_zip_file.namelist():
#                     for line in my_zip_file.open(contained_file).readlines():
#                         data.append(line)


# def write_to_csv(list_of_emails):
#      with open('data.csv', 'w', newline='') as csvfile:
#          writer = csv.writer(csvfile, delimiter = '\n')
#          writer.writerow(list_of_emails)

# write_to_csv(data)  


# import necessary libraries
# use glob to get all the csv files 
# in the folder
import pandas as pd
import glob

path = r'C:\Users\mmacmill\Documents\PhD Materials\PhD\Wildfires\load' # use your path
all_files = glob.glob(path + "/*.csv")

li = []
n=0
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)
    n=n+1
    print(n)

frame = pd.concat(li, axis=0, ignore_index=True)


frame=frame.drop(labels=["INTERVALSTARTTIME_GMT","INTERVALENDTIME_GMT","EXECUTION_TYPE","XML_DATA_ITEM","MARKET_RUN_ID",
"OPR_INTERVAL","LOAD_TYPE","LABEL","GROUP","POS"],axis=1) #remove all unnecessary columns
load= frame[frame.TAC_AREA_NAME == 'PGE-TAC'] #filter out all TAC except for relevant utility, PGE
