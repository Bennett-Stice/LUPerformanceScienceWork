# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:15:35 2023

@author: bennett stice
"""
import scipy.stats as stats
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np



Names=["Walsh","McQuiston","Stice","Salazar","Jungers","Brown","Buschschulte",
       "Darin","Council","Rakers","Subbert","Newell","James","Jackson"]
AVG_SPIN=[2300,2000,2000,2100,2100,2100,2000,2000,1700,1900,2000,2000,1700,2100]
AVG_IVB=[14.4,15.2,15.6,14.4,11.7,17.4,13.6,11.4,13.3,-0.2,19.4,15.1,10,13.1]
SPIN_EFF=[85,82,90,92,95,98,97,74,91,97,98,99,76,96]
BB_AVG_SPIN=[2300,2200,2100,2400,2300,1900,2400,2100,1600,1900,2200,2200,1700,2500]

y_val=[AVG_SPIN,AVG_IVB,SPIN_EFF,BB_AVG_SPIN]

y_val_list=["AVG_SPIN","AVG_IVB","SPIN_EFF","BB_AVG_SPIN"]

all_finger_tip_peak=[151.3,133.6,174.0,175.9,171.5,129.7,159.0,
       196.1,151.1,167.8,182.4,175.7,157.6,90.8]
index_finger_tip_peak=[46.6,45.6,63.9,75.9,51.1,66.4,59.8,
       70.3,59.1,52.4,72.3,64.2,57.1,37.8]
middle_finger_tip_peak=[59.1,53.5,70.2,78.9,65.1,58.0,64.5,
       67.1,61.1,36.6,84.1,67.8,69.3,45.8]
ring_finger_tip_peak=[45.5,28.5,49.1,65.6,42.4,41.9,49.3,
       48.0,60.2,34.1,59.0,50.5,42.9,31.6]
pinky_finger_tip_peak=[30.1,25.0,31.5,44.0,35.3,28.7,31.9,
       29.4,35.1,29.7,46.7,41.9,26.9,26.2]
ulnar_deviation_peak=[59.3,39.4,83.3,65.9,65.5,58.6,54.4,
       64.9,64.1,80.5,71.0,66.4,67.0,50.4]

all_finger_ext_peak=[32.7,23.4,39.4,36.3,39.9,34.3,38.2,
       27.3,35.9,36.0,31.3,39.3,36.2,35.0]
index_finger_ext_peak=[11.5,10.8,12.5,13.5,12.1,11.9,11.7,
       10.6,14.5,13.5,10.2,13.3,10.1,11.4]
middle_finger_ext_peak=[9.9,8.9,13.6,15.2,13.7,15.0,15.0,
       12.9,14.4,15.2,16.0,16.4,13.9,17.2]
ring_finger_ext_peak=[8.5,4.6,10.9,12.6,11.0,8.8,13.2,
       9.6,11.8,11.7,10.1,14.4,7.4,10.8]
pinky_finger_ext_peak=[7.2,7.6,10.9,11.6,9.6,9.9,12.8,
       10.9,9.6,8.5,9.0,13.7,10.0,8.6]
radial_deviation_peak=[64.7,26.8,53.9,42.7,65.3,44.1,56.8,
       66.2,39.2,51.0,40.8,63.8,44.1,40.3]

all_finger_mid_peak=[130.8,123.1,172.4,111.1,206.8,135.8,128.3,
       164.0,145.8,156.1,176.6,173.1,152.3,106.3]
index_finger_mid_peak=[50.6,43.3,58.5,66.2,62.2,62.7,54.8,
       56.9,62.6,69.8,64.8,58.2,52.6,45.6]
middle_finger_mid_peak=[58.3,56.9,64.5,73.1,78.8,52.1,50.7,
       63.3,68.1,62.1,76.0,61.2,63.3,38.5]
ring_finger_mid_peak=[41.5,28.0,31.9,64.8,44.8,44.1,53.8,
       60.4,19.5,36.3,67.2,50.4,43.8,41.5]
pinky_finger_mid_peak=[34.3,21.2,24.8,47.1,41.9,26.3,38.2,
       38.1,31.3,44.2,53.3,38.0,30.0,39.5]

x_val=[all_finger_tip_peak,index_finger_tip_peak,middle_finger_tip_peak,ring_finger_tip_peak,pinky_finger_tip_peak,ulnar_deviation_peak,
       all_finger_ext_peak,index_finger_ext_peak,middle_finger_ext_peak,ring_finger_ext_peak,pinky_finger_ext_peak,radial_deviation_peak,
       all_finger_mid_peak,index_finger_mid_peak,middle_finger_mid_peak,ring_finger_mid_peak,pinky_finger_mid_peak]

x_val_list=["all_finger_tip_peak","index_finger_tip_peak","middle_finger_tip_peak","ring_finger_tip_peak","pinky_finger_tip_peak","ulnar_deviation_peak",
       "all_finger_ext_peak","index_finger_ext_peak","middle_finger_ext_peak","ring_finger_ext_peak","pinky_finger_ext_peak","radial_deviation_peak",
       "all_finger_mid_peak","index_finger_mid_peak","middle_finger_mid_peak","ring_finger_mid_peak","pinky_finger_mid_peak"]

#cor_vals=[[],[],[]],[]
mod = LinearRegression()

x_val_array=[np.array(sublist) for sublist in x_val]

for i in range(0,len(y_val)):
    for j in range(0,len(x_val)):
        correlation = stats.pearsonr(x_val[j], y_val[i])[0]
        #cor_vals[i].append(round(correlation,2))
        
        
        #print (x_val_list[j]+" and " + y_val_list[i]+" correlation: "+str(round(correlation,2)))
        x_val_array[j]=x_val_array[j].reshape(-1,1)
        
        mod.fit(x_val_array[j], y_val[i])
        
        plt.close()
        plt.scatter(x_val[j],y_val[i])
        x_curve = np.linspace(min(x_val[j])-5, max(x_val[j])+5, 30)
        y_curve = mod.predict(x_curve.reshape(-1,1))
        plt.plot(x_curve, y_curve, c='darkorange')

        b = mod.intercept_
        m = mod.coef_[0]
        equation = f'y = {m:.2f}x + {b:.2f}'
        plt.text(max(x_val[j]) - 5, max(y_val[i]) -10 , equation, fontsize=10, color='blue')
        
        plt.title(x_val_list[j]+" and " + y_val_list[i]+" correlation: "+str(round(correlation,2)))
        plt.xlabel(x_val_list[j])
        plt.ylabel(y_val_list[i])
        plt.xlim([min(x_val[j])-5,max(x_val[j])+5])
        
        plt.show()
        






