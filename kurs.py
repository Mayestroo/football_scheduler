import random
import tkinter as tk
from tkinter import ttk, Toplevel
from tabulate import tabulate

teams = ["Arsenal", "Aston Villa", "Brentford", "Brighton", "Burnley", "Chelsea", "Crystal Palace",
         "Everton", "Leeds United", "Leicester City", "Liverpool", "Manchester City", "Manchester United",
         "Newcastle United", "Norwich City", "Southampton", "Tottenham Hotspur", "Watford", "West Ham United",
         "Wolverhampton Wanderers"]

# Generate the matchday schedule
matchday_schedule = []
for matchday in range(1, 39):
    matches = []
    schedule_teams = teams.copy()
    random.shuffle(schedule_teams)
    for i in range(0, len(schedule_teams), 2):
        home_team = schedule_teams[i]
        away_team = schedule_teams[i + 1]
        home_score = random.randint(0, 5)
        away_score = random.randint(0, 5)
        matches.append([home_team, home_score, "-", away_score, away_team])
    matchday_schedule.append(matches)

# Generate the tournament table
def generate_table(matchday_schedule, round_number):
    table = []
    for team in teams:
        played = wins = losses = draws = scores_for = scores_against = goal_difference = 0
        for matchday in matchday_schedule[:round_number]:
            for match in matchday:
                home_team, home_score, _, away_score, away_team = match
                if home_team == team:
                    played += 1
                    scores_for += home_score
                    scores_against += away_score
                    goal_difference += home_score - away_score
                    if home_score > away_score:
                        wins += 1
                    elif home_score < away_score:
                        losses += 1
                    else:
                        draws += 1
                elif away_team == team:
                    played += 1
                    scores_for += away_score
                    scores_against += home_score
                    goal_difference += away_score - home_score
                    if away_score > home_score:
                        wins += 1
                    elif away_score < home_score:
                        losses += 1
                    else:
                        draws += 1
        points = wins * 3 + draws
        table.append([team, played, wins, losses, draws, scores_for, scores_against, goal_difference, points])

    # Sort the table based on points and goal difference
    table.sort(key=lambda x: (x[8], x[7]), reverse=True)
    return table

# Function to display the matchday schedule
def display_matchday_schedule(round_number, matchday_schedule):
    if round_number < 1 or round_number > len(matchday_schedule):
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Invalid round number.")
        return
    result_text.delete(1.0, tk.END)
    for i in range(round_number):
        result_text.insert(tk.END, f"Matchday {i+1}\n")
        result_text.insert(tk.END, tabulate(matchday_schedule[i], headers=["Home Team", "", "", "", "Away Team"], tablefmt="fancy_grid"))
        result_text.insert(tk.END, "\n\n")

# Function to display the tournament table
def display_tournament_table(table, round_number):
    headers = ["№", "Team", "G", "W", "L", "D", "SF", "SA", "GD", "P"]
    table_with_rank = [[i + 1] + row for i, row in enumerate(table)]
    table_window = Toplevel(window)
    table_window.title("Tournament Table")
    table_text = tk.Text(table_window, height=45, width=90)
    table_text.pack(padx=10, pady=10)
    table_text.insert(tk.END, f"Tournament Table (Round {round_number})\n")
    table_text.insert(tk.END, tabulate(table_with_rank, headers=headers, tablefmt="fancy_grid"))

# Event handler for the submit button
def submit_round(event=None):  # Modified to accept an event argument
    round_number = int(round_entry.get())
    if round_number >= 1 and round_number <= 38:
        display_matchday_schedule(round_number, matchday_schedule)
        if round_number >= 3:
            table = generate_table(matchday_schedule, round_number)
            display_tournament_table(table, round_number)
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Invalid round number.")

# Create the Tkinter application window
window = tk.Tk()
window.title("Premier League Tournament")

# Create and position GUI elements
label = ttk.Label(window, text="Round Number:")
label.grid(row=0, column=0)

round_entry = ttk.Entry(window)
round_entry.grid(row=0, column=1)

submit_button = ttk.Button(window, text="Submit", command=submit_round)
submit_button.grid(row=0, column=2)

# Create a scrollbar
scrollbar = ttk.Scrollbar(window)
scrollbar.grid(row=1, column=3, sticky="NS")

result_text = tk.Text(window, height=30, width=70, yscrollcommand=scrollbar.set)
result_text.grid(row=1, column=0, columnspan=3, padx=10)

# Configure the scrollbar to scroll the result_text
scrollbar.configure(command=result_text.yview)

# Bind the <Return> event to the submit_round function
window.bind('<Return>', submit_round)

# Run the GUI event loop
window.mainloop()
