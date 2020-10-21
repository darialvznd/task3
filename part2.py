import pandas as pd
import re
import locale
from datetime import datetime
from collections import Counter
import numpy as np

def modify_date(x):
    x = re.sub(r'\s', ' ', x)
    x = x.split(' ', 3)
    if (x[1] != 'мая'):
      x[1] = x[1][:3]
    else:
        x[1] = 'май'
    return datetime.strptime(' '.join(x), "%d %b %Y")

def compare_dates(date):
    current_date = datetime.now()
    diff =  current_date - date
    return diff.days


groups_count = 10
pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

df = pd.read_csv('C:/python/task3/pycoder/data.csv')

df['max_salary'] = df['max_salary'].fillna(0)
df['min_salary'] = df['min_salary'].fillna(0)
# print(df[:10])
#Двойная сортировка вакансий
print(df['company'].count())
df_sorted = df.sort_values(['max_salary', 'min_salary'])
# print(df_sorted [:10])
x = df['company'].count() // groups_count
df_array = []
rest_df = df_sorted
##Разделить отсортированный датасет на 10 групп по значению максимальной зарплаты.
for i in range(groups_count-1):
    df_array.append(rest_df.head(x))
    rest_df =  rest_df.tail(len(rest_df) - x)
    # print(rest_df['name'].count())
df_array.append(rest_df)

for i in range(groups_count):
    print(df_array[i])

##Все возможные названия вакансий и количество вхождений каждой из них в группу;
for i in range(groups_count):
    print("DF" + str(i))
    print(df_array[i].groupby('name')['name'].nunique())

##среднее, максимальное и минимальное количество дней, на протяжении которых размещена вакансия на сайте (от даты парсинга);
days_since= []
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
for i in range(groups_count): 
    print("Группа " + str(i))
    df_array[i]['publish_date'] = df_array[i]['publish_date'].apply(modify_date)
    df_array[i]['publish_date'] = pd.to_datetime(df_array[i]['publish_date'])
    #apply this function to your pandas dataframe
    days_since.append(df_array[i]['publish_date'].apply(compare_dates))
    print("Среднее: ", days_since[i].mean())
    print("Максимальное: ", days_since[i].max())
    print("Минимальное: ", days_since[i].min())

##все возможные значения требуемого опыта работы и количество вхождений каждого из них в группу;  
for i in range(groups_count):
    print("DF" + str(i))
    print(df_array[i].groupby('experience')['experience'].nunique())


##все возможные значения типов занятости и количество вхождений каждого из них в группу;
for i in range(groups_count):
    print("DF" + str(i))
    print(df_array[i].groupby('employment_mode')['employment_mode'].nunique())

#все возможные значения рабочего графика и количество вхождений каждого из них в группу;
for i in range(groups_count):
    print("DF" + str(i))
    print(df_array[i].groupby('schedule')['schedule'].nunique())

#набор уникальных ключевых навыков и количество вхождений каждого навыка в группу.
for i in range(groups_count):
    print("DF" + str(i))
    df_array[i]['skills'] = df_array[i]['skills'].fillna('')
    count  = pd.Series(df_array[i]['skills'].str.replace('[\[\]\']','').str.split(';').map(Counter).sum())
    print(count)




