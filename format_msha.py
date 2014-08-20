import datetime
import random

import numpy as np
import pandas as pd


def force_to_ascii(narrative):
    narrative = unicode(narrative, 'latin-1')
    try:
        narrative = unicode.encode(narrative, 'ascii')
    except:
        print narrative
        narrative = unicode.encode(narrative, 'ascii', errors='replace')
        print narrative
    return narrative


def get_df():
    filename = r'\\ocspapps1\FINAL_OSH\Autocoding\Autocoding Class\Accidents.txt'
    df = pd.read_table(filename, sep='|', parse_dates=['ACCIDENT_DT'])
    earliest_date = datetime.date(2010, 1, 1)
    df = df[df.ACCIDENT_DT >= earliest_date]
    df = df[['MINE_ID', 'FIPS_STATE_CD', 'ACCIDENT_DT', 'INJ_BODY_PART_CD', 'INJ_BODY_PART', 'NARRATIVE']]
    df['NARRATIVE'] = df['NARRATIVE'].apply(force_to_ascii)
    df = df[df.INJ_BODY_PART_CD != '?']
    rows = df.to_dict(outtype='records')
    random.shuffle(rows)
    df = pd.DataFrame(rows)
    return df


def get_df4():
    """ Get dataframe for class 4 assignment """
    filename = r'\\ocspapps1\FINAL_OSH\Autocoding\Autocoding Class\Accidents.txt'
    df = pd.read_table(filename, sep='|', parse_dates=['ACCIDENT_DT'])
    earliest_date = datetime.date(2010, 1, 1)
    df = df[df.ACCIDENT_DT >= earliest_date]
    df = df[['DAYS_LOST', 'DEGREE_INJURY', 'NATURE_INJURY_CD', 'NATURE_INJURY', 'NARRATIVE']]
    df['NARRATIVE'] = df['NARRATIVE'].apply(force_to_ascii)
    df = df[df.NATURE_INJURY_CD != '?']
    rows = df.to_dict(outtype='records')
    random.shuffle(rows)
    df = pd.DataFrame(rows)
    return df


def export(df):
    # export
    df.to_csv('msha.csv', index=False)
    df.to_csv('msha.txt', index=False, sep='\t')
    df.to_excel('msha.xlsx', index=False)
    return df


def read_df(df):
    # read
    df = pd.read_excel('msha.xlsx')
    df = pd.read_csv('msha.txt')
    return df
