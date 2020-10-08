# UJQ
Universal Job Queue or UJQ in short is a Redis based Simple MultiPlatform Job management library. This Library is light weight and build for working with microservices. Currently we have Node and Python implementation of Library. C# and Java are in pipeline. 
## Benifits
1. Jobs can be created and processed by different application or services
2. Auto trigger when job is created
3. Job Completion and error indications

# Python
[CLICK HERE](https://github.com/Krishnaraj2003/UJQ) for Node.js Package

## Installing UJQ
You can use PIP to install

```
pip install ujq
```

## Connecting to Redis
Use the following to connect to redis

```python
from ujq import ujq
import json

UJQ = ujq(host="127.0.0.1",port=6379)
UJQ.connect()
    
```
## Create a new Job
The following Code will create a new Job
```python
id = UJQ.createJob('Test_100',{"test":"test45y76475"})
print(id)
    
```

## On creation of New Job
The Below Code will work on the job and returns a status
```python

def callback (message,complete):
    print(json.dumps(message))
    complete({'status':True,"DummyData":"blablabla"},False)

UJQ.onCreated('Test_100',callback)

```

In case of error, the false tag can be set as true... Invoking the complete callback will complete the job and will be moved from queue...

## On completion of Job

```python
result = UJQ.onCompleted(id)
print(result)
```

The above code will complete the job.

## Run Job

A new method is created for UJQ version 2 and above to run which combines both createJob and onCompleted

```python
result = UJQ.runJob('Test_100',{"test":"test45y76475"})
print(result)
```


# Express with UJQ
A simple implementation of Express in Node.js with UJQ in Python as shown


Create a **Server.js** with the below code
```javascript
const express = require("express")
const UJQ = require("ujq")
const ujq = new UJQ({ port: "6379", host: "127.0.0.1" })
const app = express()
const port = 3000

  ujq.connect()
    .then(() => {
        app.get('/', (req, res) => {

            ujq.createJob("test_q2", { test: "sample Data" })

                //Set On Complete
                .then((result) => ujq.onCompleted(result.id))

                //Send Result
                .then((result) => res.send(result))
    })
    
}).catch((e) => console.log(e))

app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))
```

Now Create **Worker.py** with the below Code
```python
from ujq import ujq
import json

def callback (message,complete):
    print(json.dumps(message))
    complete({'status':True,"DummyData":"blablabla"},False)

UJQ.onCreated('Test_100',callback)
```
Run both the files and **Enjoy** :B

## New onError method
This method will handle errors during disconnect of redis in between

```python
UJQ.onError(lambda x:run())
```