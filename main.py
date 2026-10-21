PLAYERS_FILE = "players.txt"
INNINGS_FILE = "innings.txt"
PLAYERS_HEADER = "PlayerID|Name|Team|Role"
INNINGS_HEADER = "PlayerID|MatchNo|Runs|Balls|Out(Y/N)|Overs|RunsConceded|Wickets"
ROLES = ["Batter", "Bowler", "All-rounder", "Wicketkeeper"]


# ---------------------------------------------------------------
# FILE HANDLING
# ---------------------------------------------------------------
def make_file_if_missing(filename, header):
    # If the file does not exist, create it with just the header line.
    try:
        file = open(filename, "r")
        file.close()
    except FileNotFoundError:
        file = open(filename, "w")
        file.write(header + "\n")
        file.close()


def load_players():
    # Each player is a list: [id, name, team, role]
    players = []
    file = open(PLAYERS_FILE, "r")
    for line in file:
        line = line.strip()
        if line == "":
            continue
        parts = line.split("|")
        if len(parts) != 4:
            continue
        if parts[0] == "PlayerID":
            continue
        players.append(parts)
    file.close()
    return players


def load_innings():
    # Each innings is a list:
    # [id, match, runs, balls, out, overs_text, conceded, wickets]
    innings = []
    file = open(INNINGS_FILE, "r")
    for line in file:
        line = line.strip()
        if line == "":
            continue
        parts = line.split("|")
        if len(parts) != 8:
            continue
        if parts[0] == "PlayerID":
            continue
        try:
            row = [parts[0], int(parts[1]), int(parts[2]), int(parts[3]),
                   parts[4], parts[5], int(parts[6]), int(parts[7])]
        except ValueError:
            continue
        innings.append(row)
    file.close()
    return innings


def save_players(players):
    file = open(PLAYERS_FILE, "w")
    file.write(PLAYERS_HEADER + "\n")
    for p in players:
        file.write(p[0] + "|" + p[1] + "|" + p[2] + "|" + p[3] + "\n")
    file.close()


def save_innings(innings):
    file = open(INNINGS_FILE, "w")
    file.write(INNINGS_HEADER + "\n")
    for r in innings:
        line = (r[0] + "|" + str(r[1]) + "|" + str(r[2]) + "|" + str(r[3]) + "|"
                + r[4] + "|" + r[5] + "|" + str(r[6]) + "|" + str(r[7]))
        file.write(line + "\n")
    file.close()


# ---------------------------------------------------------------
# INPUT HELPERS
# ---------------------------------------------------------------
def ask_text(prompt, label):
    while True:
        text = input(prompt).strip()
        if text == "":
            print(label + " cannot be empty.")
        elif "|" in text:
            print(label + " cannot contain the | character.")
        else:
            return text


def ask_role():
    while True:
        text = input("Enter role (Batter / Bowler / All-rounder / Wicketkeeper): ").strip().lower()
        for role in ROLES:
            if text == role.lower():
                return role
        print("Invalid role. Please choose one of the four roles shown.")


def ask_int(prompt, low, high):
    # Keeps asking until the user types a whole number between low and high.
    while True:
        text = input(prompt).strip()
        if not text.isdigit():
            print("Please enter a whole number (0 or more, no letters or signs).")
        else:
            number = int(text)
            if number < low or number > high:
                print("Number must be between " + str(low) + " and " + str(high) + ".")
            else:
                return number


def ask_yes_no(prompt):
    # Returns "Y" or "N" (accepts lowercase too).
    while True:
        text = input(prompt).strip().upper()
        if text == "Y" or text == "N":
            return text
        print("Please enter Y or N.")


def find_player(players, player_id):
    for p in players:
        if p[0] == player_id:
            return p
    return None


# ---------------------------------------------------------------
# CRICKET CALCULATIONS
# ---------------------------------------------------------------
def overs_to_balls(text):
    # "3.4" -> 3*6 + 4 = 22 balls. Returns -1 if the text is not valid.
    text = text.strip()
    if text == "":
        return -1
    if "." in text:
        pieces = text.split(".")
        if len(pieces) != 2:
            return -1
        whole = pieces[0]
        part = pieces[1]
    else:
        whole = text
        part = "0"
    if not whole.isdigit() or not part.isdigit():
        return -1
    if int(part) > 5:               # 3.6 is not a legal cricket over value
        return -1
    return int(whole) * 6 + int(part)


def balls_to_overs_text(balls):
    # 22 balls -> "3.4"
    return str(balls // 6) + "." + str(balls % 6)


def batting_average(runs, times_out):
    if times_out == 0:
        return "N/A"
    return "{:.2f}".format(runs / times_out)


def strike_rate(runs, balls):
    if balls == 0:
        return "N/A"
    return "{:.2f}".format(runs / balls * 100)


def economy(runs_conceded, balls_bowled):
    if balls_bowled == 0:
        return "N/A"
    return "{:.2f}".format(runs_conceded * 6 / balls_bowled)


def get_stats(player_id, innings):
    # Collects every statistic for one player from the innings list.
    s = {"matches": 0, "runs": 0, "balls": 0, "outs": 0, "highest": 0,
         "fifties": 0, "hundreds": 0, "wickets": 0, "bowl_balls": 0,
         "conceded": 0, "best_w": -1, "best_r": 0}
    for r in innings:
        if r[0] != player_id:
            continue
        runs = r[2]
        balls = r[3]
        bowled = overs_to_balls(r[5])
        if bowled < 0:
            bowled = 0                      # bad data in file: treat as not bowled
        s["matches"] += 1
        s["runs"] += runs
        s["balls"] += balls
        if r[4] == "Y":
            s["outs"] += 1
        if runs > s["highest"]:
            s["highest"] = runs
        if runs >= 100:
            s["hundreds"] += 1
        elif runs >= 50:
            s["fifties"] += 1
        s["wickets"] += r[7]
        s["bowl_balls"] += bowled
        s["conceded"] += r[6]
        if bowled > 0:
            # best = most wickets; if tied, fewest runs conceded
            if r[7] > s["best_w"] or (r[7] == s["best_w"] and r[6] < s["best_r"]):
                s["best_w"] = r[7]
                s["best_r"] = r[6]
    return s


# ---------------------------------------------------------------
# FEATURE 1: ADD PLAYER
# ---------------------------------------------------------------
def add_player(players):
    print("--- Add Player ---")
    while True:
        player_id = ask_text("Enter Player ID (e.g. PL11): ", "Player ID").upper()
        if " " in player_id:
            print("Player ID cannot contain spaces.")
        elif find_player(players, player_id) != None:
            print("That Player ID already exists. Please use a different one.")
        else:
            break
    name = ask_text("Enter name: ", "Name")
    team = ask_text("Enter team: ", "Team")
    role = ask_role()

    players.append([player_id, name, team, role])
    save_players(players)
    print("Player " + player_id + " (" + name + ") added and saved.")


# ---------------------------------------------------------------
# FEATURE 2: RECORD MATCH PERFORMANCE
# ---------------------------------------------------------------
def record_performance(players, innings):
    print("--- Record Match Performance ---")
    player_id = input("Enter Player ID: ").strip().upper()
    player = find_player(players, player_id)
    if player == None:
        print("No player found with ID " + player_id + ". Add the player first.")
        return
    print("Player: " + player[1] + " (" + player[2] + ")")

    match_no = ask_int("Enter match number: ", 1, 999)
    for r in innings:
        if r[0] == player_id and r[1] == match_no:
            print("A record for " + player_id + " in match " + str(match_no) + " already exists.")
            return

    # Batting: balls must be above 0 if any runs were scored
    while True:
        runs = ask_int("Runs scored: ", 0, 500)
        balls = ask_int("Balls faced: ", 0, 1000)
        if balls == 0 and runs > 0:
            print("Runs cannot be scored off 0 balls. Please enter both again.")
        else:
            break
    out = ask_yes_no("Out? (Y/N): ")

    # Bowling: if no overs were bowled, runs conceded and wickets must be 0
    while True:
        while True:
            overs_text = input("Overs bowled (e.g. 3.4 = 3 overs 4 balls, 0 if none): ").strip()
            bowled = overs_to_balls(overs_text)
            if bowled < 0:
                print("Invalid overs. Use a number like 4 or 3.4 (the part after the dot must be 0-5).")
            elif bowled > 600:
                print("Overs are too high (maximum 100).")
            else:
                break
        conceded = ask_int("Runs conceded: ", 0, 1000)
        wickets = ask_int("Wickets taken (0-10): ", 0, 10)
        if bowled == 0 and (conceded > 0 or wickets > 0):
            print("With 0 overs bowled, runs conceded and wickets must be 0. Please enter again.")
        else:
            break

    innings.append([player_id, match_no, runs, balls, out, overs_text, conceded, wickets])
    save_innings(innings)
    print("Match " + str(match_no) + " record saved for " + player[1] + ".")


# ---------------------------------------------------------------
# FEATURE 6: PLAYER PROFILE
# ---------------------------------------------------------------
def view_profile(players, innings):
    print("--- Player Profile ---")
    player_id = input("Enter Player ID: ").strip().upper()
    player = find_player(players, player_id)
    if player == None:
        print("No player found with ID " + player_id + ".")
        return
    s = get_stats(player_id, innings)

    print("")
    print("Player ID      : " + player[0])
    print("Name           : " + player[1])
    print("Team           : " + player[2])
    print("Role           : " + player[3])
    print("Matches        : " + str(s["matches"]))
    if s["matches"] == 0:
        print("No match records yet for this player.")
        return
    print("Total runs     : " + str(s["runs"]))
    print("Highest score  : " + str(s["highest"]))
    print("50s            : " + str(s["fifties"]))
    print("100s           : " + str(s["hundreds"]))
    print("Batting average: " + batting_average(s["runs"], s["outs"]))
    print("Strike rate    : " + strike_rate(s["runs"], s["balls"]))
    print("Total wickets  : " + str(s["wickets"]))
    if s["best_w"] == -1:
        print("Best bowling   : N/A")
    else:
        print("Best bowling   : " + str(s["best_w"]) + "/" + str(s["best_r"]))
    print("Overs bowled   : " + balls_to_overs_text(s["bowl_balls"]))
    print("Economy        : " + economy(s["conceded"], s["bowl_balls"]))


# ---------------------------------------------------------------
# FEATURE 7: RANKINGS AND TEAM TOTALS
# ---------------------------------------------------------------
def sort_rows(rows):
    # Selection sort. Each row is [id, name, team, value].
    # Highest value first; if values are equal, the smaller ID comes first.
    for i in range(len(rows)):
        best = i
        for j in range(i + 1, len(rows)):
            if rows[j][3] > rows[best][3]:
                best = j
            elif rows[j][3] == rows[best][3] and rows[j][0] < rows[best][0]:
                best = j
        temp = rows[i]
        rows[i] = rows[best]
        rows[best] = temp


def show_top5(players, innings, stat_key, title, column):
    rows = []
    for p in players:
        s = get_stats(p[0], innings)
        rows.append([p[0], p[1], p[2], s[stat_key]])
    sort_rows(rows)

    print("--- " + title + " ---")
    if len(rows) == 0:
        print("No players yet.")
        return
    print("Rank  ID    " + "Name".ljust(14) + "Team".ljust(14) + column)
    count = 5
    if len(rows) < 5:
        count = len(rows)
    for i in range(count):
        r = rows[i]
        print(str(i + 1).ljust(6) + r[0].ljust(6) + r[1].ljust(14) + r[2].ljust(14) + str(r[3]))


def show_team_totals(players, innings):
    print("--- Team Totals ---")
    if len(players) == 0:
        print("No players yet.")
        return
    teams = []
    for p in players:
        if p[2] not in teams:
            teams.append(p[2])
    print("Team".ljust(16) + "Players".ljust(9) + "Runs".ljust(8) + "Wickets")
    for team in teams:
        count = 0
        total_runs = 0
        total_wickets = 0
        for p in players:
            if p[2] == team:
                s = get_stats(p[0], innings)
                count += 1
                total_runs += s["runs"]
                total_wickets += s["wickets"]
        print(team.ljust(16) + str(count).ljust(9) + str(total_runs).ljust(8) + str(total_wickets))


# ---------------------------------------------------------------
# MENU
# ---------------------------------------------------------------
def show_menu():
    print("================================")
    print("   CRICKET PLAYER STATISTICS")
    print("================================")
    print("1. Add Player")
    print("2. Record Match Performance")
    print("3. View Player Profile")
    print("4. Top 5 Run Scorers")
    print("5. Top 5 Wicket Takers")
    print("6. Team Totals")
    print("7. Exit")


def main():
    make_file_if_missing(PLAYERS_FILE, PLAYERS_HEADER)
    make_file_if_missing(INNINGS_FILE, INNINGS_HEADER)
    players = load_players()
    innings = load_innings()

    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ").strip()
        if choice == "1":
            add_player(players)
        elif choice == "2":
            record_performance(players, innings)
        elif choice == "3":
            view_profile(players, innings)
        elif choice == "4":
            show_top5(players, innings, "runs", "Top 5 Run Scorers", "Runs")
        elif choice == "5":
            show_top5(players, innings, "wickets", "Top 5 Wicket Takers", "Wickets")
        elif choice == "6":
            show_team_totals(players, innings)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")
        print()


main()