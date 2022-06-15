import pandas as pd
import numpy as np
import datetime as dt
import us_abbrev
import matplotlib.pyplot as plt

dir = input('file directory: ')

df = pd.read_csv(dir)


# divide criteria by columns
df.crit_head = df.crit_head.str.split(',')
df.crit_text = df.crit_text.str.split(',')
# melt it down by the following columns' values
df = df.explode(['crit_head', 'crit_text'])
# convert crit_head values as columns and crit_text values as values
df = df.pivot_table(
    index=['title', 'company', 'location', 'date', 'detail'],
    columns='crit_head',
    values='crit_text',
    aggfunc=lambda x: ' '.join(x)
).reset_index().rename_axis(None, axis=1)
df_crit_columns = ['seniority level', 'employment type', 'job function', 'industries']


# divide dates
# convert to datetime type
df.date = pd.to_datetime(df.date, format='%Y%m%d')
# extract day, month, year, day of week
df['day'] = df.date.dt.day
df['month'] = df.date.dt.month
df['year'] = df.date.dt.year
df['day_of_week'] = df.date.dt.day_name()
df_time_columns = ['day', 'month', 'year', 'day_of_week']


# divide location
states = us_abbrev.us_state_to_abbrev
# split values into city and states
df[['city', 'state']] = df.location.str.split(',', expand=True)
# change values of rows with different format
df.state = np.where(df['state'].str.contains('united states'), df.city, df.state)
df.city = np.where(df['state'].str.contains('united states'), np.NaN, df.city)
# convert state names to abbreviation 
df.state = df.state.map(lambda x: states.get(x, x))
df_location_columns = ['city', 'state']


# job title
# extract job from job post title
dta_engi = df.title.str.contains(r'(?=.*data)(?=.*engineer)',regex=True)
dta_anal = df.title.str.contains(r'(?=.*data)(?=.*(analyst|analytic))',regex=True)
dta_scie = df.title.str.contains(r'(?=.*data)(?=.*(scientist|science))',regex=True)
dta_spec = df.title.str.contains(r'(?=.*data)(?=.*specialist)',regex=True)
ml_engi  = df.title.str.contains(r'(?=.*(machine))(?=.*(learning))(?=.*engineer)',regex=True)
# if condition match apply value
condition = [dta_engi, dta_anal, dta_scie, dta_spec, ml_engi]
value = ['data engineer','data analyst', 'data scientist', 'data specialist', 'ML engineer']
df['job'] = np.select(condition, value, np.NaN)


# description
# data science tools
df['python'] = np.where(df['detail'].str.contains('python'), 1, 0)
df['r'] = np.where(df['detail'].str.contains('\s+r\W'), 1, 0)
df['sql'] = np.where(df['detail'].str.contains('sql'), 1, 0)
df['java'] = np.where(df['detail'].str.contains('java\W'), 1, 0)
df['javascript'] = np.where(df['detail'].str.contains('javascript|js\W'), 1, 0)
df['matlab'] = np.where(df['detail'].str.contains('matlab'), 1, 0)
df['spss'] = np.where(df['detail'].str.contains('spss'), 1, 0)
df['sas'] = np.where(df['detail'].str.contains('sas\W'), 1, 0)
df['excel'] = np.where(df['detail'].str.contains('excel'), 1, 0)
df['tableau'] = np.where(df['detail'].str.contains('tableau'), 1, 0)
df['pwerbi'] = np.where(df['detail'].str.contains('power\sbi\W'), 1, 0)
df_tools_columns = ['python','r','java','javascript','matlab','spss','sas','excel','tableau','pwerbi']


# to csv file
var = ['company','job'] + df_location_columns + df_time_columns + df_crit_columns + df_tools_columns + ['detail']
today_date = dt.datetime.now().strftime('%y%m%d')
df[var].to_csv(f'linkedin_tidy_{today_date}.csv')