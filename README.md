1. Correlation Project
This is a grouping of 2 correlation projects I have done. One compares various fingers strength metrics we get from a flex pro grip device to pitch metrics like velocity, movement, spin rate, spin efficiency, etc. The other tries to find correlations between the weighted medball throws our team does in the offseason and the average/max fastball velocity.

2. GameCharter_ReportMaker
This is the team's old game charter and report system that I made last winter. It take's in 3 or 4 inputs (pitch type, velocity, pitch result, bip result if applicable) from the terminal and inputs values into an SQL table. The report maker then takes those values and creates reports that have statistics that our coaches wanted like first pitch strike percentage, off speed strike percentage, ahead after 3 pitches, etc. It also create visuals to track how the velocities of each pitch was changing as the season progressed. These reports were made for each game, each individual pitcher and the entire season combined.

3. Pitch Statistics Correlation
This looked at season statistics tracked above and if there was overlap among them. Like for example whiff percentage is highly correlated with baa among our team. Another example is percentage of pitcher's thrown ahead in the count naturally is negatively correlated with pitches per inning. 

4. ROAR_Website
This is pictures of a shiny app I created to house all the team's data from places like Rapsodo, Trackman, Vald, BlastMotion and create easy to understand visuals and tables for our players and coaches to see anywhere they are. Also it makes it possible for us to see videos from 4 or more different camera angles on every single pitch and swing from bullpens, batting practices, scrimmages, and in-season games. Another thing it does is replaces all of our coaches pen-and-paper charting systems with virtual charting systems that connect with an SQL database.

5. Stuff+ and Location+
This is my attempt at a stuff and location plus pitch grader. I used data from baseball savant. I used almost a million pitches from 2023 and 2024. The premise of my graders was to use metrics like velocity, movement, release point, and pitch location to predict estimated woba using speed angle using an xgboost model. This valued quantified soft contact and swings and misses which is what our team as a whole was chasing. 
