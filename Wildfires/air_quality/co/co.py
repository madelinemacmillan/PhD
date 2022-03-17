from io import BytesIO
from zipfile import ZipFile
import urllib.request
import pandas as pd
import sys
import os
import csv
import bz2
import pickle
import _pickle as cPickle
import pandas as pd
import glob
from dask import dataframe as dd
import dask

path = r'C:\Users\mmacmill\OneDrive - NREL\PhD Materials\PhD\Wildfires\air_quality\co' # use your path
all_files = glob.glob(path + "/*.csv")

li = []
n=0
for filename in all_files:
    df = pd.read_csv(filename)
    li.append(df)
    n=n+1
    print(n)

air=pd.concat(li,axis=0)

air=air.drop(labels=['State Code','Parameter Code','County Code','Site Num','POC','Datum','Date GMT','Time GMT','Uncertainty','Qualifier','Method Type','Units of Measure','Method Code','Method Name','Date of Last Change'],axis=1) #remove all unnecessary columns
print(air.size)

air=air.rename(columns={'Parameter Name':'Parameter_Name', 'Date Local':'Date_Local', 'Time Local':'Time_Local', 'Sample Measurement':'Sample_Measurement', 'State Name':'State_Name', 'County Name':'County_Name'})
print(air.State_Name.unique())

air=air[air.State_Name == 'California']
air=air[air.County_Name == 'Butte']
air.to_csv('co.csv')
