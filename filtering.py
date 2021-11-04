import pandas as pd
import numpy as np
from datetime import datetime, date
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

def from_dob_to_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def preprocessUserData(user_data):
    processed_data = []
    
    #interest
    if (user_data[1] == 'education'):
        processed_data.append('1')
    elif (user_data[1] == 'travel'):
        processed_data.append('2')
    elif (user_data[1] == 'entertainment'):
        processed_data.append('3')
    else:
        processed_data.append('0')
    
    #occupation
    if (user_data[2] == 'student'):
        processed_data.append('1')
    elif (user_data[2] == 'employed'):
        processed_data.append('2')
    elif (user_data[2] == 'unemployed'):
        processed_data.append('3')
    else:
        processed_data.append('0')
    
    #birthdate
    _age = pd.to_datetime(user_data[3])
    processed_data.append(from_dob_to_age(_age))
        
    #follow_count
    processed_data.append(user_data[4])
    
    #latitude
    processed_data.append(user_data[5])
    
    #longitude
    processed_data.append(user_data[6])
    
    return processed_data

def filter(data):
    # reading the CSV file
    df = pd.read_csv('data/data.csv')
    df2 = df.copy()

    df['interest'] = df['interest'].map({
        'education':'1',
        'travel':'2',
        'entertainment':'3',
        'technology':'4',
        'health and fitness':'5',
        'science and nature':'6',
        'other/everything':'7',
        np.nan:'0'},
        na_action=None)

    df['occupation'] = df['occupation'].map({
        'student':'1',
        'employed':'2',
        'unemployed':'3',
        np.nan:'0'},
        na_action=None)
    
    df['birthdate'] = pd.to_datetime(df.birthdate)
    df['birthdate'] = df['birthdate'].apply(lambda x: from_dob_to_age(x))

    df1 = df[['interest', 'occupation', 'birthdate', 'follow_count', 'latitude', 'longitude']]

    new_data = np.array(data)

    sim_results = []

    for x in df1.index:
        cosine = cosine_similarity(normalize([new_data]), normalize([df1.iloc[x].values]))
        sim_results.append(cosine)

    df2['similarity'] = sim_results
    
    id_results = []

    #get 5 top user with highest similarities
    for index, item in df2.sort_values(by='similarity', ascending=False).iloc[:5].iterrows():
        id_results.append(item['uid'])
    
    return id_results