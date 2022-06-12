import pandas as pd 
import numpy as np

data=pd.read_csv('C:/Users/Acer/Desktop/Python/crawler_pratice/104/data_analysis.csv')

#修正公司名稱
data.company=data.company.str.replace('\n','')

#刪除 人資、直播主 職位的row
hr=data[data['job_title'].str.contains(pat='人資')].index
live_host=data[data['job_title'].str.contains(pat='直播主')].index
data.drop(hr,inplace=True)
data.drop(live_host,inplace=True)

#因論件計酬無法估計 故刪除論件計酬的row
for_item=data[data['salary'].str.contains(pat='論件計酬')].index
data.drop(for_item,inplace=True)


#處理薪水；待遇面議法律規定需在4萬以上，因此設為4-6萬；部分工時人員每周不得超過40小時，因此一個月以160小時計算；日薪1個月以20日計算
#輔助列salary_asist
data.loc[data['salary'].str.contains(pat='月薪'),'salary_asist']=data.loc[data['salary'].str.contains(pat='月薪'),'salary'].\
    str.replace('元','').str.replace('月薪','').str.replace(',','')
data.loc[data['salary'].str.contains(pat='年薪'),'salary_asist']=data.loc[data['salary'].str.contains(pat='年薪'),'salary'].\
    str.replace('元','').str.replace('年薪','').str.replace(',','')
data.loc[data['salary'].str.contains(pat='時薪'),'salary_asist']=data.loc[data['salary'].str.contains(pat='時薪'),'salary'].\
    str.replace('元','').str.replace('時薪','')
data.loc[data['salary'].str.contains(pat='待遇面議'),'salary_asist']='40000~60000'
data.loc[data['salary'].str.contains(pat='日薪'),'salary_asist']=data.loc[data['salary'].str.contains(pat='日薪'),'salary'].\
    str.replace('元','').str.replace('日薪','').str.replace(',','')

#分割薪水成上、下界、平均值
#salary_h
data.loc[data['salary'].str.contains(pat='月薪'),'salary_h']=data.loc[data['salary'].str.contains(pat='月薪'),'salary_asist'].\
    map(lambda x:int(x[x.find('~')+1:]) if x.find('~')!=-1 else (int(x[0:x.find('以上')]) if x.find('以上')!=-1 else int(x)))
data.loc[data['salary'].str.contains(pat='年薪'),'salary_h']=data.loc[data['salary'].str.contains(pat='年薪'),'salary_asist'].\
    map(lambda x:int(x[x.find('~')+1:])/12 if x.find('~')!=-1 else int(x[0:x.find('以上')])/12)
data.loc[data['salary'].str.contains(pat='時薪'),'salary_h']=data.loc[data['salary'].str.contains(pat='時薪'),'salary_asist'].\
    map(lambda x:int(x[x.find('~')+1:])*160 if x.find('~')!=-1 else (int(x[0:x.find('以上')])*160 if x.find('以上')!=-1 else int(x)*160))
data.loc[data['salary'].str.contains(pat='待遇面議'),'salary_h']=40000
data.loc[data['salary'].str.contains(pat='日薪'),'salary_h']=data.loc[data['salary'].str.contains(pat='日薪'),'salary_asist'].\
    map(lambda x:int(x[x.find('~')+1:])*20 if x.find('~')!=-1 else (int(x[0:x.find('以上')])*20 if x.find('以上')!=-1 else int(x)*20))

#salary_l
data.loc[data['salary'].str.contains(pat='月薪'),'salary_l']=data.loc[data['salary'].str.contains(pat='月薪'),'salary_asist'].\
    map(lambda x:int(x[0:x.find('~')]) if x.find('~')!=-1 else (int(x[0:x.find('以上')]) if x.find('以上')!=-1 else int(x)))
data.loc[data['salary'].str.contains(pat='年薪'),'salary_l']=data.loc[data['salary'].str.contains(pat='年薪'),'salary_asist'].\
    map(lambda x:int(x[0:x.find('~')])/12 if x.find('~')!=-1 else int(x[0:x.find('以上')])/12)
data.loc[data['salary'].str.contains(pat='時薪'),'salary_l']=data.loc[data['salary'].str.contains(pat='時薪'),'salary_asist'].\
    map(lambda x:int(x[0:x.find('~')])*160 if x.find('~')!=-1 else (int(x[0:x.find('以上')])*160 if x.find('以上')!=-1 else int(x)*160))
data.loc[data['salary'].str.contains(pat='待遇面議'),'salary_l']=40000
data.loc[data['salary'].str.contains(pat='日薪'),'salary_l']=data.loc[data['salary'].str.contains(pat='日薪'),'salary_asist'].\
    map(lambda x:int(x[0:x.find('~')])*20 if x.find('~')!=-1 else (int(x[0:x.find('以上')])*20 if x.find('以上')!=-1 else int(x)*20))

#salary_a
data['salary_a']=(data['salary_h']+data['salary_l'])/2

print(data)
#print(data.groupby('working_Exp').working_Exp.count().to_dict())

data.to_csv('C:/Users/Acer/Desktop/Python/crawler_pratice/104/process_job_data_analysis.csv',index=False)