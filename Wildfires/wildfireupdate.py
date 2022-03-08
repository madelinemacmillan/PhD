all_emissions=all_emissions.drop(columns=['County Name','Date Local','Datum','Latitude','Longitude','MDL','Site Num','State Name','Units of Measure'])
all_emissions.columns=['Month','Day','Year','Hour','PM 2.5']
all_emissions[['Hour','Drop']] = all_emissions['Hour'].str.split(':',expand=True)
all_emissions=all_emissions.drop(columns=['Drop'])
all_emissions = all_emissions.astype({"Hour": int})#,'Day': int,'Month':int,'Year':int,'PM 2.5': float})
all_emissions['Hour'] += 1
#

july_2010=demand['july_2010']
july_2011=demand['july_2011']
july_2012=demand['july_2012']
july_2013=demand['july_2013']
july_2014=demand['july_2014']
july_2015=demand['july_2015']
july_2016=demand['july_2016']
july_2017=demand['july_2017']
july_2018=demand['july_2018']
july_2019=demand['july_2019']

august_2010=demand['august_2010']
august_2011=demand['august_2011']
august_2012=demand['august_2012']
august_2013=demand['august_2013']
august_2014=demand['august_2014']
august_2015=demand['august_2015']
august_2016=demand['august_2016']
august_2017=demand['august_2017']
august_2018=demand['august_2018']
august_2019=demand['august_2019']

september_2010=demand['september_2010']
september_2011=demand['september_2011']
september_2012=demand['september_2012']
september_2013=demand['september_2013']
september_2014=demand['september_2014']
september_2015=demand['september_2015']
september_2016=demand['september_2016']
september_2017=demand['september_2017']
september_2018=demand['september_2018']
september_2019=demand['september_2019']

frames1=[july_2010,august_2010,september_2010,july_2011,august_2011,september_2011,july_2012,august_2012,september_2012,july_2013,august_2013,september_2013,july_2014,august_2014,september_2014,july_2015,august_2015,september_2015,july_2016,august_2016,september_2016,july_2017,august_2017,september_2017,july_2018,august_2018,september_2018,july_2019,august_2019,september_2019]

all_demand=pd.concat(frames1,ignore_index=True,sort=False)

all_demand=all_demand.drop(columns=['INTERVALSTARTTIME_GMT', 'INTERVALENDTIME_GMT', 'LOAD_TYPE', 'OPR_INTERVAL', 'MARKET_RUN_ID', 'LABEL', 'XML_DATA_ITEM','POS','EXECUTION_TYPE','GROUP'])
all_demand[['Year','Month','Day']] = all_demand['OPR_DT'].str.split('-',expand=True)
all_demand=all_demand.loc[all_demand['TAC_AREA_NAME']=='SDGE-TAC']
all_demand=all_demand.drop(columns=['TAC_AREA_NAME','OPR_DT'])
all_demand.columns = ['Hour', 'MW','Year','Month','Day']
all_demand = all_demand.astype({"Hour": int,'Day': int,'Month':int,'Year':int})

all_demand['Date-Time']=all_demand['Year'].astype(str)+'_'+all_demand['Month'].astype(str)+'_'+all_demand['Day'].astype(str)+'_'+all_demand['Hour'].astype(str)
all_emissions.dropna()
all_emissions = all_emissions.fillna(0)
all_emissions.drop(all_emissions.loc[all_emissions['PM 2.5']=='inf'].index, inplace=True)
all_emissions = all_emissions.astype({'Day': int,'Month':int,'Year':int})

all_emissions['Date-Time']=all_emissions['Year'].astype(str)+'_'+all_emissions['Month'].astype(str)+'_'+all_emissions['Day'].astype(str)+'_'+all_emissions['Hour'].astype(str)
all_demand = all_demand.set_index('Date-Time')
all_emissions['DT'] = all_emissions['Date-Time']
all_emissions = all_emissions.set_index('Date-Time')
all_demand=all_demand.drop(columns=['Hour','Month','Day','Year'])
all_emissions=all_emissions.drop(columns=['Month','Day','Year'])

all_features = all_demand.merge(all_emissions,how='outer',right_index=True,left_index=True)

weather = pd.read_csv('weather_data.csv')
weather = weather.set_index('Date-Time')

fires=pd.read_csv('sd_fires.csv')
fires=fires.drop(columns=['Unnamed: 0', 'DISCOVERY_DATE','CONT_DATE','DISCOVERY_TIME','CONT_TIME','OBJECTID', 'FOD_ID','STAT_CAUSE_CODE', 'STAT_CAUSE_DESCR', 'FPA_ID', 'SOURCE_SYSTEM_TYPE','SOURCE_SYSTEM', 'NWCG_REPORTING_AGENCY', 'NWCG_REPORTING_UNIT_ID','NWCG_REPORTING_UNIT_NAME', 'SOURCE_REPORTING_UNIT','SOURCE_REPORTING_UNIT_NAME', 'LOCAL_FIRE_REPORT_ID','LOCAL_INCIDENT_ID', 'FIRE_CODE', 'FIRE_NAME','ICS_209_INCIDENT_NUMBER', 'ICS_209_NAME', 'MTBS_ID', 'MTBS_FIRE_NAME', 'COMPLEX_NAME', 'LATITUDE','LONGITUDE', 'OWNER_CODE', 'OWNER_DESCR', 'STATE', 'COUNTY','FIPS_CODE', 'FIPS_NAME', 'Shape'])
fires=fires.loc[(fires['FIRE_YEAR'] >= 2010)]#& fires['FIRE_YEAR'] <=2019]
fires=fires.loc[(fires['FIRE_SIZE_CLASS'] != 'A')]
fires=fires.loc[(fires['CONT_DOY'] != 'nan')]
fires=fires.dropna(subset=['CONT_DOY'])
fires['Duration']=fires['CONT_DOY']-fires['DISCOVERY_DOY']
fires=fires.mask(fires==0).fillna(1)
months=['01','02','03','04','05','06','07','08','09','10','11','12']
days=fires[['DISCOVERY_DOY','FIRE_YEAR']].copy()
month_day=[]
for i,y in zip(days['DISCOVERY_DOY'],days['FIRE_YEAR']):
    if y != 2012:
        if i <= 31:
          month_day.append('1_'+str(i))
        elif i > 31 and i <= 59:
            d=i-31
            month_day.append('2_'+str(d))
        elif i > 59 and i <= 90:
            d=i-59
            month_day.append('3_'+str(d))
        elif i > 90 and i <= 120:
            d=i-90
            month_day.append('4_'+str(d))
        elif i > 120 and i <= 151:
            d=i-120
            month_day.append('5_'+str(d))
        elif i > 151 and i <= 181:
            d=i-151
            month_day.append('6_'+str(d))
        elif i > 181 and i <= 212:
            d=i-181
            month_day.append('7_'+str(d))
        elif i > 212 and i <= 243:
            d=i-212
            month_day.append('8_'+str(d))
        elif i > 243 and i <= 273:
            d=i-243
            month_day.append('9_'+str(d))
        elif i > 273 and i <= 304:
            d=i-273
            month_day.append('10_'+str(d))
        elif i > 304 and i <= 334:
            d=i-304
            month_day.append('11_'+str(d))
        elif i > 334 and i <= 365:
            d=i-334
            month_day.append('12_'+str(d))
    elif y==2012:
        if i <= 31:
          month_day.append('1_'+str(i))
        elif i > 31 and i <= 60:
            d=i-31
            month_day.append('2_'+str(d))
        elif i > 60 and i <= 91:
            d=i-60
            month_day.append('3_'+str(d))
        elif i > 91 and i <= 121:
            d=i-91
            month_day.append('4_'+str(d))
        elif i > 121 and i <= 152:
            d=i-121
            month_day.append('5_'+str(d))
        elif i > 152 and i <= 182:
            d=i-152
            month_day.append('6_'+str(d))
        elif i > 182 and i <= 213:
            d=i-182
            month_day.append('7_'+str(d))
        elif i > 213 and i <= 244:
            d=i-213
            month_day.append('8_'+str(d))
        elif i > 244 and i <= 274:
            d=i-244
            month_day.append('9_'+str(d))
        elif i > 274 and i <= 305:
            d=i-274
            month_day.append('10_'+str(d))
        elif i > 305 and i <= 335:
            d=i-305
            month_day.append('11_'+str(d))
        elif i > 335 and i <= 366:
            d=i-335
            month_day.append('12_'+str(d))
            
fires['date']=month_day
fires['DateYear']=fires['FIRE_YEAR'].astype(str)+'_'+fires['date'].astype(str)
fires=fires.drop(columns=['FIRE_YEAR','date','DISCOVERY_DOY','CONT_DOY'])

size = fires["DateYear"].size
fires = fires.loc[fires.index.repeat(24)]
hours = np.arange(24) + 1
h = np.tile(hours, size)
fires["Hour_"] = h
fires['Date_Time']=fires['DateYear'].astype(str)+'_'+fires['Hour_'].astype(str)
fires=fires.drop(columns=['DateYear'])
fires['DT_']=fires['Date_Time']
fires = fires.set_index('Date_Time')
fires['Fire']=1
##all_features_test=all_features
all_features=all_features.merge(fires,how='outer',right_index=True,left_index=True)
all_features_test=all_features
all_features=all_features.merge(weather,how='outer',right_index=True,left_index=True)
#
all_features['FIRE_SIZE_CLASS'] = all_features['FIRE_SIZE_CLASS'].fillna('A')
all_features['FIRE_SIZE'] = all_features['FIRE_SIZE'].fillna(0)
all_features['Fire'] = all_features['Fire'].fillna(0)