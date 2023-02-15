#!/usr/bin/env python
# coding: utf-8

# In[4]:


#Importing all the required packages required 
from kafka import KafkaProducer
from json import dumps
import requests, time,datetime 
from pyspark.sql import SparkSession


# In[81]:


header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',}
x=str(datetime.date.today()).split('-')
start =(datetime.datetime(int(x[0]), int(x[1]), int(x[2]),9,16,0).timestamp()) #morning 9:16AM
end=round(time.time()) # current time.
today_end=start+22500 # 3:30PM market closing  

#Defined companies to keep a track of
comp=['LTIM','BAJAJFINSV','POLYCAB','TCS','BAJFINANCE','TATAELXSI','DEEPAKNTR','TITAN','COFORGE','SRF','RELIANCE','ASIANPAINT','INFY','ASTRAL','LTTS','DMART','VBL','MUTHOOTFIN','HDFCBANK','HLEGLAS','NAVINFLUOR','ICICIBANK','HCLTECH','AARTIIND','HINDUNILVR','RELAXO','IRCTC','HDFCAMC','TATACONSUM','CDSL','HAPPSTMNDS','DIVISLAB','ALKYLAMINE','SBICARD','NAUKRI','MTARTECH','JUBLFOOD','PRINCEPIPE','FLUOROCHEM']

#Define a function to create the messages to the topic
def send_message():
    for i in comp:
        url="https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol="+i+"&resolution=1D&from="+str(start)+"&to="+str(end)+"&countback=2&currencyCode=INR"
        resp=requests.get(url,headers=header).json() #using json() to get a dictionary type of the data recieved from requests
        resp['name']=i #adding company name to the dictionary
        producer=KafkaProducer(bootstrap_servers=['127.0.0.1:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
        producer.send('zen',value=resp)# Write message to the topic 'zen'
#Checking and Calling the function to generate messages to the topic if the current time is within market hours(9:15-15:30): 
while end<=today_end:
    send_message()
    time.sleep(3)

#Generate reports manually by uncommenting below and giving values accordingly:
'''start= 1675395960
end = 1675418820
dt= '2023-02-03' '''
dt=str(datetime.date.today())
#Create a file if not present or rewrite it:
f = open(r'E:\files\price_'+dt+'.txt', "w+")

#Writing the first line with column names:
f.write('Company,Trade_Dt,Prev_close,Open,High,Low,Close,Volume\n')

#Wrting the file after market hours with LTPs of current date for the mentioned companies.
for i in comp:
    url="https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol="+i+"&resolution=1D&from="+str(start)+"&to="+str(end)+"&countback=2&currencyCode=INR"
    resp=requests.get(url,headers=header).json()
    S=i+','+dt+','+str(resp['c'][-2])+','
    key_list=list(resp.keys())
    for i in range(2,len(key_list)):
        k=key_list[i]
        S=S+str(resp[k][-1])+','
    f.write(S[:-1]+'\n')
f.close()

