import pandas as pd 
import numpy as np

data=pd.read_csv('D:/資料20220523備份/數據分析相關/Python/crawler_pratice/104/data_analysis_0607.csv')

#修正公司名稱
data.company=data.company.str.replace('\n','')

#因論件計酬無法估計 故刪除論件計酬的row
for_item=data[data['salary'].str.contains(pat='論件計酬')].index
data.drop(for_item,inplace=True)


#處理薪水；部分工時人員每周不得超過40小時，因此一個月以160小時計算；日薪1個月以20日計算
#輔助列salary_asist
data.loc[data['salary'].str.contains(pat='月薪'),'salary_asist']=data.loc[data['salary'].str.contains(pat='月薪'),'salary'].\
    str.replace('元','').str.replace('月薪','').str.replace(',','')
data.loc[data['salary'].str.contains(pat='年薪'),'salary_asist']=data.loc[data['salary'].str.contains(pat='年薪'),'salary'].\
    str.replace('元','').str.replace('年薪','').str.replace(',','')
data.loc[data['salary'].str.contains(pat='時薪'),'salary_asist']=data.loc[data['salary'].str.contains(pat='時薪'),'salary'].\
    str.replace('元','').str.replace('時薪','').str.replace(',','')
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
data.loc[data['salary'].str.contains(pat='日薪'),'salary_h']=data.loc[data['salary'].str.contains(pat='日薪'),'salary_asist'].\
    map(lambda x:int(x[x.find('~')+1:])*20 if x.find('~')!=-1 else (int(x[0:x.find('以上')])*20 if x.find('以上')!=-1 else int(x)*20))

#salary_l
data.loc[data['salary'].str.contains(pat='月薪'),'salary_l']=data.loc[data['salary'].str.contains(pat='月薪'),'salary_asist'].\
    map(lambda x:int(x[0:x.find('~')]) if x.find('~')!=-1 else (int(x[0:x.find('以上')]) if x.find('以上')!=-1 else int(x)))
data.loc[data['salary'].str.contains(pat='年薪'),'salary_l']=data.loc[data['salary'].str.contains(pat='年薪'),'salary_asist'].\
    map(lambda x:int(x[0:x.find('~')])/12 if x.find('~')!=-1 else int(x[0:x.find('以上')])/12)
data.loc[data['salary'].str.contains(pat='時薪'),'salary_l']=data.loc[data['salary'].str.contains(pat='時薪'),'salary_asist'].\
    map(lambda x:int(x[0:x.find('~')])*160 if x.find('~')!=-1 else (int(x[0:x.find('以上')])*160 if x.find('以上')!=-1 else int(x)*160))
data.loc[data['salary'].str.contains(pat='日薪'),'salary_l']=data.loc[data['salary'].str.contains(pat='日薪'),'salary_asist'].\
    map(lambda x:int(x[0:x.find('~')])*20 if x.find('~')!=-1 else (int(x[0:x.find('以上')])*20 if x.find('以上')!=-1 else int(x)*20))

#salary_a
data['salary_a']=(data['salary_h']+data['salary_l'])/2

#處理地區 "區" 資料
data.loc[data['region'].str.contains(pat='區'),'region']=data.loc[data['region'].str.contains(pat='區'),'region'].map(lambda x: x[:3])

#處理地區 "鄉、市、鎮" 資料
data.loc[data['region'].str.contains(pat='鄉|鎮'),'region']=data.loc[data['region'].str.contains(pat='鄉|鎮'),'region'].map(lambda x: x[0:3])
data.loc[data['region'].str.contains(pat='\D{2}縣\D{2}市',regex=True),'region']=data.loc[data['region'].str.contains(pat='\D{2}縣\D{2}市',regex=True),'region'].map(lambda x: x[:3])
#處理其他國家、地區
data.loc[data['region'].str.contains(pat='\D{2}縣|\D{2}市',regex=True)==False,'region']=data.loc[data['region'].str.contains(pat='\D{2}縣|\D{2}市',regex=True)==False,'region'].map(lambda x: '其他地區')

#著重台灣職缺，故刪除國外職缺的row
aboard=data[data['region'].str.contains(pat='其他地區')].index
data.drop(aboard,inplace=True)

#刪除講師職缺
teacher=data[data['job_title'].str.contains(pat='講師')].index
data.drop(teacher,inplace=True)

#print(data.groupby('working_Exp').working_Exp.count().to_dict())

data.to_csv('D:/資料20220523備份/數據分析相關/Python/crawler_pratice/104/process_data_new0607.csv',index=False)
