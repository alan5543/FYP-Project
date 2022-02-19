# Build the TimeLine for Tweets

import pandas as pd
from datetime import datetime, timedelta
pd.options.mode.chained_assignment = None

from datetime import timedelta

def roundTime(time):
    roundTo = 30*60
    dt = time.to_pydatetime()
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    result =  dt + timedelta(0,rounding-seconds,-dt.microsecond)
    return result

def hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +timedelta(hours=t.minute//30))

def timeline_builder(tweets_table):
    temp = tweets_table
    # round off the time
    # temp['Release'] = temp["Release"].apply(hour_rounder)
    temp['Release'] = temp["Release"].apply(roundTime)
    # sorting the time
    temp.sort_values(by=['Release'])
    # extract the timeline variable
    time_variable = temp[['Release', 'Polarity', 'Neg', 'Pos']]
    # timeline groupby
    timeline = time_variable.groupby("Release").mean().reset_index()
    return timeline


def dataframe_to_time_lst(time_table):
    res = []
    for index, row in time_table.iterrows():
        item = {}
        item['Release'] = str(row['Release'])
        item['Polarity'] = row['Polarity']
        item['Neg'] = row['Neg']
        item['Pos'] = row['Pos']
        res.append(item)

    return res