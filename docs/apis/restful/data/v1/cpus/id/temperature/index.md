---
layout: api-rest-data-v1-entry
title:  "cpu temperature endpoint"
---

Represents the temperature of a cpu having the specified ID.		
	
The dataset can either depending on the submitted request headers include the newest data or a number of datapoints in a given timespan. Historical data is limited 		
	
## Request		
	
### Methods		
	
Only GET requests are supported by this endpoint.		
	
### Parameter		
	
|key|description|possible values|mandatory|		
|:---:|:-----:|---|---|		
|id|The ID assigned to the cpu by the OpServ system. A list of all ids present at the moment can be retrieved with [this request](#cpus)|dynamic|yes|		
	
### Request Header		
	
|key|description|possible values|mandatory|default value|		
|:---:|:-----:|---|---|---|		
|realtime|A boolean indicating whether realtime data is wanted or not|"false" or 0 to retrieve historical data; "true" or 1 to retrieve realtime data|no|0|		
|start|The start time expressed as millis since unix epoch|any positive integer|no|0|		
|end|The end time expressed as millis since unix epoch|any positive integer, greater than start|no|[current time](https://currentmillis.com/)|		
|limit|The maximum number of datapoints to return|any positive integer greater 0, passing anything greater than 5000 will result in a limit of 5000|no|50|		
|unit|A string indicating whether the temperature should be expressed as celsius or fahrenheit|"c" or "celsius"; "f" or "fahrenheit"|no|"c"|		
	
### Request Body		
	
\- none -		
	
### Example		
	
   GET http://example.com/cpus/0/temperature?		
		   realtime=0&start=1472680800000&end=1475186400000&limit=35&unit=fahrenheit		
	
This returns **non-realtime**, historical data, split up to **35 data points** between the **1st and 30th of September 2016** including the min, max and average temperature in degree **fahrenheit** for the cpu with the **id 0**.		
   		
Passing no additional headers results in the usage of all default values. Thus 50 historical datapoints over all gathered data in degree celsius will be returned.		
	
## Response		

All response follow the ::standard-scheme:: defined for this version.		
Thus, the actual response data is included in the data section of the response.		
	
There are two response structures depending on the requested data, one for realtime data:		
	
   {  		
	   'data': {		
		   'value': 15.3,		
		   'unit': 'c'		
	   }		
	   'links': {		
		   ...		
	   }		
   }		
	
Aswell as one for historical data:		
	
   {  		
	   'data': {		
		   'values': [		
		   { 'timestamp': 1472680800000, 'min': 13.4, 'max': 32.6, 'avg': 17.3},		
		   ...		
		   { 'timestamp': 1475186400000, 'min': 7.9, 'max': 22.7, 'avg': 15.5}		
		   ],		
		   'unit': 'f'		
	   }		
	   'links': {		
		   ...		
	   }		
   }		
	
## error codes		
	
- TODO Invalid cpu id		
- TODO unsupported method		
