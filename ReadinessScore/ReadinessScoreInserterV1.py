# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 17:59:26 2024

@author: Bennett Stice
"""

import psycopg2

def create_test_log_table(cursor):
    test_log_table_creator = """
        CREATE TABLE IF NOT EXISTS test_log_T(
            Test_id SERIAL PRIMARY KEY,
            Fname VARCHAR(255),
            Lname VARCHAR(255),
            Test_Type VARCHAR(255),
            Score INT,
            Date VARCHAR(255)
        );
    """
    cursor.execute(test_log_table_creator)
    
def create_test_maxes_mins_score_table(cursor):
    test_max_min_score_table_creator = """
        CREATE TABLE IF NOT EXISTS test_max_min_score_T(
            Fname VARCHAR(255),
            Lname VARCHAR(255),
            FOUR_FINGER_MAX INT,
            FOUR_FINGER_MIN INT,
            PINKY_RING_MAX INT,
            PINKY_RING_MIN INT,
            FORCE_PLATE_MAX INT,
            FORCE_PLATE_MIN INT,
            EXTERNAL_ROTATION_FORCE_MAX INT,
            EXTERNAL_ROTATION_FORCE_MIN INT,
            EXTERNAL_ROTATION_ROM_MAX INT,
            EXTERNAL_ROTATION_ROM_MIN INT,
            INTERNAL_ROTATION_ROM_MAX INT,
            INTERNAL_ROTATION_ROM_MIN INT,
            LAT_ROM_MAX INT,
            LAT_ROM_MIN INT,
            FOREARM_CAT_SCORE INT,
            FOREARM_LAST_UP VARCHAR(255),
            LEGS_CAT_SCORE INT,
            LEGS_LAST_UP VARCHAR(255),
            SHOULDER_CAT_SCORE INT,
            SHOULDER_LAST_UP VARCHAR(255),
            ROM_CAT_SCORE INT,
            ROM_LAST_UP VARCHAR(255),
            TOTAL_SCORE INT,
            PRIMARY KEY (Fname, Lname)
        );
    """
    
    cursor.execute(test_max_min_score_table_creator)
    
def check_max_min_test(val, cursor, firstname, lastname, column):
    # Construct the query to retrieve maximum and minimum values
    query = f"SELECT {column}_MAX AS max_val, {column}_MIN AS min_val FROM test_max_min_score_T "
    query += "WHERE Fname = %s AND Lname = %s"
    cursor.execute(query, (firstname, lastname))
    data = cursor.fetchone()

    if data:
        max_val =int(data[0])
        min_val =int(data[1])

        # Update the maximum value if necessary
        if max_val is None or max_val < int(val):
            update_max_query = f"UPDATE test_max_min_score_T SET {column}_MAX = %s WHERE Fname = %s AND Lname = %s"
            cursor.execute(update_max_query, (val, firstname, lastname))

        # Update the minimum value if necessary
        if min_val is None or min_val > int(val):
            update_min_query = f"UPDATE test_max_min_score_T SET {column}_MIN = %s WHERE Fname = %s AND Lname = %s"
            cursor.execute(update_min_query, (val, firstname, lastname))

        # Commit the changes
        cursor.connection.commit()
    else:
        print("No data found for the given firstname and lastname.")


def updateScoreDate(updateDate, cat, cursorb, cat_score, scorea, first,last):
    updateQuery = "UPDATE test_max_min_score_T SET {} = %s, {} = %s WHERE Fname = %s AND Lname = %s"
    updateQuery = updateQuery.format(cat, cat_score)
    cursorb.execute(updateQuery, (updateDate, scorea,first,last))
    cursorb.connection.commit()
    
def updateTotalScore(scoreb,first,last,cursorc):
    updateQuery = "UPDATE test_max_min_score_T SET total_score = %s WHERE Fname = %s AND Lname = %s"
    cursorc.execute(updateQuery, (scoreb,first,last))
    cursorc.connection.commit()
    
    
def get_max_test_id(cursor):
    test_id_setter = "SELECT max(Test_id) FROM test_log_T;"
    cursor.execute(test_id_setter)
    result = cursor.fetchone()
    return result[0] + 1 if result[0] is not None else 1   

def main():
    try:
        connection = psycopg2.connect(
            dbname=#,
            user=#,
            password=#,
            host=#,
            port=#
        )

        with connection.cursor() as cursor:
            print(f"Opened database successfully: {connection.dsn}")

            create_test_log_table(cursor)
            test_id = get_max_test_id(cursor)
            create_test_maxes_mins_score_table(cursor)
            connection.commit()
            
            date = input("Enter today's date (PUT IT IN MM-DD-YYYY form): ")
            
            fname, lname = input("Enter the first and last name of the pitcher: ").split()

            go = True

            while go:
                test_type=input("Enter the Type of Test (Enter 'X' to stop): ")
                
                if test_type=="X":
                    break
                if test_type not in("FOUR FINGER PULL","PINKY RING PULL","FORCE PLATE JUMP","EXTERNAL ROTATION FORCE","EXTERNAL ROTATION ROM","INTERNAL ROTATION ROM","LAT ROM"):
                    print("Test Options are FOUR FINGER PULL, PINKY RING PULL, FORCE PLATE JUMP, EXTERNAL ROTATION FORCE, EXTERNAL ROTATION ROM, INTERNAL ROTATION ROM, or LAT ROM")
                    continue
                
                score=input("Enter the reading: ")
            
                test_log_inserter = """
                INSERT INTO test_log_T (Test_ID, Fname, Lname,Test_Type,Score, Date)
                VALUES (%s, %s, %s, %s, %s, %s);
                """

                cursor.execute(test_log_inserter, (test_id, fname, lname, test_type,score,date))
                connection.commit()
                
                test_id+=1
                
                if (test_type=="FOUR FINGER PULL"):
                    check_max_min_test(score,cursor,fname,lname,"FOUR_FINGER")
                
                if (test_type=="PINKY RING PULL"):
                    check_max_min_test(score,cursor,fname,lname,"PINKY_RING")
                 
                if (test_type=="FORCE PLATE JUMP"):
                    check_max_min_test(score,cursor,fname,lname,"FORCE_PLATE")
                 
                if (test_type=="EXTERNAL ROTATION FORCE"):
                    check_max_min_test(score,cursor,fname,lname,"EXTERNAL_ROTATION_FORCE")
                
                if (test_type=="EXTERNAL ROTATION ROM"):
                    check_max_min_test(score,cursor,fname,lname,"EXTERNAL_ROTATION_ROM")
                
                if (test_type=="INTERNAL ROTATION ROM"):
                    check_max_min_test(score,cursor,fname,lname,"INTERNAL_ROTATION_ROM")
                    
                if (test_type=="LAT ROM"):
                    check_max_min_test(score,cursor,fname,lname,"LAT_ROM")
            
                
                genQuery = "SELECT Max(test_id) FROM test_log_T WHERE Fname = %s AND Lname = %s AND test_type = "
   
                
 ####################### Forearm Category #####################################  
    
                fourFingerQuery=genQuery +  "'FOUR FINGER PULL'"
                fourFingerMaxMinQuery = "SELECT FOUR_FINGER_MAX AS max_val, FOUR_FINGER_MIN AS min_val "
                fourFingerMaxMinQuery += "FROM test_max_min_score_T WHERE Fname = %s AND Lname = %s"
                
                cursor.execute(fourFingerQuery,(fname,lname))
                data = cursor.fetchone()
                
                test_num = data[0]
                scoreGettingQuery = "SELECT score FROM test_log_T WHERE test_id = %s"
                cursor.execute(scoreGettingQuery,(test_num,))
                data = cursor.fetchone()
                
                Reading =int(data[0])
                
                
                cursor.execute(fourFingerMaxMinQuery,(fname,lname))
                data=cursor.fetchone()
                
                Maxb =int(data[0])
                Minb =int(data[1])
                
                if (Maxb-Minb!=0):
                    fourFingerScore= (Reading-Minb)/(Maxb-Minb) *100
                else:
                    fourFingerScore= 100
                
                pinkyRingQuery = genQuery + "'PINKY RING PULL'"
                pinkyRingMaxMinQuery = "SELECT PINKY_RING_MAX AS max_val, PINKY_RING_MIN AS min_val "
                pinkyRingMaxMinQuery += "FROM test_max_min_score_T WHERE Fname = %s AND Lname = %s"


                cursor.execute(pinkyRingQuery, (fname, lname))
                data = cursor.fetchone()

                test_num = data[0]
                scoreGettingQuery = "SELECT score FROM test_log_T WHERE test_id = %s"
                cursor.execute(scoreGettingQuery,(test_num,))
                data = cursor.fetchone()
                
                Reading =int(data[0])

                cursor.execute(pinkyRingMaxMinQuery, (fname, lname))
                data = cursor.fetchone()


                Maxb =int(data[0])
                Minb =int(data[1])


                if Maxb - Minb != 0:
                    pinkyRingScore = (Reading - Minb) / (Maxb - Minb) * 100
                else:
                    pinkyRingScore = 100
                
                
                ForeArmCatScore = (fourFingerScore+pinkyRingScore)/2
                
                print("The Forearm Category Score is ",round(ForeArmCatScore))
                
                updateScoreDate(date,"forearm_last_up",cursor,"forearm_cat_score", ForeArmCatScore,fname,lname)

 ####################### Legs Category #####################################  

                forceJumpQuery=genQuery +  "'FORCE PLATE JUMP'"
                forceJumpMaxMinQuery = "SELECT FORCE_PLATE_MAX AS max_val, FORCE_PLATE_MIN AS min_val "
                forceJumpMaxMinQuery += "FROM test_max_min_score_T WHERE Fname = %s AND Lname = %s"
                
                cursor.execute(forceJumpQuery,(fname,lname))
                data = cursor.fetchone()
                
                test_num = data[0]
                scoreGettingQuery = "SELECT score FROM test_log_T WHERE test_id = %s"
                cursor.execute(scoreGettingQuery,(test_num,))
                data = cursor.fetchone()
                
                Reading =int(data[0])
                                
                cursor.execute(forceJumpMaxMinQuery,(fname,lname))
                data=cursor.fetchone()
                
                Maxb =int(data[0])
                Minb =int(data[1])
                
                if (Maxb-Minb!=0):
                    forceJumpScore= (Reading-Minb)/(Maxb-Minb) *100
                else:
                    forceJumpScore= 100  
                
                LegsCatScore=forceJumpScore
                
                print("The Legs Category Score is ",round(LegsCatScore))
                
                updateScoreDate(date,"legs_last_up",cursor,"legs_cat_score", LegsCatScore,fname,lname)

 ####################### Shoulder Category #####################################                      
                    
                ERForceQuery=genQuery +  "'EXTERNAL ROTATION FORCE'"
                ERForceMaxMinQuery = "SELECT EXTERNAL_ROTATION_FORCE_MAX AS max_val, EXTERNAL_ROTATION_FORCE_MIN AS min_val "
                ERForceMaxMinQuery += "FROM test_max_min_score_T WHERE Fname = %s AND Lname = %s"
                
                cursor.execute(ERForceQuery,(fname,lname))
                data = cursor.fetchone()
                
                test_num = data[0]
                scoreGettingQuery = "SELECT score FROM test_log_T WHERE test_id = %s"
                cursor.execute(scoreGettingQuery,(test_num,))
                data = cursor.fetchone()
                
                Reading =int(data[0])
                                
                cursor.execute(ERForceMaxMinQuery,(fname,lname))
                data=cursor.fetchone()
                
                Maxb =int(data[0])
                Minb =int(data[1])
                
                if (Maxb-Minb!=0):
                    ERForceScore= (Reading-Minb)/(Maxb-Minb) *100
                else:
                    ERForceScore= 100  
                
                ShoulderCatScore=ERForceScore
                
                print("The Shoulder Category Score is ",round(ShoulderCatScore))
                
                updateScoreDate(date,"shoulder_last_up",cursor,"shoulder_cat_score", ShoulderCatScore,fname,lname)
                
 ####################### Range of Motion Category #####################################               
                
                ERROMQuery=genQuery +  "'EXTERNAL ROTATION ROM'"
                ERROMMaxMinQuery = "SELECT EXTERNAL_ROTATION_ROM_MAX AS max_val, EXTERNAL_ROTATION_ROM_MIN AS min_val "
                ERROMMaxMinQuery += "FROM test_max_min_score_T WHERE Fname = %s AND Lname = %s"
                
                cursor.execute(ERROMQuery,(fname,lname))
                data = cursor.fetchone()
                
                test_num = data[0]
                scoreGettingQuery = "SELECT score FROM test_log_T WHERE test_id = %s"
                cursor.execute(scoreGettingQuery,(test_num,))
                data = cursor.fetchone()
                
                Reading =int(data[0])
                                
                cursor.execute(ERROMMaxMinQuery,(fname,lname))
                data=cursor.fetchone()
                
                Maxb =int(data[0])
                Minb =int(data[1])
                
                if (Maxb-Minb!=0):
                    ERROMScore= (Reading-Minb)/(Maxb-Minb) *100
                else:
                    ERROMScore= 100  
                    
                IRROMQuery=genQuery +  "'INTERNAL ROTATION ROM'"
                IRROMMaxMinQuery = "SELECT INTERNAL_ROTATION_ROM_MAX AS max_val, INTERNAL_ROTATION_ROM_MIN AS min_val "
                IRROMMaxMinQuery += "FROM test_max_min_score_T WHERE Fname = %s AND Lname = %s"
                
                cursor.execute(IRROMQuery,(fname,lname))
                data = cursor.fetchone()
                
                test_num = data[0]
                scoreGettingQuery = "SELECT score FROM test_log_T WHERE test_id = %s"
                cursor.execute(scoreGettingQuery,(test_num,))
                data = cursor.fetchone()
                
                Reading =int(data[0])
                                
                cursor.execute(IRROMMaxMinQuery,(fname,lname))
                data=cursor.fetchone()
                
                Maxb =int(data[0])
                Minb =int(data[1])
                
                if (Maxb-Minb!=0):
                    IRROMScore= (Reading-Minb)/(Maxb-Minb) *100
                else:
                    IRROMScore= 100  
                    
                IRROMQuery=genQuery +  "'INTERNAL ROTATION ROM'"
                IRROMMaxMinQuery = "SELECT INTERNAL_ROTATION_ROM_MAX AS max_val, INTERNAL_ROTATION_ROM_MIN AS min_val "
                IRROMMaxMinQuery += "FROM test_max_min_score_T WHERE Fname = %s AND Lname = %s"
                
                cursor.execute(IRROMQuery,(fname,lname))
                data = cursor.fetchone()
                
                test_num = data[0]
                scoreGettingQuery = "SELECT score FROM test_log_T WHERE test_id = %s"
                cursor.execute(scoreGettingQuery,(test_num,))
                data = cursor.fetchone()
                
                Reading =int(data[0])
                                
                cursor.execute(IRROMMaxMinQuery,(fname,lname))
                data=cursor.fetchone()
                
                Maxb =int(data[0])
                Minb =int(data[1])
                
                if (Maxb-Minb!=0):
                    IRROMScore= (Reading-Minb)/(Maxb-Minb) *100
                else:
                    IRROMScore= 100 
                
                LatROMQuery=genQuery +  "'LAT ROM'"
                LatROMMaxMinQuery = "SELECT LAT_ROM_MAX AS max_val, LAT_ROM_MIN AS min_val "
                LatROMMaxMinQuery += "FROM test_max_min_score_T WHERE Fname = %s AND Lname = %s"
                
                cursor.execute(LatROMQuery,(fname,lname))
                data = cursor.fetchone()
                
                test_num = data[0]
                scoreGettingQuery = "SELECT score FROM test_log_T WHERE test_id = %s"
                cursor.execute(scoreGettingQuery,(test_num,))
                data = cursor.fetchone()
                
                Reading =int(data[0])
                                
                cursor.execute(LatROMMaxMinQuery,(fname,lname))
                data=cursor.fetchone()
                
                Maxb =int(data[0])
                Minb =int(data[1])
                
                if (Maxb-Minb!=0):
                    LatROMScore= (Reading-Minb)/(Maxb-Minb) *100
                else:
                    LatROMScore= 100 
                    
                ROMCatScore = (ERROMScore+IRROMScore+LatROMScore)/3
                
                print("The Range of Motion Category Score is ",round(ROMCatScore))
                
                updateScoreDate(date,"rom_last_up",cursor,"rom_cat_score", ROMCatScore,fname,lname)
            
            
                TotalScore = (ForeArmCatScore+LegsCatScore+ShoulderCatScore+ROMCatScore)/4
                
                
                print("The Total Readiness Score is ",TotalScore)
                
                updateTotalScore(TotalScore,fname,lname,cursor)
            
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
            print("Connection closed.")

if __name__ == "__main__":
    main()