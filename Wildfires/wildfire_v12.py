# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 11:06:04 2020

@author: mmacmill
"""

import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import sklearn as sk
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge, Lasso, SGDClassifier
from sklearn.ensemble import AdaBoostRegressor
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.metrics import classification_report
from sklearn.decomposition import PCA, KernelPCA
from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score, r2_score, explained_variance_score, make_scorer, mean_squared_error
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.feature_selection import VarianceThreshold, SelectKBest, chi2

years=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
year_two=[10,11,12,13,14,15,16,17,18,19]
months=['july','august','september']
#
#import pm2.5 data
emissions={}
for y in year_two:
  year=str(y)
  filetype='.csv'
  filename='pm'+year+filetype
  out = pd.read_csv(filename)
  emissions[y]=out
  print(y)
  
#import demand data
demand={}
for y in years:
  for m in months:
    year=str(y)
    month=str(m)
    monthyear=month + '_' + year
    filetype='.csv'
    filename= monthyear + filetype
    print(filename)
    out = pd.read_csv(filename)
    demand[monthyear]=out
  print(y)

emissions_2010=emissions[10]
emissions_2011=emissions[11]
emissions_2012=emissions[12]
emissions_2013=emissions[13]
emissions_2014=emissions[14]
emissions_2015=emissions[15]
emissions_2016=emissions[16]
emissions_2017=emissions[17]
emissions_2018=emissions[18]
emissions_2019=emissions[19]

frames = [emissions_2010,emissions_2011,emissions_2012,emissions_2013,emissions_2014,emissions_2015,emissions_2016,emissions_2017,emissions_2018,emissions_2019]
all_emissions = pd.concat(frames,ignore_index=True,sort=False)

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


#merging features together
all_features=all_features.merge(fires,how='outer',right_index=True,left_index=True)
all_features_test=all_features
all_features=all_features.merge(weather,how='outer',right_index=True,left_index=True)
#
all_features['FIRE_SIZE_CLASS'] = all_features['FIRE_SIZE_CLASS'].fillna('A')
all_features['FIRE_SIZE'] = all_features['FIRE_SIZE'].fillna(0)
all_features['Fire'] = all_features['Fire'].fillna(0)
#
all_features = all_features[all_features['MW'].notna()]
all_features = all_features[all_features['PM 2.5'].notna()]
all_features = all_features[all_features['TMAX'].notna()]
all_features = all_features[all_features['TMIN'].notna()]
all_features = all_features[all_features['AWND'].notna()]
all_features = all_features[all_features['PRCP'].notna()]


#
all_features=all_features.fillna(value=0)
#
#
all_features = all_features[~all_features.index.duplicated(keep='first')]
all_features[['Year','Month','Day','Hour']] = all_features['DT'].str.split('_',expand=True)
all_features=all_features.drop(columns=['Hour_','DT_','DT'])
all_features = all_features[all_features['Year'] < '2015']  
all_features=all_features.drop(columns=['Year','Month','Day'])
##fires=fires.mask(fires==0).fillna(1)

all_features['FIRE_SIZE_CLASS'] = all_features['FIRE_SIZE_CLASS'].replace('A',1)
all_features['FIRE_SIZE_CLASS'] = all_features['FIRE_SIZE_CLASS'].replace('B',2)
all_features['FIRE_SIZE_CLASS'] = all_features['FIRE_SIZE_CLASS'].replace('C',3)
all_features['FIRE_SIZE_CLASS'] = all_features['FIRE_SIZE_CLASS'].replace('D',4)
all_features['FIRE_SIZE_CLASS'] = all_features['FIRE_SIZE_CLASS'].replace('E',5)
all_features['FIRE_SIZE_CLASS'] = all_features['FIRE_SIZE_CLASS'].replace('F',6)
all_features['FIRE_SIZE_CLASS'] = all_features['FIRE_SIZE_CLASS'].replace('G',7)





X = all_features[['Fire','TMAX','TMIN','AWND','PRCP','PM 2.5','FIRE_SIZE','FIRE_SIZE_CLASS','Hour']].copy()
y = all_features[['MW']].copy()
#######
############PCA#######
pca = PCA(n_components=5)#, kernel='rbf')
X_transformed = pca.fit_transform(X,y)
#######
#########
X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, train_size=0.8) #, shuffle=False)
#####
####y_binary=y
####y_binary['binary']=(y['MW']>3900).astype(int) #,how='outer',right_index=True,left_index=True)
####y=y.drop(columns=['binary'])
####y_binary=y_binary.drop(columns=['MW'])
#####
####pca = KernelPCA(n_components=5, kernel='rbf')
####X_transformedb = pca.fit_transform(X,y_binary)
####
####X_trainb, X_testb, y_trainb, y_testb = train_test_split(X, y_binary, train_size=0.8)
####
########REGRESSION#########
####regression=make_pipeline(StandardScaler(),SVR(kernel='linear',C=1.0,epsilon=0.1))
####regression.fit(X_train,y_train)
####r2_regr=regression.score(X_test,y_test)
####
####ridge=Ridge(alpha=1.0)
####ridge.fit(X_train,y_train)
####r2_ridge=ridge.score(X_test,y_test)
####
####lasso=Lasso(alpha=0.1)
####lasso.fit(X_train,y_train)
####r2_lasso=lasso.score(X_test,y_test)
####
####r,c=X_train.shape
####
####clf=AdaBoostRegressor()
####parameters={'loss':('linear','square','exponential'), 'n_estimators':[10,20,100,300,10000,r],'learning_rate':[0.5, 1, 3]}
####boost=GridSearchCV(clf,parameters,scoring=make_scorer(r2_score))
####boost.fit(X_train,y_train)
####r2_boost=boost.score(X_test,y_test)
####params_boost=boost.best_params_
###
boost=AdaBoostRegressor()
boost.fit(X_train,y_train)
r2_boost=boost.score(X_test,y_test)
boost_labels=boost.predict(X_test)
boost_mse=mean_squared_error(y_test,boost_labels)
##
###
####
#########CLASSIFICATION######
###gaus_nb=GaussianNB()
###gaus_nb.fit(X_trainb,y_trainb)
###acc_gaus=gaus_nb.score(X_testb,y_testb)
###gaus_labels=gaus_nb.predict(X_testb)
###report_gaus=classification_report(y_testb,gaus_labels)
###
###bern_nb=BernoulliNB()
###bern_nb.fit(X_trainb,y_trainb)
###acc_bern=bern_nb.score(X_testb,y_testb)
###bern_labels=bern_nb.predict(X_testb)
###report_bern=classification_report(y_testb,bern_labels)
###
###parameters={'loss':('hinge','log','modified_huber','squared_hinge','perceptron','squared_loss','huber'), 'penalty':('l2','l1','elasticnet'),'alpha':[0.0001,0.001,0.01,0.1],'max_iter':[10,100,1000,10000]}
####scores={'f1':make_scorer(f1_score),'recall':make_scorer(recall_score),'precision':make_scorer(precision_score)}
###clf=SGDClassifier()
###sgd_precision=GridSearchCV(clf,parameters,scoring=make_scorer(precision_score))
###sgd_precision.fit(X_trainb,y_trainb)
###accuracy_sgd_precision=sgd_precision.score(X_testb,y_testb)
###sgd_labels_precision=sgd_precision.predict(X_testb)
###report_sgd_precision=classification_report(y_testb,sgd_labels_precision)
###results_precision=sgd_precision.cv_results_
###params_precision=sgd_precision.best_params_
###
###clf=SGDClassifier()
###sgd_recall=GridSearchCV(clf,parameters,scoring=make_scorer(recall_score))
###sgd_recall.fit(X_trainb,y_trainb)
###accuracy_sgd_recall=sgd_recall.score(X_testb,y_testb)
###sgd_labels_recall=sgd_recall.predict(X_testb)
###report_sgd_recall=classification_report(y_testb,sgd_labels_recall)
###results_recall=sgd_recall.cv_results_
###params_recall=sgd_recall.best_params_
###
###sgd=SGDClassifier(loss='hinge',penalty='elasticnet',alpha=0.0001,max_iter=1000)
###sgd.fit(X_trainb,y_trainb)
###accuracy_sgd=sgd.score(X_testb,y_testb)
###sgd_labels=sgd.predict(X_testb)
##
###i=0
###acc=[]
###pre=[]
###rec=[]
###f1=[]
###sup=[]
###while i<20:
###    sgd=SGDClassifier(loss='hinge',penalty='elasticnet',alpha=0.0001,max_iter=1000)
###    sgd.fit(X_trainb,y_trainb)
###    acc.append(sgd.score(X_testb,y_testb))
###    sgd_labels=sgd.predict(X_testb)
###    precision,recall,fscore,support=score(y_testb,sgd_labels,labels=[0,1])
###    pre.append(precision[1])
###    rec.append(recall[1])
###    f1.append(fscore[1])
###    sup.append(support[1])
###    i+=1
##
###report_sgd=classification_report(y_testb,sgd_labels)
###precision, recall, f-1
##
##
##
##
