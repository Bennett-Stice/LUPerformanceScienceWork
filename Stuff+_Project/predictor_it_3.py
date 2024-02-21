# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 12:40:21 2023

@author: bennett stice
"""

import sys
import pickle
import json
import joblib
#from pybaseball import statcast
import numpy as np

#first: pfx_x
#second: pfx_z
#third: release_speed
#fourth: release_pos_x
#fifth: release_pos_y
#sixth: release_spin_rate
#seventh: plate_x
#eigth: plate_z


def main(args):
    with open('Prediction_Model_VotingClassifier_FB.pkl', 'rb') as f:
        FB_model = pickle.load(f)
        
    with open('Prediction_Model_VotingClassifier_CH.pkl', 'rb') as f:
        CH_model = pickle.load(f)
        
    with open('Prediction_Model_VotingClassifier_SL.pkl', 'rb') as f:
        SL_model = pickle.load(f)
        
    with open('Prediction_Model_VotingClassifier_CU.pkl', 'rb') as f:
        CU_model = pickle.load(f)
        
    
    #opens json file and stores it as a dictionary in sample_load_file
    sample_load_file = json.loads(args[1])
        
    pitchtype = sample_load_file['pitchtype']
    
    vb_traj=sample_load_file['vb_trajectory']
    hb_traj=sample_load_file['hb_trajectory']
    velo=sample_load_file['velocity']
    release_side=sample_load_file['releaseside']
    release_height=sample_load_file['releaseheight']
    totalspin=sample_load_file['totalspin']
    strikezoneside=sample_load_file['strikezoneside']
    strikezoneheight=sample_load_file['strikezoneheight']
    
    
    if (release_side<0):
       release_side=release_side*-1
       vb_traj=vb_traj*-1
   
    X_input =np.array([[vb_traj,hb_traj,velo,release_side,release_height,
                        totalspin,strikezoneside,strikezoneheight]])
    
    successProb=6
    

    if pitchtype == "Fastball":
        FB_scaler=joblib.load("FB_scaler.save")
        FB_input=FB_scaler.transform(X_input)
        successProb = FB_model.predict_proba(FB_input)[0][1]
    if pitchtype == "ChangeUp":
        CH_scaler=joblib.load("CH_scaler.save")
        CH_input=CH_scaler.transform(X_input)
        successProb = CH_model.predict_proba(CH_input)[0][1]
    if pitchtype =="Slider":
        SL_scaler=joblib.load("SL_scaler.save")
        SL_input=SL_scaler.transform(X_input)
        successProb = SL_model.predict_proba(SL_input)[0][1]
    if pitchtype == "Curveball":
        CU_scaler=joblib.load("CU_scaler.save")
        CU_input=CU_scaler.transform(X_input)
        successProb = CU_model.predict_proba(CU_input)[0][1]

    
    endScore=successProb*100
    
    print(round(endScore, 2))
    
    
## convert to a z score
### zscore * 10 + 50

if __name__ == "__main__":
    main(sys.argv)
