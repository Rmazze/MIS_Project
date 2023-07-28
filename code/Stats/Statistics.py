"""------- Imports and global variables -------"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display
import os
from scipy import stats

path = "/Users/laura/Downloads/final_results.csv"      # path where the .csv is located
save_path = "/Users/laura/Documents/UniTN/SecondYear/MultisensoryInteractiveSystems/Project/Results"        # path where the results are saved



"""------- Creation of the needed folder for the results -------"""
if not(os.path.exists(save_path)):
    os.mkdir(save_path)



"""------- Functions -------"""
"""
Function that given the reaction time for a stimulus computes:
- the mean
- the minimum value
- the maximum value
and stores them in a DataFrame.

:param rts: reaction time array
:param st: considered stimulus
:return stat: DataFrame containig the computed statistics
"""
def computeStat(rts, st, stat):
    s = pd.DataFrame({"stimulus": [st], "mean_value": [np.round(np.mean(rts), decimals = 3)], "max_value": [np.amax(rts)], "min_value": [np.amin(rts)], "n": [int(rts.shape[1])]})
    stat = stat.append(s, ignore_index = True)
    return stat


"""
Function that given the catch yes/no for a stimulus computes:
- the total number of catches
- the percentage of catching
and stores them in a DataFrame.

:param cs: catch yes/no array
:param st: considered stimulus
:return stat: DataFrame containig the computed statistics
"""
def computeStatC(cs, st, stat):
    s = pd.DataFrame({"stimulus": [st], "n_catches": [np.sum(cs, axis = 0)], "percentage": [np.round((np.sum(cs, axis = 0)/len(cs))*100, decimals = 2)]})
    stat = stat.append(s, ignore_index = True)
    return stat


"""
Function to save a DataFrame as a .png table.
"""
def render_table(data, col_width = 3.0, row_height = 0.625, font_size = 14, header_color = '#345c72', row_colors = ['#f1f1f2', 'w'], edge_color = 'w', bbox = [0, 0, 1, 1], header_columns = 0, ax = None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')
    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in mpl_table._cells.items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax.get_figure(), ax



"""------- Imports of data -------"""
data = pd.read_csv(path, sep = ";", header = 0)     # Import the .csv file in a DataFrame



"""------- Catched reaction time statistics -------"""
# Extract the reaction time for each stimilus (VAT, VAt, VaT, Vat, vA1t, vA2t, vAT, vaT).
# For each stimulus extract the mean, the minimum and the maximum reaction time.
# Plot the boxplot.
# Do the ANOVA test.
stat = pd.DataFrame(columns = ["stimulus", "mean_value", "max_value", "min_value"])     # DataFrame that will contain the statistics
stimuli = ["VAT", "VAt", "VaT", "Vat", "vAt", "vAT", "vaT"]     # array of possible stimuli
for item in stimuli:
    # Extraction of the reaction time for the given stimulus
    rt = np.transpose((data[(data["C_Visual"] == int(item[0].isupper())) & (data["C_Auditory"] == int(item[1].isupper())) & (data["C_Tactile"] == int(item[2].isupper())) & (data["Catch"] == 1)].loc[:, ["ReactionTime"]]).to_numpy(dtype = "float", copy = True))
    
    # Computation of the statistics
    stat = computeStat(rt, item, stat)

    # Save the reaction time in an array
    if item == "VAT":
        rt_VAT = rt
    elif item == "VAt":
        rt_VAt = rt
    elif item == "VaT":
        rt_VaT = rt
    elif item == "Vat":
        rt_Vat = rt
    elif item == "vAt":
        rt_vAt = rt
    elif item == "vAT":
        rt_vAT  = rt
    else:
        rt_vaT = rt

# Extraction of the reaction time for the stimulus "vA2t"
rt = np.transpose((data[(data["C_Visual"] == 0) & (data["C_Auditory"] == 2) & (data["C_Tactile"] == 0) & (data["Catch"] == 1)].loc[:, ["ReactionTime"]]).to_numpy(dtype = "float", copy = True))

# Computation of the statistics for the stimulus "vA2t"
stat = computeStat(rt, "vA2t", stat)

# Save the reaction time of the stimulus vA2t in the specific array
rt_VA2t = rt

# Save the table of the statistics as a .png image
fig, ax = render_table(stat, header_columns=0, col_width=2.0)
fig.savefig(os.path.join(save_path, "table_stat_rtCatch.png"))

# Create the boxplots
fig = plt.figure()
plt.boxplot([np.transpose(rt_VAT).flatten(), np.transpose(rt_VAt).flatten(), np.transpose(rt_VaT).flatten(), np.transpose(rt_Vat).flatten(), np.transpose(rt_vAt).flatten(), np.transpose(rt_vAT).flatten(), np.transpose(rt_vaT).flatten(), np.transpose(rt_VA2t).flatten()])
plt.xlabel("Stimuli")
plt.ylabel("Reaction time")
plt.title("Reaction time at ball catched for different stimuli")
plt.xticks([1,2,3,4,5,6,7,8], ["VAT", "VAt", "VaT", "Vat", "vA1t", "vAT", "vaT", "vA2t"])
plt.savefig(os.path.join(save_path, "rt_Catch_boxplot.png"))

# One-way ANOVA test
F, pvalue = stats.f_oneway(rt_VAT.flatten(), rt_VAt.flatten(), rt_VaT.flatten(), rt_Vat.flatten(), rt_vAt.flatten(), rt_vAT.flatten(), rt_vaT.flatten(), rt_VA2t.flatten())
print("\n\nFor the reaction time at catched ball, the F statistic is: ", F, "and the associated p-value is: ", pvalue, "\n\n")



"""------- Nearly catched reaction time statistics -------"""
stat = pd.DataFrame(columns = ["stimulus", "mean_value", "max_value", "min_value", "n"])     # DataFrame that will contain the statistics
stimuli = ["VAT", "VAt", "VaT", "Vat", "vAt", "vAT", "vaT"]     # array of possible stimuli
for item in stimuli:
    # Extraction of the reaction time for the given stimulus
    rt = np.transpose((data[(data["C_Visual"] == int(item[0].isupper())) & (data["C_Auditory"] == int(item[1].isupper())) & (data["C_Tactile"] == int(item[2].isupper())) & (data["Catch"] == 0.5)].loc[:, ["ReactionTime"]]).to_numpy(dtype = "float", copy = True))
    
    # Computation of the statistics
    stat = computeStat(rt, item, stat)

    # Save the reaction time in an array
    if item == "VAT":
        rt_VAT = rt
    elif item == "VAt":
        rt_VAt = rt
    elif item == "VaT":
        rt_VaT = rt
    elif item == "Vat":
        rt_Vat = rt
    elif item == "vAt":
        rt_vAt = rt
    elif item == "vAT":
        rt_vAT  = rt
    else:
        rt_vaT = rt

# Extraction of the reaction time for the stimulus "vA2t"
rt = np.transpose((data[(data["C_Visual"] == 0) & (data["C_Auditory"] == 2) & (data["C_Tactile"] == 0) & (data["Catch"] == 1)].loc[:, ["ReactionTime"]]).to_numpy(dtype = "float", copy = True))

# Computation of the statistics for the stimulus "vA2t"
stat = computeStat(rt, "vA2t", stat)

# Save the reaction time of the stimulus vA2t in the specific array
rt_VA2t = rt

# Save the table of the statistics as a .png image
fig, ax = render_table(stat, header_columns=0, col_width=2.0)
fig.savefig(os.path.join(save_path, "table_stat_rtNearlyCatch.png"))

# Create the boxplots
fig = plt.figure()
plt.boxplot([np.transpose(rt_VAT).flatten(), np.transpose(rt_VAt).flatten(), np.transpose(rt_VaT).flatten(), np.transpose(rt_Vat).flatten(), np.transpose(rt_vAt).flatten(), np.transpose(rt_vAT).flatten(), np.transpose(rt_vaT).flatten(), np.transpose(rt_VA2t).flatten()])
plt.xlabel("Stimuli")
plt.ylabel("Reaction time")
plt.title("Reaction time at ball nearly catched for different stimuli")
plt.xticks([1,2,3,4,5,6,7,8], ["VAT", "VAt", "VaT", "Vat", "vA1t", "vAT", "vaT", "vA2t"])
plt.savefig(os.path.join(save_path, "rt_NearlyCatch_boxplot.png"))

# One-way ANOVA test
F, pvalue = stats.f_oneway(rt_VAT.flatten(), rt_VAt.flatten(), rt_VaT.flatten(), rt_Vat.flatten(), rt_vAt.flatten(), rt_vAT.flatten(), rt_vaT.flatten(), rt_VA2t.flatten())
print("\n\nFor the reaction time at nearly catched ball, the F statistic is: ", F, "and the associated p-value is: ", pvalue, "\n\n")



"""------- Number of catches for each stimuli -------"""
stat = pd.DataFrame(columns = ["stimulus", "n_catches", "percentage"])     # DataFrame that will contain the statistics
stimuli = ["VAT", "VAt", "VaT", "Vat", "vAt", "vAT", "vaT"]     # array of possible stimuli
for item in stimuli:
    # Extraction of the catch yes/no for the given stimulus
    c = np.transpose((data[(data["C_Visual"] == int(item[0].isupper())) & (data["C_Auditory"] == int(item[1].isupper())) & (data["C_Tactile"] == int(item[2].isupper()))].loc[:, ["Catch"]]).to_numpy(dtype = "int", copy = True)).flatten()
    
    # Computation of the statistics
    stat = computeStatC(c, item, stat)

# Extraction of the catch yes/no for the stimulus "vA2t"
c = np.transpose((data[(data["C_Visual"] == 0) & (data["C_Auditory"] == 2) & (data["C_Tactile"] == 0)].loc[:, ["Catch"]]).to_numpy(dtype = "float", copy = True)).flatten()

# Computation of the statistics for the stimulus "vA2t"
stat = computeStatC(c, "vA2t", stat)

# Save the table of the statistics as a .png image
fig, ax = render_table(stat, header_columns=0, col_width=2.0)
fig.savefig(os.path.join(save_path, "table_stat_catch.png"))



"""------- A1 prior A2? -------"""
username_list = data["Username"]       # extract the usernames
unique_username_list = list(dict.fromkeys(username_list))   # only once
first_A1 = 0    # counter for the time that A1 occurs before A2
first_A2 = 0    # counter for the time that A2 occurs before A1
mean_pos_A1 = 0     # mean position of A1
mean_pos_A2 = 0     # mean position of A2

for i in unique_username_list:
    found_A = False     # boolean that keeps track when the first audio stimulus is found
    idx = data.index[data["Username"] == i].to_list()[0]    # extract the starting row index of each user
    stop = idx + 8      # compute the end row index of each user
    while idx < stop:
        line_trial = () # tuple containing the stimuli of each row of the user
        line_trial = line_trial + (data.iloc[idx]["C_Visual"], )
        line_trial = line_trial + (data.iloc[idx]["C_Auditory"], )
        line_trial = line_trial + (data.iloc[idx]["C_Tactile"], )

        # A1 found
        if line_trial == (0, 1, 0):
            mean_pos_A1 = mean_pos_A1 + (idx % 8) + 1
            if found_A == False:
                found_A = True
                first_A1 = first_A1 + 1

        # A2 found
        if line_trial == (0, 2, 0):
            mean_pos_A2 = mean_pos_A2 + (idx % 8) + 1
            found_A = True

        idx = idx + 1

mean_pos_A1 = mean_pos_A1 / len(unique_username_list)      # compute the mean
mean_pos_A2 = mean_pos_A2 / len(unique_username_list)      # compute the mean
first_A2 = len(unique_username_list) - first_A1

print("A1 prior A2: ", first_A1, " times")
print("A2 prior A1: ", first_A2, " times")
print("Media position A1: ", mean_pos_A1, " over ", print(len(unique_username_list)))
print("Media posizione A2: ", mean_pos_A2, " over ", print(len(unique_username_list)))