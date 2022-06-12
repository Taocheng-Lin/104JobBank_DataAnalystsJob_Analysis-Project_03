import pandas as pd

data=pd.read_csv("D:/資料20220523備份/數據分析相關/Python/crawler_pratice/104/process_job_data_analysis.csv")


#處理地區 "區" 資料
data.loc[data['region'].str.contains(pat='區'),'region']=data.loc[data['region'].str.contains(pat='區'),'region'].map(lambda x: x[:3])

#處理地區 "鄉、市、鎮" 資料
data.loc[data['region'].str.contains(pat='鄉|鎮'),'region']=data.loc[data['region'].str.contains(pat='鄉|鎮'),'region'].map(lambda x: x[0:3])
data.loc[data['region'].str.contains(pat='\D{2}縣\D{2}市',regex=True),'region']=data.loc[data['region'].str.contains(pat='\D{2}縣\D{2}市',regex=True),'region'].map(lambda x: x[:3])
#處理其他國家、地區
data.loc[data['region'].str.contains(pat='\D{2}縣|\D{2}市',regex=True)==False,'region']=data.loc[data['region'].str.contains(pat='\D{2}縣|\D{2}市',regex=True)==False,'region'].map(lambda x: '其他地區')

#print(data.groupby('region').region.count().to_dict())

#print(data.groupby('jobtype').jobtype.count().to_dict())

print(data.columns)
print(data.groupby('company').company.count().to_dict())


data.to_csv('D:/資料20220523備份/數據分析相關/Python/crawler_pratice/104/process_job_data_analysis_2.csv',index=False)