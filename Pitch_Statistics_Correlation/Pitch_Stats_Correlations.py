# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 09:20:28 2024

@author: Bennett Stice
"""
import psycopg2
import scipy.stats as stats
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np


def get_FB_percentage (cursora):
    query = "SELECT CASE WHEN COUNT(CASE WHEN pitch_type = 'FB' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'FB' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END "
    query += "FROM pitch_log_t GROUP BY fname,lname ORDER BY fname,lname ASC"
    
    cursora.execute(query)
    data=cursora.fetchall()
    FB_Percentage=[]
    
    for row in data:
        FB_Percentage.append(round(row[0]))
    
    return FB_Percentage
        
def get_CB_percentage (cursora):
    query = "SELECT CASE WHEN COUNT(CASE WHEN pitch_type = 'CB' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'CB' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END "
    query += "FROM pitch_log_t GROUP BY fname,lname ORDER BY fname,lname ASC"
    
    cursora.execute(query)
    data=cursora.fetchall()
    CB_Percentage=[]
    
    for row in data:
        CB_Percentage.append(round(row[0]))
        
    return CB_Percentage

def get_SL_percentage (cursora):
    query = "SELECT CASE WHEN COUNT(CASE WHEN pitch_type = 'SL' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'SL' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END "
    query += "FROM pitch_log_t GROUP BY fname,lname ORDER BY fname,lname ASC"
    
    cursora.execute(query)
    data=cursora.fetchall()
    SL_Percentage=[]
    
    for row in data:
        SL_Percentage.append(round(row[0]))
        
    return SL_Percentage

def get_CH_percentage (cursora):
    query = "SELECT CASE WHEN COUNT(CASE WHEN pitch_type = 'CH' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'CH' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END "
    query += "FROM pitch_log_t GROUP BY fname,lname ORDER BY fname,lname ASC"
    
    cursora.execute(query)
    data=cursora.fetchall()
    CH_Percentage=[]
    
    for row in data:
        CH_Percentage.append(round(row[0]))
        
    return CH_Percentage

def get_SP_percentage (cursora):
    query = "SELECT CASE WHEN COUNT(CASE WHEN pitch_type = 'SP' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'SP' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END "
    query += "FROM pitch_log_t GROUP BY fname,lname ORDER BY fname,lname ASC"
    
    cursora.execute(query)
    data=cursora.fetchall()
    SP_Percentage=[]
    
    for row in data:
        SP_Percentage.append(round(row[0]))
        
    return SP_Percentage
        
def get_CU_percentage (cursora):
    query = "SELECT CASE WHEN COUNT(CASE WHEN pitch_type = 'CU' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'CU' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END "
    query += "FROM pitch_log_t GROUP BY fname,lname ORDER BY fname,lname ASC"
    
    cursora.execute(query)
    data=cursora.fetchall()
    CU_Percentage=[]
    
    for row in data:
        CU_Percentage.append(round(row[0]))
        
    return CU_Percentage  

def get_advantage_counts_percentage(cursora):
    ##### Percentage of Pitches Thrown in Advantage Counts
    query = "SELECT CASE WHEN COUNT(CASE WHEN pitch_result <>'0' THEN 1 END) > 0 "
    query+= "THEN (COUNT(CASE WHEN strikes>balls THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS PTIAC FROM pitch_log_t "
    query+= "GROUP BY fname,lname ORDER BY fname,lname ASC"
    cursora.execute(query)
    data=cursora.fetchall()
    
    Advantage_Count_Percentage=[]
      
    for row in data:
        Advantage_Count_Percentage.append(round(row[0]))
        
    return Advantage_Count_Percentage 
        
def get_disadvantage_counts_percentage(cursora):
    ##### Percentage of Pitches Thrown in DisAdvantage Counts
    query = "SELECT CASE WHEN COUNT(CASE WHEN pitch_result <>'0' THEN 1 END) > 0 "
    query+= "THEN (COUNT(CASE WHEN strikes<balls THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS PTIDC FROM pitch_log_t "
    query+= "GROUP BY fname,lname ORDER BY fname,lname ASC"
    cursora.execute(query)
    data=cursora.fetchall()
    
    Disadvantage_Count_Percentage=[]
      
    for row in data:
        Disadvantage_Count_Percentage.append(round(row[0]))
        
    return Disadvantage_Count_Percentage 

def get_strikeout_percentage(cursora):
    ##### Strikeout Percentage
    query = "SELECT CASE WHEN COUNT(CASE WHEN ab_result <> '0' THEN 1 END) >0"
    query += " THEN (COUNT(CASE WHEN strikes = 2 AND (pitch_result = 'SL' or pitch_result = 'SS' or pitch_result = 'SSC' or pitch_result = 'D3SS') THEN 1 END) * 100 /" 
    query += " COUNT(CASE WHEN ab_result <> '0' THEN 1 END)) ELSE 0 END AS KPer FROM pitch_log_t "
    query+= "GROUP BY fname,lname ORDER BY fname,lname ASC"
    cursora.execute(query)
    data=cursora.fetchall()
    
    Strikeout_Percentage=[]
      
    for row in data:
        Strikeout_Percentage.append(round(row[0]))
        
    return Strikeout_Percentage 
        
def get_ground_ball_out_percentage(cursora):
    ##### Ground Ball Out Percentage
    query = "SELECT CASE WHEN COUNT(CASE WHEN pitch_result = 'BIP' THEN 1 END) >0"
    query += " THEN (COUNT(CASE WHEN bip_result = 'GO' OR bip_result = 'DP' THEN 1 END) * 100 /"
    query += " COUNT(CASE WHEN pitch_result = 'BIP' THEN 1 END)) ELSE 0 END AS GBOPer FROM pitch_log_t "
    query+= "GROUP BY fname,lname ORDER BY fname,lname ASC"
    cursora.execute(query)
    data=cursora.fetchall()
    
    Groundout_Percentage=[]
      
    for row in data:
        Groundout_Percentage.append(round(row[0]))
        
    return Groundout_Percentage
        
def get_fly_ball_out_percentage(cursora):
    ##### Fly Ball Out Percentage
    query = "SELECT CASE WHEN COUNT(CASE WHEN pitch_result = 'BIP' THEN 1 END) >0"
    query += " THEN (COUNT(CASE WHEN bip_result = 'FO' THEN 1 END) * 100 /" 
    query += " COUNT(CASE WHEN pitch_result = 'BIP' THEN 1 END)) ELSE 0 END AS FBOPer FROM pitch_log_t "
    query+= "GROUP BY fname,lname ORDER BY fname,lname ASC"
    cursora.execute(query)
    data=cursora.fetchall()
    
    Flyballout_Percentage=[]
      
    for row in data:
        Flyballout_Percentage.append(round(row[0]))
        
    return Flyballout_Percentage

def get_baa_bip(cursora):
    ##### Oppenent Batting Average on Balls in Play
    query = "SELECT COUNT(CASE WHEN pitch_result = 'BIP' THEN 1 END) AS BIP, "
    query+="COUNT(CASE WHEN ab_result = 'safe' AND pitch_result = 'BIP' THEN 1 END) AS BIPSAFE FROM pitch_log_t "
    query+= "GROUP BY fname,lname ORDER BY fname,lname ASC"
    cursora.execute(query)
    data=cursora.fetchall()
    
    BAA_BIP=[]
      
    for row in data:
        bip,bipsafe=row
        if (bip!=0):    
            BAA_BIP.append(round(bipsafe*1.0/bip,3))
        else:
            BAA_BIP.append(0.0)
        
    return BAA_BIP

def get_opponent_slugging_percentage(cursora):
    query = "SELECT  COUNT(CASE WHEN bip_result='1B' THEN 1 END) AS Singles , "
    query += "COUNT(CASE WHEN bip_result='2B' THEN 1 END) AS Doubles, "
    query += "COUNT(CASE WHEN bip_result='3B' THEN 1 END) AS Triples, "
    query += "COUNT(CASE WHEN bip_result='HR' THEN 1 END) AS Homeruns, "
    query += "COUNT(CASE WHEN ab_result<>'0' AND pitch_result NOT IN ('B','HBP') THEN 1 END) AS At_Bats "
    query += "FROM pitch_log_T "
    query+= "GROUP BY fname,lname ORDER BY fname,lname ASC"
    cursora.execute(query)
    data=cursora.fetchall()
    
    Opp_SLG_Percentage=[]
      
    for row in data:
        Sing,Doub,Trip,HR,AB=row
        if (AB!=0):    
            Opp_SLG_Percentage.append(round((Sing+(Doub*2)+(Trip*3)+(HR*4))/AB,3))
        else:
            Opp_SLG_Percentage.append(0.0)
        
    return Opp_SLG_Percentage

def get_chases_percentage(cursora):
    ##### Chases
    query = "SELECT COUNT(CASE WHEN pitch_result IN ('SSC','D3SS') THEN 1 END) AS chases, "
    query += "COUNT(CASE WHEN pitch_id<>'0' THEN 1 END) "
    query += "FROM pitch_log_T "
    query += "GROUP BY fname, lname ORDER BY fname, lname"
    
    cursora.execute(query)
    data=cursora.fetchall()
    
    Chases_Percentage=[]
    for row in data:
        chases,pitches = row
        if (pitches!=0):
            Chases_Percentage.append(round(chases*100.0/pitches))
        else:
            Chases_Percentage.append(0)
    
    return Chases_Percentage

def get_ahead_after_3_pitches_percentage(cursora):
    ##### Ahead After 3 Pitches Percentage
    query = "SELECT CASE WHEN COUNT(CASE WHEN (balls=1 AND strikes=2) or (balls=2 AND strikes=1) or (balls=0 AND strikes=2 AND pitch_result Not IN ('B','F')) or (balls=2 AND strikes=0 AND pitch_result IN ('B','HBP','BIP'))THEN 1 END) > 0 "
    query+="THEN (COUNT(CASE WHEN (balls=1 AND strikes=2) or (balls=0 AND strikes=2 AND pitch_result Not IN ('B','F')) THEN 1 END) * 100.0 / "
    query+="COUNT(CASE WHEN (balls=1 AND strikes=2) or (balls=2 AND strikes=1) or (balls=0 AND strikes=2 AND pitch_result Not IN ('B','F','HBP')) or (balls=2 AND strikes=0 AND pitch_result IN ('B','HBP','BIP'))THEN 1 END)) ELSE 0 END AS AA3P FROM pitch_log_t "
    query+= "GROUP BY fname,lname ORDER BY fname,lname ASC"
    cursora.execute(query)
    data=cursora.fetchall()
    
    Ahead_After_3_Percentage=[]
      
    for row in data:
        Ahead_After_3_Percentage.append(round(row[0]))
        
    return Ahead_After_3_Percentage

def get_pitches_per_inning(cursora):
    ##### Pitches Per Inning       
    query = "SELECT SUM(pitches) AS pitchCount, SUM(max_outs) AS outs FROM (SELECT MAX(pitch_count) as pitches,  "
    query += "MAX(outs_accrued) AS max_outs,fname,lname FROM pitch_log_T WHERE pitch_id <> '0' "
    query += " GROUP BY date,fname,lname) AS asdf GROUP BY fname,lname ORDER BY fname,lname"
      
    cursora.execute(query)
    data=cursora.fetchall()
    
    Pitches_Per_Inning=[]
    
    for row in data:
        pitchCount,outs=row
        if (outs!=0):
            Pitches_Per_Inning.append(round(pitchCount/(outs/3),2))
    
    return Pitches_Per_Inning
    
        
def get_peak_velo(cursora):
    ##### Peak Velocity
    query="SELECT MAX(velocity) AS velo FROM pitch_log_t "
    query+= "GROUP BY fname,lname ORDER BY fname,lname ASC"
    cursora.execute(query)
    data=cursora.fetchall()
    
    Peak_Velo=[]
      
    for row in data:
        Peak_Velo.append(row[0])
        
    return Peak_Velo

def get_average_fastball_velo(cursora):
    ##### Average Fastball Velocity
    query="SELECT AVG(velocity) AS velo FROM pitch_log_t "
    query+="WHERE pitch_type = 'FB' "
    query+= "GROUP BY fname,lname ORDER BY fname,lname ASC"
    cursora.execute(query)
    data=cursora.fetchall()
    
    Average_Velo=[]
      
    for row in data:
        Average_Velo.append(round(row[0]))
        
    return Average_Velo
  
def get_1st_pitch_strike_percentage(cursora):
    ##### 1st Pitch Strike Percentage
    query="SELECT CASE WHEN COUNT(CASE WHEN balls = 0 AND strikes = 0 THEN 1 END) > 0 "
    query+="THEN (COUNT(CASE WHEN balls = 0 AND strikes = 0 AND pitch_result <> 'B' AND pitch_result <> 'HBP' THEN 1 END) * 100.0 / "
    query+="COUNT(CASE WHEN balls = 0 AND strikes = 0 THEN 1 END)) ELSE 0 END AS Percentage FROM pitch_log_t "
    query+= "GROUP BY fname,lname ORDER BY fname,lname ASC"
    cursora.execute(query)
    data=cursora.fetchall()
    
    First_Pitch_Strike_Percentage=[]
      
    for row in data:
        First_Pitch_Strike_Percentage.append(round(row[0]))
        
    return First_Pitch_Strike_Percentage
            
def get_off_speed_strike_percentage(cursora):
    ##### Off-Speed Strike Percentage
    query="SELECT CASE WHEN COUNT(CASE WHEN pitch_type <> 'FB' and pitch_type <> 'CU' THEN 1 END) > 0 "
    query+="THEN (COUNT(CASE WHEN pitch_type <> 'FB' AND pitch_type <> 'CU' AND pitch_result <> 'B' AND pitch_result <> 'HBP' THEN 1 END) * 100.0 / "
    query+="COUNT(CASE WHEN pitch_type <> 'FB' and pitch_type <> 'CU' THEN 1 END)) ELSE 0 END AS PercentageOFF FROM pitch_log_t "
    query+= "GROUP BY fname,lname ORDER BY fname,lname ASC"
    cursora.execute(query)
    data=cursora.fetchall()
    
    Off_Speed_Strike_Percentage=[]
      
    for row in data:
        Off_Speed_Strike_Percentage.append(round(row[0]))
        
    return Off_Speed_Strike_Percentage
            
def get_swing_and_miss_percentage(cursora):
    ##### Swing and Miss Percentage
    query ="SELECT CASE WHEN COUNT(CASE WHEN pitch_result <>'0' THEN 1 END) > 0 "
    query+="THEN (COUNT(CASE WHEN pitch_result = 'SS' or pitch_result = 'SSC' or pitch_result = 'D3SS' THEN 1 END) * 100.0 / "
    query+="COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS Misses FROM pitch_log_t "
    query+= "GROUP BY fname,lname ORDER BY fname,lname ASC"
    cursora.execute(query)
    data=cursora.fetchall()
    
    Swing_And_Miss_Percentage=[]
      
    for row in data:
        Swing_And_Miss_Percentage.append(round(row[0]))
        
    return Swing_And_Miss_Percentage

def get_overall_strike_percentage(cursora):
    ##### Overall Strike Percentage
    query="SELECT CASE WHEN COUNT(CASE WHEN pitch_result <> '0' THEN 1 END) > 0 "
    query+="THEN (COUNT(CASE WHEN pitch_result <> 'B' AND pitch_result <> 'HBP' THEN 1 END) * 100.0 / "
    query+="COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS OvePer FROM pitch_log_t "
    query+= "GROUP BY fname,lname ORDER BY fname,lname ASC"
    cursora.execute(query)
    data=cursora.fetchall()
    
    Strike_Percentage=[]
      
    for row in data:
        Strike_Percentage.append(round(row[0]))
        
    return Strike_Percentage

def get_WHIP(cursora):
    #### Walks and Hits Per Innings Pitched
    query = "SELECT "
    query += "COUNT(CASE WHEN ab_result='out' THEN 1 END) AS Outs, "
    query += "COUNT(CASE WHEN ab_result='safe' AND bip_result NOT IN ('E','HBP') THEN 1 END) AS Safes "
    query += "FROM pitch_log_T GROUP BY fname,lname ORDER BY fname,lname ASC"
    
    cursora.execute(query)
    data=cursora.fetchall()
    
    WHIP=[]
      
    for row in data:
        outs,safes=row
        if outs!=0:
            WHIP.append(round(safes/outs/3,2))
        else:
            WHIP.append(0)
        
    return WHIP

def get_baa(cursora):
    ##### Oppenent Batting Average
    query = "SELECT COUNT(CASE WHEN pitch_result<>'B' AND pitch_result<>'HBP' AND ab_result<>'0' THEN 1 END) AS AB, "
    query+="COUNT(CASE WHEN bip_result IN ('1B','2B','3B','HR')  THEN 1 END) AS SAFE FROM pitch_log_t "
    query+= "GROUP BY fname,lname ORDER BY fname,lname ASC"
    cursora.execute(query)
    data=cursora.fetchall()
    
    Batting_Average_Against=[]
      
    for row in data:
        AB,safe=row
        
        if (AB!=0):    
            Batting_Average_Against.append(round(safe*1.0/AB,3))
        else:
            Batting_Average_Against.append(0.0)
        
    return Batting_Average_Against

def get_OBP(cursora):
    ##### Oppenent On Base Percentage
    query = "SELECT COUNT(CASE WHEN ab_result<>'0' THEN 1 END) AS AB, "
    query+="COUNT(CASE WHEN ab_result='safe'  THEN 1 END) AS SAFE FROM pitch_log_t "
    query+= "GROUP BY fname,lname ORDER BY fname,lname ASC"
    cursora.execute(query)
    data=cursora.fetchall()
    
    Opponent_On_Base_Percentage=[]
      
    for row in data:
        AB,safe=row
        if (AB!=0):    
            Opponent_On_Base_Percentage.append(round(safe*1.0/AB,3))
        else:
            Opponent_On_Base_Percentage.append(0.0)
        
    return Opponent_On_Base_Percentage

def main():
    try:
        connection = psycopg2.connect(
            dbname="ps1",
            user="pythoncon",
            password="password",
            host="18.217.248.114",
            port="5432"
        )
        
        with connection.cursor() as cursora:
            
            FB_Percentage=get_FB_percentage(cursora)
            CB_Percentage=get_CB_percentage(cursora)
            SL_Percentage=get_SL_percentage(cursora)
            CH_Percentage=get_CH_percentage(cursora)
            SP_Percentage=get_SP_percentage(cursora)
            CU_Percentage=get_CU_percentage(cursora)
            Advantage_Count_Percentage=get_advantage_counts_percentage(cursora)
            Disadvantage_Count_Percentage=get_disadvantage_counts_percentage(cursora)
            Strikeout_Percentage=get_strikeout_percentage(cursora)
            Groundout_Percentage=get_ground_ball_out_percentage(cursora)
            Flyballout_Percentage=get_fly_ball_out_percentage(cursora)
            BAA_BIP=get_baa_bip(cursora)
            Opp_SLG_Percentage=get_opponent_slugging_percentage(cursora)
            Chases_Percentage=get_chases_percentage(cursora)
            Ahead_After_3_Percentage=get_ahead_after_3_pitches_percentage(cursora)
            Pitches_Per_Inning=get_pitches_per_inning(cursora)
            Peak_Velo=get_peak_velo(cursora)
            Average_Fastball_Velo=get_average_fastball_velo(cursora)
            First_Pitch_Strike_Percentage=get_1st_pitch_strike_percentage(cursora)
            Off_Speed_Strike_Percentage=get_off_speed_strike_percentage(cursora)
            Swing_And_Miss_Percentage=get_swing_and_miss_percentage(cursora)
            Strike_Percentage=get_overall_strike_percentage(cursora)
            WHIP=get_WHIP(cursora)
            Batting_Average_Against=get_baa(cursora)
            Opponent_On_Base_Percentage=get_OBP(cursora)
            
            On_Base_Plus_Slugging=[]
            for i in range(0,len(Opponent_On_Base_Percentage)):
                On_Base_Plus_Slugging.append(Opp_SLG_Percentage[i]+Opponent_On_Base_Percentage[i])
                
            
            x_val=[FB_Percentage,CB_Percentage,SL_Percentage,CH_Percentage,SP_Percentage,CU_Percentage,Advantage_Count_Percentage,
                    Disadvantage_Count_Percentage,Strikeout_Percentage,Groundout_Percentage,Flyballout_Percentage,BAA_BIP,Opp_SLG_Percentage,
                    Chases_Percentage,Ahead_After_3_Percentage,Pitches_Per_Inning,Peak_Velo,Average_Fastball_Velo,First_Pitch_Strike_Percentage,
                    Off_Speed_Strike_Percentage,Swing_And_Miss_Percentage,Strike_Percentage]
            
            x_val_list=["FB_Percentage","CB_Percentage","SL_Percentage","CH_Percentage","SP_Percentage","CU_Percentage","Advantage_Count_Percentage",
                    "Disadvantage_Count_Percentage","Strikeout_Percentage","Groundout_Percentage","Flyballout_Percentage","BAA_BIP","Opp_SLG_Percentage",
                    "Chases_Percentage","Ahead_After_3_Percentage","Pitches_Per_Inning","Peak_Velo","Average_Fastball_Velo","First_Pitch_Strike_Percentage",
                    "Off_Speed_Strike_Percentage","Swing_And_Miss_Percentage","Strike_Percentage"]
            
            y_val=[Strikeout_Percentage,Groundout_Percentage,Flyballout_Percentage,BAA_BIP,Opp_SLG_Percentage,Chases_Percentage,
                    Ahead_After_3_Percentage,Pitches_Per_Inning,Swing_And_Miss_Percentage,WHIP,Batting_Average_Against,Opponent_On_Base_Percentage,
                    On_Base_Plus_Slugging]
            
            y_val_list=["Strikeout_Percentage","Groundout_Percentage","Flyballout_Percentage","BAA_BIP","Opp_SLG_Percentage","Chases_Percentage",
                    "Ahead_After_3_Percentage","Pitches_Per_Inning","Swing_And_Miss_Percentage","WHIP","Batting_Average_Against","Opponent_On_Base_Percentage",
                    "On_Base_Plus_Slugging"]
            
            mod = LinearRegression()

            x_val_array=[np.array(sublist) for sublist in x_val]

            for i in range(0,len(y_val)):
                for j in range(0,len(x_val)):
                    if (x_val[j]!=y_val[i]):
                        correlation = stats.pearsonr(x_val[j], y_val[i])[0]
                   
                        x_val_array[j]=x_val_array[j].reshape(-1,1)
                    
                        mod.fit(x_val_array[j], y_val[i])
                    
                        plt.close()
                        plt.scatter(x_val[j],y_val[i])
                        x_curve = np.linspace(min(x_val[j]) - 0.25 * (max(x_val[j]) - min(x_val[j])), max(x_val[j]) + 0.25 * (max(x_val[j]) - min(x_val[j])), 30)
                        y_curve = mod.predict(x_curve.reshape(-1,1))
                        plt.plot(x_curve, y_curve, c='darkorange')

             #           b = mod.intercept_
              #          m = mod.coef_[0]
              #          equation = f'y = {m:.2f}x + {b:.2f}'
               #         plt.text(max(x_val[j]) - round(.25*min(x_val[j]),3), max(y_val[i]) -round(.25(y_val[i]),3) , equation, fontsize=10, color='blue')
                    
                        plt.title(x_val_list[j]+" and " + y_val_list[i]+" correlation: "+str(round(correlation,2)))
                        plt.xlabel(x_val_list[j])
                        plt.ylabel(y_val_list[i])
                        
                    
                        plt.show()
                    
            
                
        
    except psycopg2.Error as e:
        # Handle database-related exceptions here
        print(f"Database error: {e}")

    except Exception as e:
        # Handle other exceptions here
        print(f"An unexpected error occurred: {e}")

    finally:
        # This block will be executed whether an exception occurs or not
        if connection:
            connection.close()
            print("Connection closed. GO LIONS!!!!")

if __name__ == "__main__":
    main()           
    
    
    