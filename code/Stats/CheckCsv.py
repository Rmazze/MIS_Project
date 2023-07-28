import pandas as pd

path = "final_results.csv"

"""------- Conversion to float of the "Catch" column -------"""
# Read the .csv file as a pandas dataframe
results = pd.read_csv(path, sep = ";", header = 0)

# Convert the "Catch" column from int to float
results = results.astype({"Catch": float})

# Save the pandas dataframe as .csv file
results.to_csv(path, sep = ";", index = False)

"""------- Check if every user has 8 trials -------"""
username_list = results["Username"] # extract the usernames
unique_username_list = list(dict.fromkeys(username_list)) # only once

for i in unique_username_list:
    count = results["Username"].value_counts()[i]
    if count != 8:
        print(i, "'s count is not correct")

"""------- Check for duplicate and missing stimuli -------"""
for i in unique_username_list:
    idx = results.index[results["Username"] == i].to_list()[0] # extract the starting row index of each user
    stop = idx + 8 # compute the end row index of each user
    trial_list = set(((0, 0, 1), (0, 1, 1), (1, 1, 1), (0, 1, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1), (0, 2, 0))) # set containing all the stimuli
    user_trials = set() # set containig the stimuli presented to each user
    while idx < stop:
        line_trial = () # tuple containing the stimuli of each row of the user
        line_trial = line_trial + (results.iloc[idx]["C_Visual"], )
        line_trial = line_trial + (results.iloc[idx]["C_Auditory"], )
        line_trial = line_trial + (results.iloc[idx]["C_Tactile"], )

        # Check for duplicates
        if line_trial in user_trials:
            print("For ", i, "duplicate stimulus: ", line_trial)
        else:
            user_trials.add(line_trial)
        idx = idx + 1

    # Check for missing stimuli
    missing_stimuli = trial_list - user_trials

    if len(missing_stimuli) > 0:
        print("For ", i, " missing stimuli: ", missing_stimuli)

"""------- Put 0 reaction time for 0.0 catch -------"""
for idx, row in results.iterrows():
    if row["Catch"] == 0.0:
        if not(row["ReactionTime"] == 0.0):
            results.at[idx, "ReactionTime"] = 0

results.to_csv(path, sep = ';', index = False, header = True)