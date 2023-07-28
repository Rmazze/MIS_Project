""" imports and path """

# imports
import pandas as pd

# file path
path = "questionnarie.csv"

""" data preparation """

# import the .csv file in a DataFrame
# columns from 17 to 26 are SUS answers in our csv file, change them as needed
data = pd.read_csv(path, sep = ",", header=None, usecols=[17,18,19,20,21,22,23,24,25,26])    

# convert columns to lists
q1 = data[17].tolist()
q2 = data[18].tolist()
q3 = data[19].tolist()
q4 = data[20].tolist()
q5 = data[21].tolist()
q6 = data[22].tolist()
q7 = data[23].tolist()
q8 = data[24].tolist()
q9 = data[25].tolist()
q10 = data[26].tolist()


""" odd answers calculation """

# odd list
odd_list = [q1, q3, q5, q7, q9]
odd_count = 0
for column in odd_list:
    for i in column:
        # for every odd answer: answer - 1
        res = i - 1
        odd_count = odd_count + res


""" even answers calculation """      

# even list
even_list = [q2, q4, q6, q8, q10]
even_count = 0
for column in even_list:
    for i in column:
        # for every even answer: 5 - answer
        res = 5 - i
        even_count = even_count + res



""" compute average SUS score """   

# total sus score
sus_score = (odd_count + even_count)*2.5

# number of users
number_users = len(data.index)

# average sus score
sus_score = sus_score/number_users
print(sus_score)