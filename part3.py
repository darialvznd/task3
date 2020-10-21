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
    diff =  current_date - modify_date(date)
    return diff.days



pd.set_option('display.max_rows', 400)
#pd.set_option('display.max_columns', None)

df = pd.read_csv('C:/python/task3/pycoder/data.csv')

df['max_salary'] = df['max_salary'].fillna(0)
df['min_salary'] = df['min_salary'].fillna(0)
# print(df[:10])
#Двойная сортировка вакансий

df_name = df.groupby('name')


print(df_name.first())


# все возможные значения максимальной и минимальной зарплаты и количество вхождений каждой из них в группу;
for name, group in df_name: 
    print(name) 
    print(group.groupby('max_salary')['max_salary'].nunique())  
    print(group.groupby('min_salary')['min_salary'].nunique())
    print() 

##среднее, максимальное и минимальное количество дней, на протяжении которых размещена вакансия на сайте (от даты парсинга);
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
for name, group in df_name: 
    days_since= []
    print(name)
    days_since.append(group['publish_date'].apply(compare_dates))
    print("Среднее: ",sum(days_since) / len(days_since))
    print("Максимальное: ", max(days_since))
    print("Минимальное: ", min(days_since))

# ##все возможные значения требуемого опыта работы и количество вхождений каждого из них в группу;  
for name, group in df_name: 
    print(name) 
    print(group.groupby('experience')['experience'].nunique())  
    print() 


# ##все возможные значения типов занятости и количество вхождений каждого из них в группу;
for name, group in df_name: 
    print(name) 
    print(group.groupby('employment_mode')['employment_mode'].nunique())  
    print() 


##все возможные значения рабочего графика и количество вхождений каждого из них в группу;
for name, group in df_name: 
    print(name) 
    print(group.groupby('schedule')['schedule'].nunique())  
    print()


##набор уникальных ключевых навыков и количество вхождений каждого навыка в группу.
for name, group in df_name: 
    print(name)
    group['skills'] = group['skills'].fillna('') 
    for i in group['skills']:
        skills = []
        skills.extend(i.replace('[\[\]\']','').split(';'))
    for i in range(len(skills)):
        print(skills[i], skills[i].count(skills[i]))
        
  
