# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 11:42:50 2023

@author: benne
"""

import joblib
from pybaseball import statcast
import numpy as np
from statistics import mean

rawData = statcast(start_dt="2023-9-02", end_dt="2023-9-03")
rawData = rawData[["pitch_type","pfx_x","pfx_z","release_speed","release_spin_rate"]]
rawData=rawData[rawData["pitch_type"].str.contains('FF|CH|SL|CU', na=False)]

np.random.seed(1)
df1 = rawData.sample(1) 

pitchtype=df1['pitch_type'].values

vb_traj=df1.pfx_x.iloc[0]
hb_traj=df1.pfx_z.iloc[0]
velo=df1.release_speed.iloc[0]
totalspin=df1.release_spin_rate.iloc[0]

vb_traj=abs(vb_traj*12)
hb_traj=abs(hb_traj*12)
#print (vb_traj)

X_input=np.array([[vb_traj+5,hb_traj,velo,totalspin]])
print (X_input)
#X_input.reshape(1,-1)


pfx_x_FB_min=-2.0183453072982163
pfx_x_FB_max= 2.0183453072982163
pfx_z_FB_min=-4.706491700184713
pfx_z_FB_max=3.104321032223065
velo_FB_min=-4.063066140231642 
velo_FB_max=3.4844466582306075
spin_FB_min= -6.256341752721373 
spin_FB_max=4.054490617759393

pfx_x_CH_min= -3.990389733219817 
pfx_x_CH_max= 2.539771902723787
pfx_z_CH_min= -1.5562449762658164 
pfx_z_CH_max= 3.6032029914884216
velo_CH_min= -9.04663256787433 
velo_CH_max= 2.779113956009813
spin_CH_min= -3.3670740613967136 
spin_CH_max= 3.4103198334862226

pfx_x_SL_min= -1.3363225151532006 
pfx_x_SL_max= 3.994889180157588
pfx_z_SL_min= -1.3564920235903455 
pfx_z_SL_max= 4.947893791753892
velo_SL_min= -3.822361605602511 
velo_SL_max= 3.1079652079711257
spin_SL_min= -5.800766165373565 
spin_SL_max= 3.663344750267779

pfx_x_CU_min= -1.9185064129354714 
pfx_x_CU_max= 2.9139204440171103
pfx_z_CU_min= -2.0689688301824596 
pfx_z_CU_max= 2.2478920653987617
velo_CU_min= -3.591337522299007 
velo_CU_max= 2.7293660462037357
spin_CU_min= -2.663753459343813 
spin_CU_max= 2.8004011601305234

lower_bound=-3
upper_bound=3
print (X_input.shape)    
print(X_input)

if pitchtype == "FF":
    FB_scaler=joblib.load("FB_scaler_z.save")
    FB_input=FB_scaler.transform(X_input)
    print (FB_input)
    #FB_input=X_input
    for i in range(0,len(FB_input[0])):
        if (i==0):
            FB_input[0][i]=lower_bound+(FB_input[0][i]-pfx_x_FB_min) * (upper_bound - lower_bound) / (pfx_x_FB_max - pfx_x_FB_min)
        if (i==1):
            FB_input[0][i]=lower_bound+(FB_input[0][i]-pfx_z_FB_min) * (upper_bound - lower_bound) / (pfx_z_FB_max - pfx_z_FB_min)
        if (i==2):
            FB_input[0][i]=lower_bound+(FB_input[0][i]-velo_FB_min) * (upper_bound - lower_bound) / (velo_FB_max - velo_FB_min)
        if (i==3):
            FB_input[0][i]=lower_bound+(FB_input[0][i]-spin_FB_min) * (upper_bound - lower_bound) / (spin_FB_max - spin_FB_min)
    
    output=mean(FB_input[0])*10+50
    
elif pitchtype == "CH":
    CH_scaler=joblib.load("CH_scaler_z.save")
    CH_input=CH_scaler.fit_transform(X_input)
    
    for i in range(0,len(CH_input[0])):
        if (i==0):
            CH_input[0][i]=lower_bound+(CH_input[0][i]-pfx_x_CH_min) * (upper_bound - lower_bound) / (pfx_x_CH_max - pfx_x_CH_min)
        if (i==1):
            CH_input[0][i]=lower_bound+(CH_input[0][i]-pfx_z_CH_min) * (upper_bound - lower_bound) / (pfx_z_CH_max - pfx_z_CH_min)
        if (i==2):
            CH_input[0][i]=lower_bound+(CH_input[0][i]-velo_CH_min) * (upper_bound - lower_bound) / (velo_CH_max - velo_CH_min)
        if (i==3):
            CH_input[0][i]=lower_bound+(CH_input[0][i]-spin_CH_min) * (upper_bound - lower_bound) / (spin_CH_max - spin_CH_min)
    
    output=mean(CH_input[0])*10+50
    
elif pitchtype =="SL":
    SL_scaler=joblib.load("SL_scaler_z.save")
    SL_input=SL_scaler.fit_transform(X_input)
    
    for i in range(0,len(SL_input[0])):
        if (i==0):
            SL_input[0][i]=lower_bound+(SL_input[0][i]-pfx_x_SL_min) * (upper_bound - lower_bound) / (pfx_x_SL_max - pfx_x_SL_min)
        if (i==1):
            SL_input[0][i]=lower_bound+(SL_input[0][i]-pfx_z_SL_min) * (upper_bound - lower_bound) / (pfx_z_SL_max - pfx_z_SL_min)
        if (i==2):
            SL_input[0][i]=lower_bound+(SL_input[0][i]-velo_SL_min) * (upper_bound - lower_bound) / (velo_SL_max - velo_SL_min)
        if (i==3):
            SL_input[0][i]=lower_bound+(SL_input[0][i]-spin_SL_min) * (upper_bound - lower_bound) / (spin_SL_max - spin_SL_min)
    
    output=mean(SL_input[0])*10+50
    
elif pitchtype == "CU":
    CU_scaler=joblib.load("CU_scaler_z.save")
    CU_input=CU_scaler.fit_transform(X_input)
    
    for i in range(0,len(CU_input[0])):
        if (i==0):
            CU_input[0][i]=lower_bound+(CU_input[0][i]-pfx_x_CU_min) * (upper_bound - lower_bound) / (pfx_x_CU_max - pfx_x_CU_min)
        if (i==1):
            CU_input[0][i]=lower_bound+(CU_input[0][i]-pfx_z_CU_min) * (upper_bound - lower_bound) / (pfx_z_CU_max - pfx_z_CU_min)
        if (i==2):
            CU_input[0][i]=lower_bound+(CU_input[0][i]-velo_CU_min) * (upper_bound - lower_bound) / (velo_CU_max - velo_CU_min)
        if (i==3):
            CU_input[0][i]=lower_bound+(CU_input[0][i]-spin_CU_min) * (upper_bound - lower_bound) / (spin_CU_max - spin_CU_min)
    
    output=mean(CU_input[0])*10+50
print('')
print('')
print ("Output is " +str(round(output,2)))
    