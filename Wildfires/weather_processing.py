#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 12:55:46 2020

@author: cbarraug
"""
import pandas as pd
import numpy as np

ozone = pd.read_csv("ozone.csv")
co=pd.read_csv("co.csv")
load=pd.read_csv("load.csv")

load=load.drop(columns=['Unnamed: 0','TAC_AREA_NAME'])

##Adjust hours to be the same

co[['Hour','Trash']] = co['Time_Local'].str.split(':',expand=True)
co=co.drop(columns=['Time_Local','Trash','State_Name','County_Name','Unnamed: 0'])
co['Hour'] = co['Hour'].astype('int64')
co.Hour = co.Hour.mask( co.Hour >= 0, co.Hour + 1)

ozone[['Hour','Trash']] = ozone['Time_Local'].str.split(':',expand=True)
ozone=ozone.drop(columns=['Time_Local','Trash','State_Name','County_Name','Unnamed: 0'])
ozone['Hour'] = ozone['Hour'].astype('int64')
ozone.Hour = ozone.Hour.mask( ozone.Hour >= 0, ozone.Hour + 1)

##drop locations that won't be used (keep the location with the most data)


#Join files based on date and hour
co['combined']=co['Date_Local'].astype(str)+'-'+co['Hour'].astype(str)
ozone['combined']=ozone['Date_Local'].astype(str)+'-'+ozone['Hour'].astype(str)
load['combined']=load['OPR_DT'].astype(str)+'-'+load['OPR_HR'].astype(str)

air = pd.merge(co, ozone, on="combined")
data = pd.merge(air, load, on="combined")