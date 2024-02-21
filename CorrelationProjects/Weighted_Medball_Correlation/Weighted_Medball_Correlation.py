# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 16:40:36 2023

@author: bennett stice
"""

import scipy.stats as stats
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np



Names = ["Walsh","McQuiston","Stice","Salazar","Jungers","Brown","Buschschulte",
       "Darin","Council","Rakers","Subbert","Newell","James","Jackson","Rodgers","Coleman",
       "Gregory", "Kroeger","Camfield","Schmidt","Miller","Young","Downing","Arras","Prywitch",
       "Barnard","Louck","Leingang","Howshaw","Reinhardt", "Kroeger_1","Camfield_1", "Schmidt_1",
       "Young_1","Arras_1","Prywitch_1","Downing_1","Reinhardt_1"]

######################## DEPENDENT VALUES ###########################

AVG_VELO=[87,80,84.5,88,85,85,89,85.5,82,81,85.5,89,89,88,84,79,89,89,90,87.5,87,87.5,87,85,
          85,85,83,83,82.5,82,87,88,87,86,85,85,85,81]
PEAK_VELO=[91,84,87,90,88,88,93,88,86,84,89,92,92,92,87,83,94,94,93,92,92,91,91,90,
           89,87,87,86,86,85,93,92,91,90,90,89,88,83]

Y_VALS = [AVG_VELO,PEAK_VELO]
Y_VALS_LIST = ["Average Throwing Velocity", "Peak Throwing Velocity"]

####################### INDEPENDENT VALUES ##########################

OH_AVG = [36,33.5,32,37,37,35.5,36,34,37,36,38,40.5,41,35,36,37,39,39.5,39,38,40,38.5,40,36,38,35,39,38,37,34,39
          ,38,42,37,37,39,38,35]
OH_PEAK = [36,35,33,39,40,36,38,35,40,39,39,44,43,37,37,40,41,41,40,40,42,41,42,37,40,36,39,40,40,34,41
           ,40,43,39,38,40,39,37]

ROCKER_AVG = [38.5,36,36,44,39,39,42,38,39,44,38,43,43,41,39,39,43,43,42,43,46,44,42,38,41,43,44,44,39,32.5,43
              ,42,47,41.5,42,43,40,37]
ROCKER_PEAK = [41,40,40,50,42,41,45,40,42,46,41,45,46,43,42,42,45,44,43,46,48,46,43,40,42,44,44,45,42,33,45
               ,44,48,44,45,44,42,38]

LEG_LIFT_AVG = [38,37,39,47,41,39,44,40,40,44,40,46,44,44,41,40,46,43,42.5,45,48,46,39,41,43,44,45,44,40,38,44
                ,43,48,45,44,44,39,37]
LEG_LIFT_PEAK = [41,42,41,52,44,41,46,43,41,46,42,48,46,47,44,41,47,44,45,46,50,50,42,43,44,46,45,46,41,38,45
                 ,45,50,47,46,47,41,39]

X_VALS = [OH_AVG,OH_PEAK,ROCKER_AVG,ROCKER_PEAK,LEG_LIFT_AVG,LEG_LIFT_PEAK]
X_VALS_LIST = ["Overhead Average Velocity", "Overhead Peak Velocity",
               "Rocker Average Velocity", "Rocker Peak Velocity",
               "Leg Lift Average Velocity", "Leg Lift Peak Velocity"]

LR_mod = LinearRegression()

X_VALS_ARRAY=[np.array(sublist) for sublist in X_VALS]

for i in range(0,len(Y_VALS)):
    for j in range(0,len(X_VALS)):
        correlation = stats.pearsonr(X_VALS[j], Y_VALS[i])[0]
        
        
        X_VALS_ARRAY[j]=X_VALS_ARRAY[j].reshape(-1,1)
        
        LR_mod.fit(X_VALS_ARRAY[j], Y_VALS[i])
        
        plt.close()
        plt.scatter(X_VALS[j],Y_VALS[i])
        
        x_curve = np.linspace(min(X_VALS[j])-5, max(X_VALS[j])+5, 30)
        y_curve = LR_mod.predict(x_curve.reshape(-1,1))
        plt.plot(x_curve, y_curve, c='darkorange')

        b = LR_mod.intercept_
        m = LR_mod.coef_[0]
        equation = f'y = {m:.2f}x + {b:.2f}'
        plt.text(max(X_VALS[j]) - 5, max(Y_VALS[i]) -10 , equation, fontsize=10, color='blue')
        
        plt.title(X_VALS_LIST[j]+" and " + Y_VALS_LIST[i]+" correlation: "+str(round(correlation,2)))
        plt.xlabel(X_VALS_LIST[j])
        plt.ylabel(Y_VALS_LIST[i])
        plt.ylim(min(Y_VALS[i])-5,max(Y_VALS[i])+5)
        plt.xlim([min(X_VALS[j])-5,max(X_VALS[j])+5])
        plt.legend()
        
        plt.show()

