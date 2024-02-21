# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 10:53:08 2023

@author: bennett stice
"""

#Pull designated statcast data
import pandas as pd
#import pybaseball
#from pybaseball import pitching_stats
from pybaseball import statcast
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import log_loss
import random
import joblib
import warnings
warnings.filterwarnings('ignore')

rawData = statcast(start_dt="2023-9-02", end_dt="2023-10-02")
rawData = rawData[["pitch_type","pfx_x","pfx_z","release_speed","release_spin_rate"]]
rawData=rawData[rawData["pitch_type"].str.contains('FF|CH|SL|CU', na=False)]

np.random.seed(1)
df1 = rawData.sample(20) 

#NAN checks in data
df1 = df1[pd.notna(df1['release_speed'])]
df1 = df1[pd.notna(df1['release_spin_rate'])]
df1 = df1[pd.notna(df1['pfx_x'])]
df1 = df1[pd.notna(df1['pfx_z'])]
df1= df1[pd.notna(df1['pitch_type'])]



for i in range (0,len(df1.pfx_x)):
    df1.pfx_x.iloc[i]=abs(df1.pfx_x.iloc[i]*12)
for i in range (0,len(df1.pfx_z)):
    df1.pfx_z.iloc[i]=abs(df1.pfx_z.iloc[i]*12)
    
#seperates numeric, catagorical, and response coloumns
X_num = df1[["pfx_x","pfx_z","release_speed","release_spin_rate"]].values
X_cat = df1["pitch_type"].values

print (X_num)
    
    
############## Cut up values based on pitch type ##################

X_FB=[]

X_CH=[]

X_SL=[]

X_CU=[]


for i in range (0, len(df1.pfx_x)):
    if X_cat[i]=='FF':
        X_FB.append(X_num[i])

    elif X_cat[i]=='CH':
        X_CH.append(X_num[i])
            
    elif X_cat[i]=='SL':
        X_SL.append(X_num[i])
        
    elif X_cat[i]=='CU':
        X_CU.append(X_num[i])
    
    
    
##################### Scale all values ###################

FB_scaler= StandardScaler()
CH_scaler= StandardScaler()
SL_scaler= StandardScaler()
CU_scaler= StandardScaler()

X_FB_sca = FB_scaler.fit_transform(X_FB)
X_CH_sca = CH_scaler.fit_transform(X_CH)
X_SL_sca = SL_scaler.fit_transform(X_SL)
X_CU_sca = CU_scaler.fit_transform(X_CU)

joblib.dump(FB_scaler,'FB_scaler_z.save')
joblib.dump(CH_scaler,'CH_scaler_z.save')
joblib.dump(SL_scaler,'SL_scaler_z.save')
joblib.dump(CU_scaler,'CU_scaler_z.save')

pfx_x_FB=[]
pfx_z_FB=[]
velo_FB=[]
spin_FB=[]

for i in range (0,len(X_FB_sca)):
    pfx_x_FB.append(X_FB_sca[i][0])
    pfx_z_FB.append(X_FB_sca[i][1])
    velo_FB.append(X_FB_sca[i][2])
    spin_FB.append(X_FB_sca[i][3])

pfx_x_FB_min=min(pfx_x_FB)
pfx_z_FB_min=min(pfx_z_FB)
velo_FB_min=min(velo_FB)
spin_FB_min=min(spin_FB)

pfx_x_FB_max=max(pfx_x_FB)
pfx_z_FB_max=max(pfx_z_FB)
velo_FB_max=max(velo_FB)
spin_FB_max=max(spin_FB)

print("pfx_x FB min: "+str(pfx_x_FB_min)+" pfx_x FB max: " + str(pfx_x_FB_max))
print("pfx_z FB min: "+str(pfx_z_FB_min)+" pfx_z FB max: " + str(pfx_z_FB_max))
print("velo FB min: "+str(velo_FB_min)+" velo FB max: " + str(velo_FB_max))
print("spin FB min: "+str(spin_FB_min)+" spin FB max: " + str(spin_FB_max))
print('')

pfx_x_CH=[]
pfx_z_CH=[]
velo_CH=[]
spin_CH=[]

for i in range (0,len(X_CH_sca)):
    pfx_x_CH.append(X_CH_sca[i][0])
    pfx_z_CH.append(X_CH_sca[i][1])
    velo_CH.append(X_CH_sca[i][2])
    spin_CH.append(X_CH_sca[i][3])

pfx_x_CH_min=min(pfx_x_CH)
pfx_z_CH_min=min(pfx_z_CH)
velo_CH_min=min(velo_CH)
spin_CH_min=min(spin_CH)

pfx_x_CH_max=max(pfx_x_CH)
pfx_z_CH_max=max(pfx_z_CH)
velo_CH_max=max(velo_CH)
spin_CH_max=max(spin_CH)

print("pfx_x CH min: "+str(pfx_x_CH_min)+" pfx_x CH max: " + str(pfx_x_CH_max))
print("pfx_z CH min: "+str(pfx_z_CH_min)+" pfx_z CH max: " + str(pfx_z_CH_max))
print("velo CH min: "+str(velo_CH_min)+" velo CH max: " + str(velo_CH_max))
print("spin CH min: "+str(spin_CH_min)+" spin CH max: " + str(spin_CH_max))
print('')

pfx_x_SL=[]
pfx_z_SL=[]
velo_SL=[]
spin_SL=[]

for i in range (0,len(X_SL_sca)):
    pfx_x_SL.append(X_SL_sca[i][0])
    pfx_z_SL.append(X_SL_sca[i][1])
    velo_SL.append(X_SL_sca[i][2])
    spin_SL.append(X_SL_sca[i][3])

pfx_x_SL_min=min(pfx_x_SL)
pfx_z_SL_min=min(pfx_z_SL)
velo_SL_min=min(velo_SL)
spin_SL_min=min(spin_SL)

pfx_x_SL_max=max(pfx_x_SL)
pfx_z_SL_max=max(pfx_z_SL)
velo_SL_max=max(velo_SL)
spin_SL_max=max(spin_SL)

print("pfx_x SL min: "+str(pfx_x_SL_min)+" pfx_x SL max: " + str(pfx_x_SL_max))
print("pfx_z SL min: "+str(pfx_z_SL_min)+" pfx_z SL max: " + str(pfx_z_SL_max))
print("velo SL min: "+str(velo_SL_min)+" velo SL max: " + str(velo_SL_max))
print("spin SL min: "+str(spin_SL_min)+" spin SL max: " + str(spin_SL_max))
print('')

pfx_x_CU=[]
pfx_z_CU=[]
velo_CU=[]
spin_CU=[]

for i in range (0,len(X_CU_sca)):
    pfx_x_CU.append(X_CU_sca[i][0])
    pfx_z_CU.append(X_CU_sca[i][1])
    velo_CU.append(X_CU_sca[i][2])
    spin_CU.append(X_CU_sca[i][3])

pfx_x_CU_min=min(pfx_x_CU)
pfx_z_CU_min=min(pfx_z_CU)
velo_CU_min=min(velo_CU)
spin_CU_min=min(spin_CU)

pfx_x_CU_max=max(pfx_x_CU)
pfx_z_CU_max=max(pfx_z_CU)
velo_CU_max=max(velo_CU)
spin_CU_max=max(spin_CU)

print("pfx_x CU min: "+str(pfx_x_CU_min)+" pfx_x CU max: " + str(pfx_x_CU_max))
print("pfx_z CU min: "+str(pfx_z_CU_min)+" pfx_z CU max: " + str(pfx_z_CU_max))
print("velo CU min: "+str(velo_CU_min)+" velo CU max: " + str(velo_CU_max))
print("spin CU min: "+str(spin_CU_min)+" spin CU max: " + str(spin_CU_max))
print('')

print (X_CH_sca[4])