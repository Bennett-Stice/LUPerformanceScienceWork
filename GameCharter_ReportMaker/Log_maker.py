# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 17:03:35 2023

@author: Bennett Stice
"""
import psycopg2
import openpyxl
from openpyxl.styles import Font
from openpyxl.styles import PatternFill
import os

##globals
header_pos=['A2','B2','C2','D2','E2','F2','G2','H2','I2','J2','K2','L2','M2','N2','O2','P2','Q2','R2','S2','T2','U2','V2','W2','X2']
pitch_headersa=['Date','Opponent','Pitches','Pitches Per Inning','Peak Velocity','1st Pitch % (60)','OS Strike % (50)','S/M % (25)','Velo-Range','Chases','A3P % (60)']
pitcher_headersb=['LO % (65)','Overall Strike % (60)','BAA w/ 2K (.150)','Pitches Ahead %','Pitches Behind %','Strikeout %','Ground Ball Out %','Fly Ball Out %','BAA BIP','AB Win %','Pitch Spread %','Pitch Spread Strike %', 'Pitch Spread Whiff %']
pitcher_headers=pitch_headersa+pitcher_headersb
season_game_headersa=['Name','Pitches','Pitches Per Inning','Peak Velocity','1st Pitch % (60)','OS Strike % (50)','S/M % (25)','Velo-Range','Chases','A3P % (60)']
season_game_headersb=['LO % (65)','Overall Strike % (60)','BAA w/ 2K (.150)','Pitches Ahead %','Pitches Behind %','Strikeout %','Ground Ball Out %','Fly Ball Out %','BAA BIP','AB Win %','Pitch Spread %','Pitch Spread Strike %', 'Pitch Spread Whiff %' ]
season_game_headers=season_game_headersa+season_game_headersb





def insert_header(pos,name,sheetName):
    sheetName[pos]=name
    bold_font = Font(bold=True)
    sheetName[pos].font = bold_font
    
def wipe(workbooka):
    # Delete all sheets except the active one
    all_sheets = workbooka.sheetnames

    for sheet_name in all_sheets:
        if sheet_name != 'Sheet':
            del workbooka[sheet_name]
            
def create_workbook(file_nameb):
    # Specify the path to the file
    file_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Lindenwood Performance Science", "gameCharter", file_nameb)

    # Check if the file exists
    if os.path.exists(file_path):
        # Load the existing workbook
        workbook = openpyxl.load_workbook(file_path)
    else:
        # Create a new workbook
        workbook = openpyxl.Workbook()
    
    return_list=[workbook,file_path]
    
    return return_list

def setup(sheetnameb,workbookb,A1title,B1entry,D1title,E1entry,G1title,H1entry,pos,head):
    # Create a new sheet and set it as the active sheet
    new_sheetc = workbookb.create_sheet(sheetnameb)
    workbookb.active = new_sheetc

    new_sheetc['A1']=A1title
    new_sheetc['B1']=B1entry
    bold_font = Font(bold=True)
    new_sheetc['A1'].font = bold_font
    
    new_sheetc['D1']=D1title
    new_sheetc['E1']=E1entry
    new_sheetc['D1'].font = bold_font
    
    new_sheetc['G1']=G1title
    new_sheetc['H1']=H1entry
    new_sheetc['G1'].font = bold_font
    
    for l in range(0,len(head)):
        insert_header(pos[l],head[l],new_sheetc)
        
    return new_sheetc

def bold_first_column_if_threshold(sheet, threshold):
    for row in range(3, sheet.max_row + 1):
        bold_count = sum(1 for col in sheet.iter_cols(min_row=row, max_row=row) for cell in col if cell.font and cell.font.bold)
        
        if bold_count >= threshold:
            sheet.cell(row=row, column=1).font = Font(bold=True)

def adjust_formating(new_sheetd,row_i):
     
    # Shade cells in the row that have values
    for col_num in range(1, new_sheetd.max_column + 1):
        cell_value = new_sheetd.cell(row=row_i, column=col_num).value
        if cell_value is not None:
            new_sheetd.cell(row=row_i, column=col_num).fill = PatternFill(start_color="808080", end_color="808080", fill_type="solid")
        
    # Adjust column width to fit the widest text entry
    for column in new_sheetd.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
            adjusted_width = (max_length + 1)
            new_sheetd.column_dimensions[column[0].column_letter].width = adjusted_width

    # Center all text in the cells
    for row in new_sheetd.iter_rows():
        for cell in row:
            cell.alignment = openpyxl.styles.Alignment(horizontal='center', vertical='center')
            
def savebook(workbookc,file_pathb,endMessage):
    # Close the workbook before saving
    workbookc.close()
   
    # Save the workbook
    workbookc.save(file_pathb)
    
    print(endMessage)
    
def insert_names (cursora,new_sheetb,ending,row_i,col_i, exe):
    ##### Name
    query="SELECT DISTINCT fname, lname FROM pitch_log_t "
    query+=ending
    cursora.execute(query, exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0 ):
        trip=True
    
    for i, (fname, lname) in enumerate(data,3):
        if (trip):
            row_i=i
        full_name = f"{fname} {lname}"
        new_sheetb.cell(row=row_i,column=col_i, value=full_name)

def insert_oppo(cursorb,new_sheetb,ending,row_i,column_i,exe):
    ##### Opponent
    query= "SELECT opponent AS oppo FROM pitch_log_t "
    query+= ending
    cursorb.execute(query,exe)
    data=cursorb.fetchall()
    
    for k, (oppo,) in enumerate(data, 3):
        if (row_i==0):
            row_i=k
        put_in = oppo[0] if isinstance(oppo, tuple) and oppo else oppo
        new_sheetb.cell(row=row_i, column=column_i, value=put_in)
        
def insert_pitches_thrown(cursorb,new_sheetb,ending,row_i,column_i,exe):
    ##### Pitches Thrown
    query="SELECT COUNT(pitch_id) AS pitchCount FROM pitch_log_t "
    query+= ending
    cursorb.execute(query, exe)
    data=cursorb.fetchall()
    trip=False
    if (row_i==0):
        trip=True
    tpc=0 ########################################################################### Problem Here for pitcher logs
    for k, (pitchCount,) in enumerate(data, 3):
        if (trip):
            row_i=k
        put_in = int(pitchCount) if pitchCount is not None else 0
        new_sheetb.cell(row=row_i, column=column_i, value=put_in)
        tpc += put_in
    return tpc
        
def insert_pitches_per_inning(cursora,new_sheetb,ending,row_i,col_i,exe):
    ##### Pitches Per Inning
    query= "SELECT COUNT(pitch_id) AS pitchCount, MAX(outs_accrued) AS outs FROM pitch_log_t "
    query+=ending
    cursora.execute(query, exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
    
    ti=0
    for k, (pitchCount, outs) in enumerate(data, 3):
        if (trip):
            row_i=k
        innings= int(outs)/3 if outs is not None else 0
        ti+=innings 
        count_a=int(pitchCount) if pitchCount is not None else 0
        if (innings!=0):
            put_in = count_a/innings
            put_in=round (put_in,2)
        else:
            put_in=0
        new_sheetb.cell(row=row_i, column=col_i, value=put_in)
    return ti
        
def insert_peak_velo(cursora,new_sheetb,ending,row_i,col_i,exe):
    ##### Peak Velocity
    query="SELECT MAX(velocity) AS velo FROM pitch_log_t "
    query+=ending
    cursora.execute(query, exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
    tpv=0    
    arms=len(data)
    #print(arms)
    for k, (velo,) in enumerate(data,3):
        if (trip):
            row_i=k
        put_in = int(velo) if velo is not None else 0
        tpv+=put_in 
        new_sheetb.cell(row=row_i, column=col_i, value=put_in)
    return tpv, arms
  
def insert_1st_pitch_strike_percentage(cursora,new_sheetb,ending,row_i,col_i,exe,goodNum):
    ##### 1st Pitch Strike Percentage
    query="SELECT CASE WHEN COUNT(CASE WHEN balls = 0 AND strikes = 0 THEN 1 END) > 0 "
    query+="THEN (COUNT(CASE WHEN balls = 0 AND strikes = 0 AND pitch_result <> 'B' AND pitch_result <> 'HBP' THEN 1 END) * 100.0 / "
    query+="COUNT(CASE WHEN balls = 0 AND strikes = 0 THEN 1 END)) ELSE 0 END AS Percentage FROM pitch_log_t "
    query+= ending
    cursora.execute(query,exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
    
    for k, (percentage,) in enumerate(data,3):
        if (trip):
            row_i=k
        put_in = int(percentage) if percentage is not None else 0
        cella = new_sheetb.cell(row=row_i, column=col_i, value=put_in)
        
        if put_in >= goodNum:
            cella.font = Font(bold=True)
            
def insert_off_speed_strike_percentage(cursora,new_sheetb,ending,row_i,col_i,exe,goodNum):
    ##### Off-Speed Strike Percentage
    query="SELECT CASE WHEN COUNT(CASE WHEN pitch_type <> 'FB' and pitch_type <> 'CU' THEN 1 END) > 0 "
    query+="THEN (COUNT(CASE WHEN pitch_type <> 'FB' AND pitch_type <> 'CU' AND pitch_result <> 'B' AND pitch_result <> 'HBP' THEN 1 END) * 100.0 / "
    query+="COUNT(CASE WHEN pitch_type <> 'FB' and pitch_type <> 'CU' THEN 1 END)) ELSE 0 END AS PercentageOFF FROM pitch_log_t "
    query+=ending
    cursora.execute(query ,exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
    
    for k, (percentageOFF,) in enumerate(data,3):
        if (trip):
            row_i=k
        put_in = int(percentageOFF) if percentageOFF is not None else 0
        cella = new_sheetb.cell(row=row_i, column=col_i, value=put_in)
        
        if put_in >= goodNum:
            cella.font = Font(bold=True)
            
def insert_swing_and_miss_percentage(cursora,new_sheetb,ending,row_i,col_i,exe,goodNum):
    ##### Swing and Miss Percentage
    query ="SELECT CASE WHEN COUNT(CASE WHEN pitch_result <>'0' THEN 1 END) > 0 "
    query+="THEN (COUNT(CASE WHEN pitch_result = 'SS' or pitch_result = 'SSC' or pitch_result = 'D3SS' THEN 1 END) * 100.0 / "
    query+="COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS Misses FROM pitch_log_t "
    query+= ending
    cursora.execute(query,exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
    
    for k, (misses,) in enumerate(data,3):
        if (trip):
            row_i=k
        put_in = int(misses) if misses is not None else 0
        cella = new_sheetb.cell(row=row_i, column=col_i, value=put_in)
         
        if put_in >= goodNum:
            cella.font = Font(bold=True)
    
def insert_velo_range(cursora,new_sheetb,ending,row_i,col_i,exe,trigger1,trigger2, trigger3):
    ##### Velocity Range
    query="SELECT MIN(velocity) AS MINV, MAX(velocity) AS MAXV FROM pitch_log_t "
    if trigger1:
        query += "WHERE pitch_type = 'FB' AND pitch_id <> '0' AND opponent <> 'Scrimmage' GROUP BY fname,lname ORDER BY fname,lname"
    if trigger2:
        query+="WHERE pitch_type = 'FB' AND date = %s AND opponent = %s AND opponent <> 'Scrimmage' GROUP BY fname,lname ORDER BY fname,lname"
    if trigger3:
        query+="WHERE pitch_type = 'FB' AND date = %s AND opponent = %s GROUP BY fname,lname ORDER BY fname,lname"
    if not (trigger1 or trigger2 or trigger3):
        query+= ending
        query += " AND pitch_type = 'FB' "
    
    cursora.execute(query, exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
     
    for k, (minv, maxv) in enumerate(data, 3):
        if (trip):
            row_i=k
        min_value = int(minv) if minv is not None else 0
        max_value = int(maxv) if maxv is not None else 0
        put_in = f"{min_value}-{max_value}"
        new_sheetb.cell(row=row_i, column=col_i, value=put_in)

def insert_chases(cursora,new_sheetb,ending,row_i,col_i,exe):
    ##### Chases
    query="SELECT SUM(CASE WHEN pitch_result='SSC' or pitch_result='D3SS' THEN 1 ELSE 0 END) AS chases, Max(outs_accrued)/3 AS IP FROM pitch_log_t "
    query+=ending
    cursora.execute(query, exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True

    for k, (chases,ip,) in enumerate(data,3):
        if (trip):
            row_i=k
        put_in = int(chases) if chases is not None else 0
        cella=new_sheetb.cell(row=row_i, column=col_i, value=put_in)

        innings= int(ip) if ip is not None else 0
        if put_in >= innings:
            cella.font = Font(bold=True)

def insert_ahead_after_3_pitches_percentage(cursora,new_sheetb,ending,row_i,col_i,exe,goodNum):
    ##### Ahead After 3 Pitches Percentage
    query = "SELECT CASE WHEN COUNT(CASE WHEN (balls=1 AND strikes=2) or (balls=2 AND strikes=1) or (balls=0 AND strikes=2 AND pitch_result Not IN ('B','F')) or (balls=2 AND strikes=0 AND pitch_result IN ('B','HBP','BIP'))THEN 1 END) > 0 "
    query+="THEN (COUNT(CASE WHEN (balls=1 AND strikes=2) or (balls=0 AND strikes=2 AND pitch_result Not IN ('B','F')) THEN 1 END) * 100.0 / "
    query+="COUNT(CASE WHEN (balls=1 AND strikes=2) or (balls=2 AND strikes=1) or (balls=0 AND strikes=2 AND pitch_result Not IN ('B','F','HBP')) or (balls=2 AND strikes=0 AND pitch_result IN ('B','HBP','BIP'))THEN 1 END)) ELSE 0 END AS AA3P FROM pitch_log_t "
    query+=ending
    cursora.execute(query,exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True

    for k, (aa3p,) in enumerate(data,3):
        if (trip):
            row_i=k
        put_in = int(aa3p) if aa3p is not None else 0
        cella = new_sheetb.cell(row=row_i, column=col_i, value=put_in)
 
        if put_in >= goodNum:
            cella.font = Font(bold=True)   
            
def insert_lead_off_out_percentage(cursora,new_sheetb,ending,row_i,col_i,exe,goodNum):
    ##### Lead Off Out Percentage
    query = "SELECT CASE WHEN COUNT(CASE WHEN batter_of_inning = 1 and ab_result <> '0' THEN 1 END) > 0 "
    query+= "THEN (COUNT(CASE WHEN batter_of_inning = 1 AND ab_result = 'out' THEN 1 END) * 100.0 / COUNT(CASE WHEN batter_of_inning = 1 AND (ab_result = 'out' or ab_result = 'safe') THEN 1 END)) ELSE 0 END AS LOO FROM pitch_log_t "
    query+= ending
    cursora.execute(query, exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
    
    for k, (loo,) in enumerate(data,3):
        if (trip):
            row_i=k
        put_in = int(loo) if loo is not None else 0
        cella=new_sheetb.cell(row=row_i, column=col_i, value=put_in)
        
        if put_in >= goodNum:
            cella.font = Font(bold=True)

def insert_overall_strike_percentage(cursora,new_sheetb,ending,row_i,col_i,exe,goodNum):
    ##### Overall Strike Percentage
    query="SELECT CASE WHEN COUNT(CASE WHEN pitch_result <> '0' THEN 1 END) > 0 "
    query+="THEN (COUNT(CASE WHEN pitch_result <> 'B' AND pitch_result <> 'HBP' THEN 1 END) * 100.0 / "
    query+="COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS OvePer FROM pitch_log_t "
    query+=ending
    cursora.execute(query,exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
    
    for k, (oveper,) in enumerate(data,3):
        if (trip):
            row_i=k
        put_in = int(oveper) if oveper is not None else 0
        cella = new_sheetb.cell(row=row_i, column=col_i, value=put_in)
        
        if put_in >= goodNum:
            cella.font = Font(bold=True)

def insert_baa_with_2_strikes(cursora,new_sheetb,ending,row_i,col_i,exe,goodNum):
    ##### Opponent Batting Average with 2 Strikes
    query="SELECT CASE WHEN COUNT(CASE WHEN strikes = 2 AND ab_result <> '0' and (pitch_result <> 'B' and pitch_result <> 'HBP') THEN 1 END) > 0 "
    query+="THEN (COUNT(CASE WHEN strikes = 2 AND ab_result = 'safe' and bip_result In ('1B','2B','3B','HR') and bip_result <> 'E' THEN 1 END) * 1.0 / "
    query+="COUNT(CASE WHEN strikes = 2 AND ab_result <> '0' and (pitch_result <> 'B' and pitch_result <> 'HBP') THEN 1 END)) ELSE 0 END AS BAAw2K FROM pitch_log_t "
    query+= ending
    cursora.execute(query,exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
    
    for k, (baaw2k,) in enumerate(data,3):
        if (trip):
            row_i=k
        put_in = round(float(baaw2k),3) if baaw2k is not None else 0
        cella = new_sheetb.cell(row=row_i, column=col_i, value=put_in)
        
        if put_in <=goodNum:
            cella.font = Font(bold=True)
            
def insert_advantage_counts_percentage(cursora,new_sheetb,ending,row_i,col_i,exe):
    ##### Percentage of Pitches Thrown in Advantage Counts
    query = "SELECT CASE WHEN COUNT(CASE WHEN pitch_result <>'0' THEN 1 END) > 0 "
    query+= "THEN (COUNT(CASE WHEN strikes>balls THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS PTIAC FROM pitch_log_t "
    query+= ending
    cursora.execute(query, exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
    
    for k, (ptiac,) in enumerate(data,3):
        if (trip):
            row_i=k
        put_in = int(ptiac) if ptiac is not None else 0
        new_sheetb.cell(row=row_i, column=col_i, value=put_in)     
        
def insert_disadvantage_counts_percentage(cursora,new_sheetb,ending,row_i,col_i,exe):
    ##### Percentage of Pitches Thrown in DisAdvantage Counts
    query = "SELECT CASE WHEN COUNT(CASE WHEN pitch_result <>'0' THEN 1 END) > 0 "
    query+= "THEN (COUNT(CASE WHEN strikes<balls THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS PTIDC FROM pitch_log_t "
    query+= ending
    cursora.execute(query, exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
    
    for k, (ptidc,) in enumerate(data,3):
        if (trip):
            row_i=k
        put_in = int(ptidc) if ptidc is not None else 0
        new_sheetb.cell(row=row_i, column=col_i, value=put_in)

def insert_strikeout_percentage(cursora,new_sheetb,ending,row_i,col_i,exe):
    ##### Strikeout Percentage
    query = "SELECT CASE WHEN COUNT(CASE WHEN ab_result <> '0' THEN 1 END) >0"
    query += " THEN (COUNT(CASE WHEN strikes = 2 AND (pitch_result = 'SL' or pitch_result = 'SS' or pitch_result = 'SSC' or pitch_result = 'D3SS') THEN 1 END) * 100 /" 
    query += " COUNT(CASE WHEN ab_result <> '0' THEN 1 END)) ELSE 0 END AS KPer FROM pitch_log_t "
    query += ending
    cursora.execute(query, exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
    
    for k, (kper,) in enumerate(data,3):
        if (trip):
            row_i=k
        put_in = int(kper) if kper is not None else 0
        new_sheetb.cell(row=row_i, column=col_i, value=put_in)
        
def insert_ground_ball_out_percentage(cursora,new_sheetb,ending,row_i,col_i,exe):
    ##### Ground Ball Out Percentage
    query = "SELECT CASE WHEN COUNT(CASE WHEN pitch_result = 'BIP' THEN 1 END) >0"
    query += " THEN (COUNT(CASE WHEN bip_result = 'GO' OR bip_result = 'DP' THEN 1 END) * 100 /"
    query += " COUNT(CASE WHEN pitch_result = 'BIP' THEN 1 END)) ELSE 0 END AS GBOPer FROM pitch_log_t "
    query += ending
    cursora.execute(query, exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
     
    for k, (gboper,) in enumerate(data,3):
        if (trip):
            row_i=k
        put_in = int(gboper) if gboper is not None else 0
        new_sheetb.cell(row=row_i, column=col_i, value=put_in)
        
def insert_fly_ball_out_percentage(cursora,new_sheetb,ending,row_i,col_i,exe):
    ##### Fly Ball Out Percentage
    query = "SELECT CASE WHEN COUNT(CASE WHEN pitch_result = 'BIP' THEN 1 END) >0"
    query += " THEN (COUNT(CASE WHEN bip_result = 'FO' THEN 1 END) * 100 /" 
    query += " COUNT(CASE WHEN pitch_result = 'BIP' THEN 1 END)) ELSE 0 END AS FBOPer FROM pitch_log_t "
    query += ending
    cursora.execute(query, exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
     
    for k, (fboper,) in enumerate(data,3):
        if (trip):
            row_i=k
        put_in = int(fboper) if fboper is not None else 0
        new_sheetb.cell(row=row_i, column=col_i, value=put_in)  

def insert_baa_bip(cursora,new_sheetb,ending,row_i,col_i,exe):
    ##### Oppenent Batting Average on Balls in Play
    query = "SELECT COUNT(CASE WHEN pitch_result = 'BIP' THEN 1 END) AS BIP, "
    query+="COUNT(CASE WHEN ab_result = 'safe' AND pitch_result = 'BIP' THEN 1 END) AS BIPSAFE FROM pitch_log_t "
    query += ending
    cursora.execute(query, exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
    
    for k, (bip,bipsafe) in enumerate(data,3):
        if (trip):
            row_i=k
        bip=int(bip) if bip is not None else 0
        bipsafe=int(bipsafe)*1.0 if bipsafe is not None else 0
        if bip!=0:
            put_in=bipsafe/bip
        else:
            put_in=0
        put_in=round(put_in,3)
        new_sheetb.cell(row=row_i, column=col_i, value=put_in)  
        
def insert_at_bat_win_rate(cursora,new_sheetb,ending,row_i,col_i,exe):
    ##### Percentage of At Bats that resulted in an Out
    query = "SELECT CASE WHEN COUNT(CASE WHEN ab_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN ab_result = 'out' THEN 1 END) * 100.0 / "
    query += "COUNT(CASE WHEN ab_result <> '0' THEN 1 END)) ELSE 0 END AS WINRATE FROM pitch_log_t "
    query += ending
    
    cursora.execute(query,exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
        
    for k,(winrate,) in enumerate(data,3):
        if (trip):
            row_i=k
        put_in=int(winrate) if winrate is not None else 0
        new_sheetb.cell(row=row_i, column=col_i, value=put_in)
        
def insert_pitch_spread_percentage(cursora,new_sheetb,ending,row_i,col_i,exe):
    ##### Fastball - Curveball - Slider - Change UP - Splitter Spread Percentage
    query = "SELECT "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'FB' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'FB' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS FBP, "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'CB' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'CB' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS CBP, "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'SL' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'SL' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS SLP, "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'CH' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'CH' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS CHP, "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'SP' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'SP' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END))ELSE 0 END AS SPP, "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'CU' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'CU' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END))ELSE 0 END AS CUP "
    query += "FROM pitch_log_t "
    query +=ending
    
    cursora.execute(query,exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
        
    for k,(FBP,CBP,SLP,CHP,SPP,CUP) in enumerate(data,3):
        if (trip):
            row_i=k
        FBP=int(FBP) if FBP is not None else 0
        CBP=int(CBP) if CBP is not None else 0
        SLP=int(SLP) if SLP is not None else 0
        CHP=int(CHP) if CHP is not None else 0
        SPP=int(SPP) if SPP is not None else 0
        CUP=int(CUP) if CUP is not None else 0  
        
        put_in = f"{FBP}-{CBP}-{SLP}-{CHP}-{SPP}-{CUP}"
        new_sheetb.cell(row=row_i, column=col_i, value=put_in)
        
def insert_pitch_spread_strike_percentage(cursora,new_sheetb,ending,row_i,col_i,exe):
    ##### Fastball - Curveball - Slider - Change UP - Splitter Spread Strike Percentage
    query = "SELECT "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'FB' AND pitch_result <> 'B' AND pitch_result <> 'HBP' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'FB' AND pitch_result <> 'B' AND pitch_result <> 'HBP' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS FBP, "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'CB' AND pitch_result <> 'B' AND pitch_result <> 'HBP' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'CB' AND pitch_result <> 'B' AND pitch_result <> 'HBP' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS CBP, "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'SL' AND pitch_result <> 'B' AND pitch_result <> 'HBP' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'SL' AND pitch_result <> 'B' AND pitch_result <> 'HBP' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS SLP, "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'CH' AND pitch_result <> 'B' AND pitch_result <> 'HBP' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'CH' AND pitch_result <> 'B' AND pitch_result <> 'HBP' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS CHP, "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'SP' AND pitch_result <> 'B' AND pitch_result <> 'HBP' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'SP' AND pitch_result <> 'B' AND pitch_result <> 'HBP' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS SPP, "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'CU' AND pitch_result <> 'B' AND pitch_result <> 'HBP' AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'CU' AND pitch_result <> 'B' AND pitch_result <> 'HBP' THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS CUP "
    query += "FROM pitch_log_t "
    query +=ending
    
    cursora.execute(query,exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
        
    for k,(FBP,CBP,SLP,CHP,SPP,CUP) in enumerate(data,3):
        if (trip):
            row_i=k
        FBP=int(FBP) if FBP is not None else 0
        CBP=int(CBP) if CBP is not None else 0
        SLP=int(SLP) if SLP is not None else 0
        CHP=int(CHP) if CHP is not None else 0
        SPP=int(SPP) if SPP is not None else 0
        CUP=int(CUP) if CUP is not None else 0  
                
        put_in = f"{FBP}-{CBP}-{SLP}-{CHP}-{SPP}-{CUP}"
        new_sheetb.cell(row=row_i, column=col_i, value=put_in)       
        
def insert_pitch_spread_whiff_percentage(cursora,new_sheetb,ending,row_i,col_i,exe):
    ##### Fastball - Curveball - Slider - Change UP - Splitter Spread whiff Percentage
    query = "SELECT "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'FB' AND (pitch_result = 'SS' or pitch_result = 'SSC' or pitch_result = 'D3SS') AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'FB' AND (pitch_result = 'SS' or pitch_result = 'SSC' or pitch_result = 'D3SS') THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS FBP, "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'CB' AND (pitch_result = 'SS' or pitch_result = 'SSC' or pitch_result = 'D3SS') AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'CB' AND (pitch_result = 'SS' or pitch_result = 'SSC' or pitch_result = 'D3SS') THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS CBP, "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'SL' AND (pitch_result = 'SS' or pitch_result = 'SSC' or pitch_result = 'D3SS') AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'SL' AND (pitch_result = 'SS' or pitch_result = 'SSC' or pitch_result = 'D3SS') THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS SLP, "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'CH' AND (pitch_result = 'SS' or pitch_result = 'SSC' or pitch_result = 'D3SS') AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'CH' AND (pitch_result = 'SS' or pitch_result = 'SSC' or pitch_result = 'D3SS') THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS CHP, "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'SP' AND (pitch_result = 'SS' or pitch_result = 'SSC' or pitch_result = 'D3SS')  AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'SP' AND (pitch_result = 'SS' or pitch_result = 'SSC' or pitch_result = 'D3SS') THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS SPP, "
    query += "CASE WHEN COUNT(CASE WHEN pitch_type = 'CU' AND (pitch_result = 'SS' or pitch_result = 'SSC' or pitch_result = 'D3SS') AND pitch_result <> '0' THEN 1 END) > 0 "
    query += "THEN (COUNT(CASE WHEN pitch_type = 'CU' AND (pitch_result = 'SS' or pitch_result = 'SSC' or pitch_result = 'D3SS') THEN 1 END) * 100.0 / COUNT(CASE WHEN pitch_result <> '0' THEN 1 END)) ELSE 0 END AS CUP "
    query += "FROM pitch_log_t "
    query +=ending
    
    cursora.execute(query,exe)
    data=cursora.fetchall()
    trip=False
    if (row_i==0):
        trip=True
        
    for k,(FBP,CBP,SLP,CHP,SPP,CUP) in enumerate(data,3):
        if (trip):
            row_i=k
        FBP=int(FBP) if FBP is not None else 0
        CBP=int(CBP) if CBP is not None else 0
        SLP=int(SLP) if SLP is not None else 0
        CHP=int(CHP) if CHP is not None else 0
        SPP=int(SPP) if SPP is not None else 0
        CUP=int(CUP) if CUP is not None else 0  
                
        put_in = f"{FBP}-{CBP}-{SLP}-{CHP}-{SPP}-{CUP}"
        new_sheetb.cell(row=row_i, column=col_i, value=put_in)
        

#updates pitchers logs
def up_pitchers_log(cursor,update_date,file_name):
           
           workbook=create_workbook(file_name)[0]
           file_path=create_workbook(file_name)[1]
         
           wipe (workbook)
           
           ##### Name
           cursor.execute("SELECT DISTINCT fname, lname FROM pitch_log_t WHERE pitch_id <>'0' ")
           data=cursor.fetchall()
           
           for i, (fname, lname) in enumerate(data,3):
               name = f"{fname} {lname}"
               sheetname=name 
               
                                    
               new_sheet=setup(sheetname,workbook,"Name",name,"Updated Date",update_date,"","",header_pos,pitcher_headers)
               

               query="SELECT DISTINCT date AS datea FROM pitch_log_t WHERE fname=%s AND lname = %s and pitch_id <> '0' "
               cursor.execute(query,(fname,lname))
               data=cursor.fetchall()
               
               total_pitch_count=0
               total_innings=0
               total_peak_velo=0
               pitchers=0
               
               
               for j, (datea) in enumerate(data,3):
                   dates=len(data)
                   datea =datea[0] if isinstance(datea, tuple) and datea else datea
                   new_sheet.cell(row=j, column=1, value=datea)
                   
                   exea=(datea,fname,lname)
                   iplEndStatement="WHERE date = %s AND fname = %s AND lname = %s AND pitch_id <> '0' "
                           
                   insert_oppo(cursor, new_sheet,iplEndStatement,j,2,exea)
                   
                   total_pitch_count+=insert_pitches_thrown(cursor, new_sheet, iplEndStatement, j, 3, exea)
                   
                   total_innings+=insert_pitches_per_inning(cursor, new_sheet, iplEndStatement, j, 4, exea)
                   
                   a, b=insert_peak_velo(cursor, new_sheet, iplEndStatement, j, 5, exea)
                  
                   total_peak_velo+=a
                   pitchers+=b
                               
                   insert_1st_pitch_strike_percentage(cursor, new_sheet, iplEndStatement, j, 6, exea, 60)
                   
                   insert_off_speed_strike_percentage(cursor, new_sheet, iplEndStatement, j, 7, exea, 50)
                 
                   insert_swing_and_miss_percentage(cursor, new_sheet,iplEndStatement, j, 8, exea, 25)
                        
                   insert_velo_range(cursor, new_sheet, iplEndStatement, j, 9, exea,False,False,False)        
                           
                   insert_chases(cursor, new_sheet, iplEndStatement, j, 10, exea)
                   
                   insert_ahead_after_3_pitches_percentage(cursor,new_sheet,iplEndStatement,j,11,exea,60)
                   
                   insert_lead_off_out_percentage(cursor, new_sheet, iplEndStatement, j, 12, exea, 65)
                   
                   insert_overall_strike_percentage(cursor, new_sheet, iplEndStatement, j, 13, exea, 60)
                   
                   insert_baa_with_2_strikes(cursor, new_sheet, iplEndStatement, j, 14, exea, 0.15)
                   
                   insert_advantage_counts_percentage(cursor, new_sheet, iplEndStatement, j, 15, exea)
                   
                   insert_disadvantage_counts_percentage(cursor, new_sheet, iplEndStatement, j, 16, exea)
                                      
                   insert_strikeout_percentage(cursor, new_sheet, iplEndStatement, j, 17, exea)
                   
                   insert_ground_ball_out_percentage(cursor, new_sheet, iplEndStatement, j, 18, exea)
                   
                   insert_fly_ball_out_percentage(cursor, new_sheet, iplEndStatement, j, 19, exea)
                    
                   insert_baa_bip(cursor, new_sheet, iplEndStatement, j, 20, exea)
                   
                   insert_at_bat_win_rate(cursor, new_sheet, iplEndStatement, j, 21, exea)
                   
                   insert_pitch_spread_percentage(cursor, new_sheet, iplEndStatement, j, 22, exea)
                   
                   insert_pitch_spread_strike_percentage(cursor, new_sheet, iplEndStatement, j, 23, exea)
                   
                   insert_pitch_spread_whiff_percentage(cursor, new_sheet, iplEndStatement, j, 24, exea)
                   
               ######################## Player's Season Totals ####################################
               
               iplEndStatement="WHERE fname = %s AND lname = %s AND pitch_id <> '0' AND opponent <> 'Scrimmage' "
               exea=(fname,lname)
               
               # Calculate and insert team totals
               season_totals_row = dates + 4  # Assuming a gap of one row between individual pitchers and team totals
               
               new_sheet.cell(row=season_totals_row, column=1, value="Season Totals")
            
               ##### Total Pitch Count
               new_sheet.cell(row=season_totals_row, column=2, value="-")
        
               ##### Total Pitch Count
               new_sheet.cell(row=season_totals_row, column=3, value=total_pitch_count)
        
               ##### Average Pitches Per Inning
               if total_innings !=0:
                   new_sheet.cell(row=season_totals_row, column=4, value=round(total_pitch_count/total_innings,2))
               else:
                   new_sheet.cell(row=season_totals_row,column = 4, value = 0)
            
               #####  Average Peak Velocity
               if pitchers!=0:
                   new_sheet.cell(row=season_totals_row, column=5, value=round(total_peak_velo/pitchers,2))
               else:
                   new_sheet.cell(row=season_totals_row,column = 5, value = 0)
               
               
               insert_1st_pitch_strike_percentage(cursor, new_sheet, iplEndStatement, season_totals_row, 6, exea, 60)
               
               insert_off_speed_strike_percentage(cursor, new_sheet, iplEndStatement, season_totals_row, 7, exea, 50)
             
               insert_swing_and_miss_percentage(cursor, new_sheet,iplEndStatement, season_totals_row, 8, exea, 25)
                    
               insert_velo_range(cursor, new_sheet, iplEndStatement, season_totals_row, 9, exea,False,False,False)        
                       
               insert_chases(cursor, new_sheet, iplEndStatement, season_totals_row, 10, exea)
               
               insert_ahead_after_3_pitches_percentage(cursor,new_sheet,iplEndStatement,season_totals_row,11,exea,60)
               
               insert_lead_off_out_percentage(cursor, new_sheet, iplEndStatement, season_totals_row, 12, exea, 65)
               
               insert_overall_strike_percentage(cursor, new_sheet, iplEndStatement, season_totals_row, 13, exea, 60)
               
               insert_baa_with_2_strikes(cursor, new_sheet, iplEndStatement, season_totals_row, 14, exea, 0.15)
               
               insert_advantage_counts_percentage(cursor, new_sheet, iplEndStatement, season_totals_row, 15, exea)
               
               insert_disadvantage_counts_percentage(cursor, new_sheet, iplEndStatement, season_totals_row, 16, exea)
                                  
               insert_strikeout_percentage(cursor, new_sheet, iplEndStatement, season_totals_row, 17, exea)
               
               insert_ground_ball_out_percentage(cursor, new_sheet, iplEndStatement, season_totals_row, 18, exea)
               
               insert_fly_ball_out_percentage(cursor, new_sheet, iplEndStatement, season_totals_row, 19, exea)
                
               insert_baa_bip(cursor, new_sheet, iplEndStatement, season_totals_row, 20, exea)
                                 
               insert_at_bat_win_rate(cursor, new_sheet, iplEndStatement, season_totals_row, 21, exea)
               
               insert_pitch_spread_percentage(cursor, new_sheet, iplEndStatement, season_totals_row, 22, exea)
               
               insert_pitch_spread_strike_percentage(cursor, new_sheet, iplEndStatement, season_totals_row, 23, exea)
               
               insert_pitch_spread_whiff_percentage(cursor, new_sheet, iplEndStatement, season_totals_row, 24, exea)    
                                  
               bold_first_column_if_threshold(new_sheet, 5)
               
               adjust_formating(new_sheet, season_totals_row)
          
           savebook(workbook, file_path, "Pitcher Logs Updated")
           
#updates season log
def up_season_log(cursor,date,file_name):
            
    
           workbook=create_workbook(file_name)[0]
           file_path=create_workbook(file_name)[1]
         
           
            
           sheetname=date
           
           new_sheet=setup(sheetname, workbook, "Updated Date", date, "", "", "", "", header_pos, season_game_headers)
           
           exea=()
           iplEndStatement="WHERE pitch_id <> '0' AND opponent <> 'Scrimmage' GROUP BY fname, lname ORDER BY fname,lname"
 
           ##### Name
           cursor.execute("SELECT DISTINCT fname, lname FROM pitch_log_t WHERE pitch_id <> '0' AND opponent <> 'Scrimmage' GROUP BY fname,lname Order By fname,lname")
           data=cursor.fetchall()
           
           for i, (fname, lname) in enumerate(data,3):
               full_name = f"{fname} {lname}"
               new_sheet.cell(row=i, column=1, value=full_name)
             
           total_pitch_count=insert_pitches_thrown(cursor, new_sheet, iplEndStatement, 0, 2, exea)
           
           total_innings=insert_pitches_per_inning(cursor, new_sheet, iplEndStatement, 0, 3, exea)
          
           total_peak_velo, pitchers=insert_peak_velo(cursor, new_sheet, iplEndStatement, 0, 4, exea) 
                       
           insert_1st_pitch_strike_percentage(cursor, new_sheet, iplEndStatement, 0, 5, exea, 60)
           
           insert_off_speed_strike_percentage(cursor, new_sheet, iplEndStatement, 0, 6, exea, 50)
         
           insert_swing_and_miss_percentage(cursor, new_sheet,iplEndStatement, 0, 7, exea, 25)
                
           insert_velo_range(cursor, new_sheet, iplEndStatement, 0, 8, exea,True,False,False)   
                   
           insert_chases(cursor, new_sheet, iplEndStatement, 0, 9, exea)
           
           insert_ahead_after_3_pitches_percentage(cursor,new_sheet,iplEndStatement,0,10,exea,60)
           
           insert_lead_off_out_percentage(cursor, new_sheet, iplEndStatement, 0, 11, exea, 65)
           
           insert_overall_strike_percentage(cursor, new_sheet, iplEndStatement, 0, 12, exea, 60)
           
           insert_baa_with_2_strikes(cursor, new_sheet, iplEndStatement, 0, 13, exea, 0.15)
           
           insert_advantage_counts_percentage(cursor, new_sheet, iplEndStatement, 0, 14, exea)
           
           insert_disadvantage_counts_percentage(cursor, new_sheet, iplEndStatement, 0, 15, exea)
                              
           insert_strikeout_percentage(cursor, new_sheet, iplEndStatement, 0, 16, exea)
           
           insert_ground_ball_out_percentage(cursor, new_sheet, iplEndStatement, 0, 17, exea)
           
           insert_fly_ball_out_percentage(cursor, new_sheet, iplEndStatement, 0, 18, exea)
            
           insert_baa_bip(cursor, new_sheet, iplEndStatement, 0, 19, exea)
           
           insert_at_bat_win_rate(cursor, new_sheet, iplEndStatement, 0, 20, exea)
           
           insert_pitch_spread_percentage(cursor, new_sheet, iplEndStatement, 0, 21, exea)
           
           insert_pitch_spread_strike_percentage(cursor, new_sheet, iplEndStatement, 0, 22, exea)
           
           insert_pitch_spread_whiff_percentage(cursor, new_sheet, iplEndStatement, 0, 23, exea)
           
           
               
           ################################## Team Totals ############################################# 
             
           exea=()
           iplEndStatement="WHERE pitch_id <> '0' AND opponent <> 'Scrimmage' "
            
           # Calculate and insert team totals
           team_totals_row = len(data) + 4  # Assuming a gap of one row between individual pitchers and team totals

           new_sheet.cell(row=team_totals_row, column=1, value="Team Totals")
           
           
           ##### Total Pitch Count
           new_sheet.cell(row=team_totals_row, column=2, value=total_pitch_count)
           
           ##### Average Pitches Per Inning
           if total_innings!=0:
               new_sheet.cell(row=team_totals_row, column=3, value=round(total_pitch_count/total_innings,2))
           else:
               new_sheet.cell(row=team_totals_row, column=3, value=0)
           
           #####  Average Peak Velocity
           if pitchers!=0:
               new_sheet.cell(row=team_totals_row, column=4, value=round(total_peak_velo/pitchers,2))
           else:
               new_sheet.cell(row=team_totals_row, column=4, value=0)
               
               
          
           insert_1st_pitch_strike_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 5, exea, 60)
           
           insert_off_speed_strike_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 6, exea, 50)
         
           insert_swing_and_miss_percentage(cursor, new_sheet,iplEndStatement, team_totals_row, 7, exea, 25)
                
           insert_velo_range(cursor, new_sheet, iplEndStatement, team_totals_row, 8, exea,True,False,False)        
                   
           insert_chases(cursor, new_sheet, iplEndStatement, team_totals_row, 9, exea)
           
           insert_ahead_after_3_pitches_percentage(cursor,new_sheet,iplEndStatement,team_totals_row,10,exea,60)
           
           insert_lead_off_out_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 11, exea, 65)
           
           insert_overall_strike_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 12, exea, 60)
           
           insert_baa_with_2_strikes(cursor, new_sheet, iplEndStatement, team_totals_row, 13, exea, 0.15)
           
           insert_advantage_counts_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 14, exea)
           
           insert_disadvantage_counts_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 15, exea)
                              
           insert_strikeout_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 16, exea)
           
           insert_ground_ball_out_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 17, exea)
           
           insert_fly_ball_out_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 18, exea)
            
           insert_baa_bip(cursor, new_sheet, iplEndStatement, team_totals_row, 19, exea)
                      
           insert_at_bat_win_rate(cursor, new_sheet, iplEndStatement, team_totals_row, 20, exea)
           
           insert_pitch_spread_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 21, exea)
           
           insert_pitch_spread_strike_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 22, exea)
           
           insert_pitch_spread_whiff_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 23, exea)
           
           bold_first_column_if_threshold(new_sheet, 5)
           
           adjust_formating(new_sheet, team_totals_row)
           
           
           savebook(workbook, file_path, "Season Log Updated")
           
#updates game log
def up_game_log(cursor,updated_date,file_name):

            workbook=create_workbook(file_name)[0]
            file_path=create_workbook(file_name)[1]
          
            wipe (workbook)
            
            query="SELECT DISTINCT date AS datea,opponent as oppo FROM pitch_log_t WHERE pitch_id<>0 "
            cursor.execute(query)
            data=cursor.fetchall()
            
            for j, (datea,oppo) in enumerate(data,3):
                
                datea = str(datea) if datea is not None else ""
                oppo = str(oppo) if oppo is not None else ""
                exea=(datea,oppo)
                
                iplEndStatement="WHERE date = %s AND opponent = %s AND pitch_id <> '0'  GROUP BY fname,lname ORDER BY fname,lname "
                

                sheetname=datea +" "+oppo
                
                new_sheet=setup(sheetname,workbook,"Date",datea,"Opponent",oppo,"Updated Date",updated_date,header_pos,season_game_headers)
                
                
                insert_names(cursor,new_sheet,iplEndStatement,0,1,exea)
                
                total_pitch_count=insert_pitches_thrown(cursor, new_sheet, iplEndStatement, 0, 2, exea)
                
                total_innings=insert_pitches_per_inning(cursor, new_sheet, iplEndStatement, 0, 3, exea)
               
                total_peak_velo,pitchers = insert_peak_velo(cursor, new_sheet, iplEndStatement, 0, 4, exea) 
                            
                insert_1st_pitch_strike_percentage(cursor, new_sheet, iplEndStatement, 0, 5, exea, 60)
                
                insert_off_speed_strike_percentage(cursor, new_sheet, iplEndStatement, 0, 6, exea, 50)
              
                insert_swing_and_miss_percentage(cursor, new_sheet,iplEndStatement, 0, 7, exea, 25)
                     
                insert_velo_range(cursor, new_sheet, iplEndStatement, 0, 8, exea,False,False,True)   
                        
                insert_chases(cursor, new_sheet, iplEndStatement, 0, 9, exea)
                
                insert_ahead_after_3_pitches_percentage(cursor,new_sheet,iplEndStatement,0,10,exea,60)
                
                insert_lead_off_out_percentage(cursor, new_sheet, iplEndStatement, 0, 11, exea, 65)
                
                insert_overall_strike_percentage(cursor, new_sheet, iplEndStatement, 0, 12, exea, 60)
                
                insert_baa_with_2_strikes(cursor, new_sheet, iplEndStatement, 0, 13, exea, 0.15)
                
                insert_advantage_counts_percentage(cursor, new_sheet, iplEndStatement, 0, 14, exea)
                
                insert_disadvantage_counts_percentage(cursor, new_sheet, iplEndStatement, 0, 15, exea)
                                   
                insert_strikeout_percentage(cursor, new_sheet, iplEndStatement, 0, 16, exea)
                
                insert_ground_ball_out_percentage(cursor, new_sheet, iplEndStatement, 0, 17, exea)
                
                insert_fly_ball_out_percentage(cursor, new_sheet, iplEndStatement, 0, 18, exea)
                 
                insert_baa_bip(cursor, new_sheet, iplEndStatement, 0, 19, exea)
                
                insert_at_bat_win_rate(cursor, new_sheet, iplEndStatement, 0, 20, exea)
                
                insert_pitch_spread_percentage(cursor, new_sheet, iplEndStatement, 0, 21, exea)
                
                insert_pitch_spread_strike_percentage(cursor, new_sheet, iplEndStatement, 0, 22, exea)
                
                insert_pitch_spread_whiff_percentage(cursor, new_sheet, iplEndStatement, 0, 23, exea)
                        
                    
                ################################## Team Totals ############################################# 
                
                exea=(datea,oppo)
                iplEndStatement="WHERE date = %s AND opponent = %s AND pitch_id <> '0' "
                  
                # Calculate and insert team totals
                team_totals_row = pitchers + 4  # Assuming a gap of one row between individual pitchers and team totals

                new_sheet.cell(row=team_totals_row, column=1, value="Team Totals")
                
                ##### Total Pitch Count
                new_sheet.cell(row=team_totals_row, column=2, value=total_pitch_count)
                
                ##### Average Pitches Per Inning
                if total_innings!=0:
                    new_sheet.cell(row=team_totals_row, column=3, value=round(total_pitch_count/total_innings,2))
                else:
                    new_sheet.cell(row=team_totals_row, column=3, value=0)
                
                #####  Average Peak Velocity
                if pitchers!=0:
                    new_sheet.cell(row=team_totals_row, column=4, value=round(total_peak_velo/pitchers,2))
                else:
                    new_sheet.cell(row=team_totals_row, column=4, value=0)
                    
                
                insert_1st_pitch_strike_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 5, exea, 60)
                
                insert_off_speed_strike_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 6, exea, 50)
              
                insert_swing_and_miss_percentage(cursor, new_sheet,iplEndStatement, team_totals_row, 7, exea, 25)
                     
                insert_velo_range(cursor, new_sheet, iplEndStatement, team_totals_row, 8, exea,False,False,False)   
                        
                insert_chases(cursor, new_sheet, iplEndStatement, team_totals_row, 9, exea)
                
                insert_ahead_after_3_pitches_percentage(cursor,new_sheet,iplEndStatement,team_totals_row,10,exea,60)
                
                insert_lead_off_out_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 11, exea, 65)
                
                insert_overall_strike_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 12, exea, 60)
                
                insert_baa_with_2_strikes(cursor, new_sheet, iplEndStatement, team_totals_row, 13, exea, 0.15)
                
                insert_advantage_counts_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 14, exea)
                
                insert_disadvantage_counts_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 15, exea)
                                   
                insert_strikeout_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 16, exea)
                
                insert_ground_ball_out_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 17, exea)
                
                insert_fly_ball_out_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 18, exea)
                 
                insert_baa_bip(cursor, new_sheet, iplEndStatement, team_totals_row, 19, exea) 
                
                insert_at_bat_win_rate(cursor, new_sheet, iplEndStatement, team_totals_row, 20, exea)
                
                insert_pitch_spread_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 21, exea)
                
                insert_pitch_spread_strike_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 22, exea)
                
                insert_pitch_spread_whiff_percentage(cursor, new_sheet, iplEndStatement, team_totals_row, 23, exea)
                  
                bold_first_column_if_threshold(new_sheet, 5)
                
                adjust_formating(new_sheet, team_totals_row)
                
                
            savebook(workbook, file_path, "Game Log Updated")



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
            print ("Welcome to Pitching Log Creator. ")
            today = input("Enter today's date (PUT IT IN MM-DD-YYYY form): ")
        
            update = input("Would you like to update pitchers log, season log, game log, or all logs? (X to stop): ")
        
            while (update!='X'):
            
                print("")
                
                #update pitchers log
                if (update=='pitchers'):
                    up_pitchers_log(cursora,today,"Pitcher_Logs_2024_A.xlsx")
                
                #update season log
                if (update =='season'):
                    up_season_log(cursora,today,"Season_Logs_2024_A.xlsx")
                    
                #update game log
                if (update =='game'):
                    up_game_log(cursora,today,"Game_Logs_2024_A.xlsx")
                
                #update all logs
                if (update =='all'):
                    up_pitchers_log(cursora,today,"Pitcher_Logs_2024_A.xlsx")
                    up_season_log(cursora,today,"Season_Logs_2024_A.xlsx")
                    up_game_log(cursora,today,"Game_Logs_2024_A.xlsx")
                    update='X'
                    
                if update not in ("pitchers","season","game","all","X"):
                    print("Invalid Entry")
                    
                print("")
                
                if (update!='X'):
                    update = input("Would you like to update game log, season log, pitchers log, or all logs? (X to stop): ")
                    if (update=='X'):
                        print("")
                
        
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
            print("Connection closed. GO MUTHAAFUCKIN LIONS!!!!")

if __name__ == "__main__":
    main()