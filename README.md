# Stock-Market-Alerting-and-Analysis
Project to demo Realtime data streaming and batch processing for analytics

A realtime alerting system for Indian Stock Market which generates alerts based on LTP(Last Traded Price) and loads a DataWarehouse for generating reports and data analytics for BI by creating a Data Pipeline.
Structure of the project goes like:
We have Kafka for streaming the realtime data from the MoneyControl website. 
There is a topic 'zen' to which all the messages from the Producer which will write the messages. 
The Consumer subscribes to the same topic and checks if the Last Traded Price changes more than 5%.  If there are any such cases then it will trigger an alert(basic printing here)
All this happens during the market hrs(9:15-15:30)
Once the market closes then it creates a file with the LTP for all the mentioned Companies.
This file is consumed by a downstream(Simulation) Hive Team which is loading the files everyday into the warehouse. Now we can run analytics to get more insights 
Simulation of another downstream is BI team which are generating Power Bi reports daily based on the same file to represent data changes for the current day.
