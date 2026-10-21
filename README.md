# 7376252AL125_P24
PROJECT P24 - CRICKET PLAYER STATISTICS
Register Number : 7376252AL125
Student Name    : GAYATHRI S 
Programme       : AIXcelerate General Programming
Repository      : 7376252AL125_P24
Language        : Python 3 (no imports, no external libraries)

1. PROJECT DESCRIPTION
----------------------
A terminal-based program that stores cricket players and their match
performances in plain text files, and calculates batting, bowling,
ranking and team statistics from that data.

2. FILES
--------
main.py        The complete program.
players.txt    Player records.
innings.txt    Match performance records.
README.txt     This file.
sample_run.txt Example terminal session.

3. HOW TO RUN
-------------
1. Install Python 3.
2. Put main.py, players.txt and innings.txt in the same folder.
3. Open a terminal in that folder and run:
       python main.py
   (On some systems use: python3 main.py)
4. Choose options 1-7 from the menu. Choose 7 to exit.
If players.txt or innings.txt is missing, the program creates it
with just the header line.

4. MENU
-------
1. Add Player                 - add a player with a unique ID
2. Record Match Performance   - save one innings for a player
3. View Player Profile        - show all statistics for one player
4. Top 5 Run Scorers          - ranking by total runs
5. Top 5 Wicket Takers        - ranking by total wickets
6. Team Totals                - players, runs and wickets per team
7. Exit

5. DATA FILE FORMATS (separator is |)
-------------------------------------
players.txt
    PlayerID|Name|Team|Role
    PL07|Arjun S|CSE Strikers|Batter
Roles allowed: Batter, Bowler, All-rounder, Wicketkeeper.

innings.txt
    PlayerID|MatchNo|Runs|Balls|Out(Y/N)|Overs|RunsConceded|Wickets
    PL07|3|64|48|Y|0|0|0

Each file has a header line. The program skips the header, blank
lines and badly formed lines when loading. After every successful
add or record, the whole file is rewritten, so data is still there
when the program is restarted.

6. FORMULAS USED
----------------
Batting average = total runs / number of times out
                  (N/A if the player was never out)
Strike rate     = total runs / total balls faced * 100
                  (N/A if no balls were faced)
Economy         = runs conceded * 6 / total balls bowled
                  (N/A if no balls were bowled)

Cricket overs: 3.4 means 3 overs and 4 balls = 3 x 6 + 4 = 22 balls.
Overs are never added as decimals. The program converts each innings
to balls, adds the balls, and only converts back to overs for display.
Example: 3.4 + 2.2 overs = 22 + 14 = 36 balls = 6.0 overs.
The part after the dot must be 0 to 5 (3.6 is rejected).

7. RULES AND ASSUMPTIONS
------------------------
- Player IDs are converted to capital letters (pl11 becomes PL11).
- Player IDs must be unique and cannot contain spaces.
- Names, teams and IDs cannot be empty or contain the | character.
- Roles can be typed in any capitalisation and are saved correctly.
- Matches = number of innings records for the player.
- A score of 50-99 counts as a 50; a score of 100 or more counts as
  a 100 (a 100 is not also counted as a 50).
- Highest score is the highest runs in any one innings.
- Best bowling = most wickets in one innings; if tied, fewest runs
  conceded. Shown as wickets/runs (for example 3/21).
- Only one record is allowed per player per match number.
- Runs cannot be scored off 0 balls.
- If 0 overs were bowled, runs conceded and wickets must be 0.
- Wickets in one innings: 0 to 10.
- Rankings with equal values are ordered by Player ID.

8. INPUT CHECKS
---------------
Whole-number inputs reject letters, negative numbers and empty text.
Out status accepts Y or N (upper or lower case).
Unknown player IDs are rejected when recording an innings or viewing
a profile.
A player with no innings shows "Matches: 0" and does not crash.

9. TEST CHECKLIST
-----------------
Expected results using the original sample data:
- Profile PL01: runs 106, average 106.00, strike rate 135.90
- Profile PL07: runs 133, highest 83, 50s 2, strike rate 152.87,
  wickets 1, best 1/20, overs 4.2, economy 8.31
- Top 5 runs: PL07 133, PL01 106, PL09 105, PL04 96, PL05 93
- Top 5 wickets: PL06 5, PL08 5, PL02 3, PL03 3, PL07 1
- Team runs: CSE Strikers 324, ECE Eagles 220, IT Warriors 198
- Overs 3.6 or abc: rejected
- Runs 10 with balls 0: rejected
- Duplicate player ID or duplicate player+match: rejected
- Restart the program: added data is still present

10. LIMITATIONS
---------------
- Data is held in memory while the program runs, and the files are
  rewritten after each change. Editing the .txt files by hand while
  the program is open is not supported.
- There is no option to edit or delete a record.
- Names with the | character are not allowed.
