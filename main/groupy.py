import csv
import pandas as pd
import numpy as np
from functools import reduce
import time

def return_csv_details(file):
    # check for a valid file
    if not file.lower().endswith(('.csv')):
        return False

    # create a dataframe from the csv file
    df = pd.read_csv(file)

    # make a list of current headers
    header_list = list(df)

    # make sure there are no more than 10 attributes
    if len(header_list) >= 12:
        return False

    return header_list[1:]

def generate_teams(file, team_size, iterations, weightings):
        
    # create a dataframe from the csv file
    df = pd.read_csv(file)

    # make a list of current headers
    header_list = list(df) 

    # get the number of teams according to the required team size
    df_size = df.shape[0]
    NUM_TEAMS = df_size / team_size
    NUM_TEAMS = round(NUM_TEAMS)

    # check for too few students
    if NUM_TEAMS <= 1:
        return False

    if len(header_list) == 1:
        # randomise all rows for starting solution
        df = df.sample(frac=1).reset_index()
        final_variance_dict = {}
        table_list = []

        # df index is split evenly, each iteration assigns group number according to row indices
        for idx,val in enumerate(np.array_split(df.index, NUM_TEAMS)):
            df.loc[val,'teams'] = idx+1
        df.teams = df.teams.astype(int)
        
        results_dict = {
            'df': df,
            'final_variance_dict': final_variance_dict,
            'table_list': table_list,
        }

        return results_dict

    # get the first student from the dataframe
    first_entry = df.values[0]

    # rename first column header
    df.rename(columns={ df.columns[0]: "id" }, inplace=True)

    # rename all other columns
    counter = 1
    for i in header_list[1:]:
        df.rename(columns={ df.columns[counter]: "v" + str(counter)}, inplace=True)
        counter += 1

    # make a list of new headers
    new_header_list = list(df)

    # function for allocating scores to each student according to attributes
    def calculate_score(name):
        # score each student according to values given
        value_score_list = []

        # make a list of all the values in column
        value_list = list(df[name])

        if str(value_list[0]).isdigit():
            min_attribute = min(value_list)
            max_attribute = max(value_list)

            for i in value_list:
                try:
                    i_normalised = (i - min_attribute) / (max_attribute - min_attribute)
                    value_score_list.append(i_normalised)
                except ZeroDivisionError:
                    value_score_list.append(1)
        else:
            attribute_count = []
            for i in value_list:
                attribute_count.append(value_list.count(i))
            min_attribute = min(attribute_count)
            max_attribute = max(attribute_count)

            # make a list of all the scores for each value in the column
            for i in value_list:
                i_frequency = value_list.count(i)

                try:
                    i_normalised = (i_frequency - min_attribute) / (max_attribute - min_attribute)
                    value_score_list.append(i_normalised)
                except ZeroDivisionError:
                    value_score_list.append(1)
        return value_score_list

    final_scores_list = []

    for i in new_header_list[1:]:
        final_scores_list.append(calculate_score(i))

    final_scores = [sum(values) for values in zip(*final_scores_list)]

    df['score'] = final_scores

    # Sort dataframe in score order
    df = df.sort_values('score', ascending=False)

     # make a list of the overall score for each student
    final_scores_list = []

    for i in new_header_list[1:]:
        final_scores_list.append(calculate_score(i))

    final_scores = [sum(values) for values in zip(*final_scores_list)]

    df['score'] = final_scores

    # Sort dataframe in score order
    df = df.sort_values('score', ascending=False)

    # make a list of team names
    team_value_list = []
    counter = 1
    direction = 'up'
    for i in range(df_size):
        if direction == 'up':
            team_value_list.append(counter)
            counter += 1
            if counter == (NUM_TEAMS + 1):
                direction = 'down'
        else:
            counter -= 1
            team_value_list.append(counter)
            if counter == 1:
                direction = 'up'

    df['teams'] = team_value_list

    # sort dataframe in team order
    df = df.sort_values('teams')

    # get the first score for the starting fitness score
    var_first_score_list = []

    # function get variance score from column
    def get_first_variance(name, colno):
        if str(first_entry[colno]).isdigit():
            var = df.groupby('teams').mean()[name].var() / 100 * int(weightings[colno - 1])
            var_first_score_list.append(var)
        else:
            # get a list of unique values in column
            values = df[name].unique()
            for i in values:
                var = (df[df[name] == i].groupby('teams')[name].count()/df.groupby('teams')[name].count()).var() * int(weightings[colno - 1])
                var_first_score_list.append(var)

    counter = 1
    for i in new_header_list[1:]:
        get_first_variance(i,counter)
        counter += 1

    # starting score
    # 'nan' treated as 0
    var_best = np.nansum(var_first_score_list)

    # list of best scores for graph
    var_best_list = []

    # start the algorithm
    iteration = 0

    for i in range(iterations):
        iteration += 1

        var_best_list.append(var_best)
        # dataframe is grouped by 'groups' and each group is sampled once and rows are stored in 'swop'
        swop = df.groupby('teams').apply(lambda x: x.sample(n=1))

        # dropping dataframe's multiindex
        swop.reset_index(level=0, drop=True, inplace=True)
        
        # randomise groups in swop
        swop.teams = np.random.permutation(swop.teams)

        # creating a copy of the dataframe to overwrite swopped rows
        df_test = df.copy()
        df_test.loc[swop.index,'teams'] = swop['teams']

        var_score_list = []

        # function get variance score from column
        def get_column_variance(name, colno):
            if str(first_entry[colno]).isdigit():
                var = df_test.groupby('teams').mean()[name].var() / 100 * int(weightings[colno - 1])
                var_score_list.append(var)
            else:
                # get a list of unique values in column
                values = df[name].unique()
                for i in values:
                    var = (df_test[df_test[name] == i].groupby('teams')[name].count()/df_test.groupby('teams')[name].count()).var() * int(weightings[colno - 1])
                    var_score_list.append(var)

        # call score function for each column
        counter = 1
        for i in new_header_list[1:]:
            get_column_variance(i,counter)
            counter += 1

        # add up all scores to get overall variance score PROBLEM?
        var = np.nansum(var_score_list)

        # check whether fitness function output is better than previous best
        if var < var_best:
            # overwrite best fitness function output
            var_best = var
            # overwrite dataframe with test dataframe
            df = df_test.copy()


    # Sort dataframe in group order
    df = df.sort_values('teams')

    # Remove score weightings from dataframe
    del df['score']

    # Rename headers back to original names
    header_list.append('Teams')
    df.columns = header_list

    # Make dictionary of attributes and final vars
    final_variance_dict = {}

    # function for getting final variance
    def get_final_variance(name,colno):
        if str(first_entry[colno]).isdigit():
            var = df.groupby('Teams').mean()[name].var() / 100
            final_variance_dict[name] = var
        else:
            # get a list of unique values in column
            values = df[name].unique()
            for i in values:
                var = (df[df[name] == i].groupby('Teams')[name].count()/df.groupby('Teams')[name].count()).var()
                final_variance_dict[i] = var

    counter = 1
    for i in header_list[1:-1]:
        get_final_variance(i,counter)
        counter += 1

    table_list  = []

    counter = 1
    for i in header_list[1:-1]:
        if str(first_entry[counter]).isdigit():
            table_list.append(df.groupby('Teams').describe()[i])
            counter += 1
        else:
            table_list.append(pd.crosstab(df[i], df.Teams))
            counter += 1



    results_dict = {
        'df': df,
        'final_variance_dict': final_variance_dict,
        'table_list': table_list,
    }

    return results_dict

