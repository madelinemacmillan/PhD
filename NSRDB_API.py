# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 11:58:50 2022

@author: mmacmill
"""
import pandas as pd
import numpy as np
import sys, os
from IPython.display import display
# Declare all variables as strings. Spaces must be replaced with '+', i.e., change 'John Smith' to 'John+Smith'.
# Define the lat, long of the location and the year
lat, lon, year = 39.7596, -121.6219, 2018 #i tried defining these as strings--no luck
# You must request an NSRDB api key from the link above
api_key = '5WWb1fodzAanZfgwIHbtUqD6ESJy0TGdpALwPdKu'
# Set the attributes to extract (e.g., dhi, ghi, etc.), separated by commas.
attributes = 'ghi,dhi,dni,clearsky_dhi'
# Choose year of data
year = '2018'
# Set leap year to true or false. True will return leap day data if present, false will not.
leap_year = 'false'
# Set time interval in minutes, i.e., '30' is half hour intervals. Valid intervals are 30 & 60.
interval = '60'
# Specify Coordinated Universal Time (UTC), 'true' will use UTC, 'false' will use the local time zone of the data.
# NOTE: In order to use the NSRDB data in SAM, you must specify UTC as 'false'. SAM requires the data to be in the
# local time zone.
utc = 'false'
# Your full name, use '+' instead of spaces.
your_name = 'Madeline+Macmillan'
# Your reason for using the NSRDB.
reason_for_use = 'REopt+analysis'
# Your affiliation
your_affiliation = 'Mines+and+NREL'
# Your email address
your_email = 'madeline.macmillan@nrel.gov'
# Please join our mailing list so we can keep you up-to-date on new developments.
mailing_list = 'false'

# Declare url string
url = 'https://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes)
# Return just the first 2 lines to get metadata:
info = pd.read_csv(url, nrows=1)
df = pd.read_csv(url)
df.to_csv('paradise_2018_1.csv')

##other_url=https://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?wkt=POINT(-121.6219%2039.7596)&names=2018&leap_day=false&interval=60&utc=false&full_name=Madeline+Macmillan&email=madeline.macmillan@nrel.gov&affiliation=Mines+and+NREL&mailing_list=false&reason=REopt+analysis&api_key=5WWb1fodzAanZfgwIHbtUqD6ESJy0TGdpALwPdKu&attributes=ghi,dhi,dni,clearsky_ghi,clearsky_dhi,clearsky_dni
# See metadata for specified properties, e.g., timezone and elevation
timezone, elevation = info['Local Time Zone'], info['Elevation']