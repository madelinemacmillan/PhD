#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 12:55:46 2020

@author: cbarraug
"""
import pandas as pd
import numpy as np

df = pd.read_csv("weather.csv")

split = df["DATE"].str.split("-", expand=True)

df["YEAR"] = split[0]
#df["YEAR"] = "20" + df["YEAR"]
df

df["MONTH"] = split[1]

df["DAY"] = split[2]

daily_size = df["YEAR"].size

df = df.loc[df.index.repeat(24)]
#
#hours = np.arange(24) + 1
#
#h = np.tile(hours, daily_size)
#
#df["HOUR"] = h
#
#delimiter = "_"
#
#
#df["Date-Time"] = df["YEAR"].astype(str) + delimiter + df["MONTH"].astype(str) + delimiter + df["DAY"].astype(str) + delimiter + df["HOUR"].astype(str)
#
#df = df.drop(["DATE", "YEAR", "MONTH", "DAY", "HOUR"], axis=1)
##
#df = df.set_index("Date-Time")
#
#df.to_csv("weather_data2.csv")
#weather2=weather
#frames = [df,weather2]
#
#weather_new = pd.concat(frames)
#
#print(df.head())
