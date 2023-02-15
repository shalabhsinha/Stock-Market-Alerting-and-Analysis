#!/usr/bin/env python
# coding: utf-8

# In[7]:


#Importing all the required packages required 
from kafka import KafkaConsumer
from json import dumps,loads
import requests, time, datetime


# In[40]:


#Defining a consumer which subscribes to the topic zen 
consumer =KafkaConsumer('zen',bootstrap_servers=['127.0.0.1:9092'],value_deserializer=lambda x: loads(x.decode('utf-8')))
#Traversing through all the messages in the consumer to check if any of then company's LTP crosses 5% change mark. If so then print them
for c in consumer:
    ini_val=c.value['c'][-2] #stock price at market open
    cur_val=c.value['c'][-1] #stock price at urrent time
    name=c.value['name']
    percent=(cur_val-ini_val)*100/ini_val
    print(c.value)
    if(abs(percent)>=4.99):
        print(name)
        print(ini_val)
        print(cur_val)
        print(percent)

