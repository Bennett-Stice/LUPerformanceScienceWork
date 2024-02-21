# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 23:53:14 2023

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

rawData = statcast(start_dt="2023-9-02", end_dt="2023-11-02")
rawData = rawData[["p_throws","pitch_type","pfx_x","pfx_z","events","description","release_speed","release_pos_x","release_pos_y","release_pos_z","release_spin_rate","plate_x","plate_z"]]
rawData=rawData[rawData["pitch_type"].str.contains('FF|CH|SL|CU', na=False)]

np.random.seed(1)
df1 = rawData.sample(10000) 

#NAN checks in data
df1 = df1[pd.notna(df1['release_speed'])]
df1 = df1[pd.notna(df1['release_spin_rate'])]
df1 = df1[pd.notna(df1['pfx_x'])]
df1 = df1[pd.notna(df1['pfx_z'])]
df1= df1[pd.notna(df1['release_pos_x'])]
df1= df1[pd.notna(df1['release_pos_y'])]
df1= df1[pd.notna(df1['release_spin_rate'])]
df1= df1[pd.notna(df1['pitch_type'])]
df1= df1[pd.notna(df1['plate_x'])]
df1= df1[pd.notna(df1['plate_z'])]

#creates target variable coloumn
df1['eventordescrip']=df1['description']
for i in range (0, len(df1.description)):
    if(df1.description.iloc[i]=="hit_into_play"):
        df1.eventordescrip.iloc[i]=df1.events.iloc[i]

        
#create good/bad col
all_outcomes = ['blocked_ball' 'ball' 'called_strike' 'foul' 'swinging_strike'
 'field_out' 'force_out' 'single' 'double' 'home_run'
 'swinging_strike_blocked' 'sac_bunt' 'grounded_into_double_play'
 'foul_tip' 'field_error' 'hit_by_pitch' 'foul_bunt' 'triple'
 'fielders_choice' 'sac_fly' 'double_play' 'fielders_choice_out'
 'missed_bunt' 'bunt_foul_tip']

bad_outcome = ["single","double","triple","home_run","ball","hit_by_pitch","hit_by_pitch"]
good_outcome = ["swinging_strike","called_strike","double_play","field_out","grounded_into_double_play","force_out",
                "swinging_strike_blocked","fielders_choice_out","missed_bunt","sac_fly"]

## try turning swinging stikes into the only good

################# Adjusting location and movement parameters
for i in range (0,len(df1.plate_x)):
    df1.plate_x.iloc[i]=df1.plate_x.iloc[i]*12
for i in range (0,len(df1.plate_z)):
    df1.plate_z.iloc[i]=df1.plate_z.iloc[i]*12
    
for i in range (0,len(df1.pfx_x)):
    df1.pfx_x.iloc[i]=df1.pfx_x.iloc[i]*12
for i in range (0,len(df1.pfx_z)):
    df1.pfx_z.iloc[i]=df1.pfx_z.iloc[i]*12
    
for i in range (0,len(df1.release_pos_x)):
    df1.release_pos_x.iloc[i]=df1.release_pos_x.iloc[i]*12
for i in range (0,len(df1.release_pos_z)):
    df1.release_pos_z.iloc[i]=df1.release_pos_z.iloc[i]*12
    
for i in range (0,len(df1.pfx_x)):
    if (df1.p_throws.iloc[i]=="L"):
        df1.pfx_x.iloc[i]=df1.pfx_x.iloc[i]*-1
        df1.release_pos_x.iloc[i]=df1.release_pos_x.iloc[i]*-1

#seperates numeric, catagorical, and response coloumns
X_num = df1[["pfx_x","pfx_z","release_speed","release_pos_x","release_pos_y","release_spin_rate","plate_x","plate_z"]].values
X_cat = df1["pitch_type"].values

#### flip release_pos_x and pfx_x by pitcher handeness 
#### may look into batter handeness

############## Cut up values based on pitch type ##################

X_FB=[]
y_FB=[]

X_CH=[]
y_CH=[]

X_SL=[]
y_SL=[]

X_CU=[]
y_CU=[]


for i in range (0, len(df1.eventordescrip)):
    if X_cat[i]=='FF':
        if df1.eventordescrip.iloc[i] in bad_outcome:
            y_FB.append(0.0)
            X_FB.append(X_num[i])
        
        elif df1.eventordescrip.iloc[i] in good_outcome:
            y_FB.append(1.0)
            X_FB.append(X_num[i])
    
    elif X_cat[i]=='CH':
        if df1.eventordescrip.iloc[i] in bad_outcome:
            y_CH.append(0.0)
            X_CH.append(X_num[i])
        
        elif df1.eventordescrip.iloc[i] in good_outcome:
            y_CH.append(1.0)
            X_CH.append(X_num[i])
            
    elif X_cat[i]=='SL':
        if df1.eventordescrip.iloc[i] in bad_outcome:
            y_SL.append(0.0)
            X_SL.append(X_num[i])
        
        elif df1.eventordescrip.iloc[i] in good_outcome:
            y_SL.append(1.0)
            X_SL.append(X_num[i])
            
    elif X_cat[i]=='CU':
        if df1.eventordescrip.iloc[i] in bad_outcome:
            y_CU.append(0.0)
            X_CU.append(X_num[i])
        
        elif df1.eventordescrip.iloc[i] in good_outcome:
            y_CU.append(1.0)
            X_CU.append(X_num[i])
            
#################### Train Test Splits ###################

X_FB_train, X_FB_val, y_FB_train, y_FB_val = train_test_split(X_FB, y_FB, test_size=0.2, random_state=1)
X_CH_train, X_CH_val, y_CH_train, y_CH_val = train_test_split(X_CH, y_CH, test_size=0.2, random_state=1)
X_SL_train, X_SL_val, y_SL_train, y_SL_val = train_test_split(X_SL, y_SL, test_size=0.2, random_state=1)
X_CU_train, X_CU_val, y_CU_train, y_CU_val = train_test_split(X_CU, y_CU, test_size=0.2, random_state=1)


################### Scale Data #####################

#gen_scaler = StandardScaler()

## maybe not normally distributed

FB_scaler= StandardScaler()
CH_scaler= StandardScaler()
SL_scaler= StandardScaler()
CU_scaler= StandardScaler()

X_FB_train_sca = FB_scaler.fit_transform(X_FB_train)
X_CH_train_sca = CH_scaler.fit_transform(X_CH_train)
X_SL_train_sca = SL_scaler.fit_transform(X_SL_train)
X_CU_train_sca = CU_scaler.fit_transform(X_CU_train)

X_FB_val_sca = FB_scaler.fit_transform(X_FB_val)
X_CH_val_sca = CH_scaler.fit_transform(X_CH_val)
X_SL_val_sca = SL_scaler.fit_transform(X_SL_val)
X_CU_val_sca = CU_scaler.fit_transform(X_CU_val)

joblib.dump(FB_scaler,'FB_scaler.save')
joblib.dump(CH_scaler,'CH_scaler.save')
joblib.dump(SL_scaler,'SL_scaler.save')
joblib.dump(CU_scaler,'CU_scaler.save')

################ Decision Tree #################

depth_list = range(1,10)
np.random.seed(1)


FB_va_acc = []
for d in depth_list:
    temp_mod = DecisionTreeClassifier(max_depth=d)
    temp_mod.fit(X_FB_train_sca, y_FB_train)
    FB_va_acc.append(temp_mod.score(X_FB_val_sca, y_FB_val))
    
idx = np.argmax(FB_va_acc)
best_d = depth_list[idx]
d_tree_FB = DecisionTreeClassifier(max_depth=best_d)
d_tree_FB.fit(X_FB_train_sca,y_FB_train)
print('Training Accuracy Fastball Decision Tree:  ', d_tree_FB.score(X_FB_val_sca, y_FB_val))

CH_va_acc = []
for d in depth_list:
    temp_mod = DecisionTreeClassifier(max_depth=d)
    temp_mod.fit(X_CH_train_sca, y_CH_train)
    CH_va_acc.append(temp_mod.score(X_CH_val_sca, y_CH_val))
    
idx = np.argmax(CH_va_acc)
best_d = depth_list[idx]
d_tree_CH = DecisionTreeClassifier(max_depth=best_d)
d_tree_CH.fit(X_CH_train_sca,y_CH_train)
print('Training Accuracy ChangeUP Decision Tree:  ', d_tree_CH.score(X_CH_val_sca, y_CH_val))

SL_va_acc = []
for d in depth_list:
    temp_mod = DecisionTreeClassifier(max_depth=d)
    temp_mod.fit(X_SL_train_sca, y_SL_train)
    SL_va_acc.append(temp_mod.score(X_SL_val_sca, y_SL_val))
    
idx = np.argmax(SL_va_acc)
best_d = depth_list[idx]
d_tree_SL = DecisionTreeClassifier(max_depth=best_d)
d_tree_SL.fit(X_SL_train_sca,y_SL_train)
print('Training Accuracy Slider Decision Tree:  ', d_tree_SL.score(X_SL_val_sca, y_SL_val))

CU_va_acc = []
for d in depth_list:
    temp_mod = DecisionTreeClassifier(max_depth=d)
    temp_mod.fit(X_CU_train_sca, y_CU_train)
    CU_va_acc.append(temp_mod.score(X_CU_val_sca, y_CU_val))
    
idx = np.argmax(CU_va_acc)
best_d = depth_list[idx]
d_tree_CU = DecisionTreeClassifier(max_depth=best_d)
d_tree_CU.fit(X_CU_train_sca,y_CU_train)
print('Training Accuracy Curveball Decision Tree:  ', d_tree_CU.score(X_CU_val_sca, y_CU_val))
print('')

############ KNN ############

param_grid = [{'n_neighbors': range(15,20), 'p': [1,2]}]

knn_FB = KNeighborsClassifier()
gscv_02 = GridSearchCV(knn_FB, param_grid, cv=5, scoring='accuracy',  refit=True)
gscv_02.fit(X_FB_train_sca, y_FB_train)
knn_FB = gscv_02.best_estimator_
print('Training Score Fastball KNearest Neighbors:', knn_FB.score(X_FB_val_sca, y_FB_val))

knn_CH = KNeighborsClassifier()
gscv_02 = GridSearchCV(knn_CH, param_grid, cv=5, scoring='accuracy',  refit=True)
gscv_02.fit(X_CH_train_sca, y_CH_train)
knn_CH = gscv_02.best_estimator_
print('Training Score ChangeUP KNearest Neighbors:', knn_CH.score(X_CH_val_sca, y_CH_val))

knn_SL = KNeighborsClassifier()
gscv_02 = GridSearchCV(knn_SL, param_grid, cv=5, scoring='accuracy',  refit=True)
gscv_02.fit(X_SL_train_sca, y_SL_train)
knn_SL = gscv_02.best_estimator_
print('Training Score Slider KNearest Neighbors:', knn_SL.score(X_SL_val_sca, y_SL_val))

knn_CU = KNeighborsClassifier()
gscv_02 = GridSearchCV(knn_CU, param_grid, cv=5, scoring='accuracy',  refit=True)
gscv_02.fit(X_CU_train_sca, y_CU_train)
knn_CU = gscv_02.best_estimator_
print('Training Score Curveball KNearest Neighbors:', knn_CU.score(X_CU_val_sca, y_CU_val))
print('')

############### Random Forest ##############

param_grid = [{'n_estimators':np.arange(100,500,100), 'max_depth':range(2,15)}]

forest_FB = RandomForestClassifier()
gscv_04 = GridSearchCV(forest_FB, param_grid, cv=5, scoring='accuracy',  refit=True)
gscv_04.fit(X_FB_train_sca, y_FB_train)
forest_FB = gscv_04.best_estimator_
print('Training Score Fastball Random Forest:', forest_FB.score(X_FB_val_sca, y_FB_val))

forest_CH = RandomForestClassifier()
gscv_04 = GridSearchCV(forest_CH, param_grid, cv=5, scoring='accuracy',  refit=True)
gscv_04.fit(X_CH_train_sca, y_CH_train)
forest_CH = gscv_04.best_estimator_
print('Training Score ChangeUP Random Forest:', forest_CH.score(X_CH_val_sca, y_CH_val))

forest_SL = RandomForestClassifier()
gscv_04 = GridSearchCV(forest_SL, param_grid, cv=5, scoring='accuracy',  refit=True)
gscv_04.fit(X_SL_train_sca, y_SL_train)
forest_SL = gscv_04.best_estimator_
print('Training Score Slider Random Forest:', forest_SL.score(X_SL_val_sca, y_SL_val))

forest_CU = RandomForestClassifier()
gscv_04 = GridSearchCV(forest_CU, param_grid, cv=5, scoring='accuracy',  refit=True)
gscv_04.fit(X_CU_train_sca, y_CU_train)
forest_CU = gscv_04.best_estimator_
print('Training Score Curveball Random Forest:', forest_CU.score(X_CU_val_sca, y_CU_val))
print('')

################### Voting Classifier ################# 

VoteClass_FB = VotingClassifier(
    estimators = [('tree', d_tree_FB),('knn', knn_FB),('rf',forest_FB)], voting = 'soft')
VoteClass_FB.fit(X_FB_train_sca, y_FB_train)
print('Training Accuracy Fastball Voting Classifier:  ', VoteClass_FB.score(X_FB_val_sca, y_FB_val))

VoteClass_CH = VotingClassifier(
    estimators = [('tree', d_tree_CH),('knn', knn_CH),('rf',forest_CH)], voting = 'soft')
VoteClass_CH.fit(X_CH_train_sca, y_CH_train)
print('Training Accuracy ChangeUP Voting Classifier:  ', VoteClass_CH.score(X_CH_val_sca, y_CH_val))

VoteClass_SL = VotingClassifier(
    estimators = [('tree', d_tree_SL),('knn', knn_SL),('rf',forest_SL)], voting = 'soft')
VoteClass_SL.fit(X_SL_train_sca, y_SL_train)
print('Training Accuracy Slider Voting Classifier:  ', VoteClass_SL.score(X_SL_val_sca, y_SL_val))

VoteClass_CU = VotingClassifier(
    estimators = [('tree', d_tree_CU),('knn', knn_CU),('rf',forest_CU)], voting = 'soft')
VoteClass_CU.fit(X_CU_train_sca, y_CU_train)
print('Training Accuracy Curveball Voting Classifier:  ', VoteClass_CU.score(X_CU_val_sca, y_CU_val))
print('')


################ Pickle Files ####################
import pickle

filename='Prediction_Model_VotingClassifier_FB.pkl'
pickle.dump(VoteClass_FB,open(filename,'wb'))
loaded_model=pickle.load(open(filename,'rb'))

filename='Prediction_Model_VotingClassifier_CH.pkl'
pickle.dump(VoteClass_CH,open(filename,'wb'))
loaded_model=pickle.load(open(filename,'rb'))

filename='Prediction_Model_VotingClassifier_SL.pkl'
pickle.dump(VoteClass_SL,open(filename,'wb'))
loaded_model=pickle.load(open(filename,'rb'))

filename='Prediction_Model_VotingClassifier_CU.pkl'
pickle.dump(VoteClass_CU,open(filename,'wb'))
loaded_model=pickle.load(open(filename,'rb'))

print("done")
            
   