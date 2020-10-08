import redis
from threading import Thread
from threading import Lock
from time import sleep
import json
import datetime
import hashlib
import random

class redisLib:
    def __init__(self, **args):
        self._args = args
        self._redisClient = None
        self._subscriberClient = None
        self._queuesUnderConsideration = {}
        self._finishedQueuesUnderConsideration = {}
        self._subscribeQueue = "$#ujq_subscribed_queue"
        self._queueNamePreString = "$#ujq_queue"
        self._finishedQueue = "$#ujq_finished_queue"
        self._p = None
        self._errorCallback = lambda x: None
        self._errorCallback = None
        self._lock = Lock()
        self._exit = None

    def _connectRedis(self):
        try:
            self._redisClient = redis.Redis(**self._args)
            self._subscriberClient = redis.Redis(**self._args)
            self._eventEmitter()
            return True
        except Exception as e:
            if self._errorCallback:
                self._errorCallback(str(e))
            else:
                raise Exception("Error Creating Redis Queue : "+str(e))

    def _eventEmitter(self):
        try:

            self._p = self._subscriberClient.pubsub()
            self._p.psubscribe(self._subscribeQueue, self._finishedQueue)
            thread = Thread(target=self._newJob, args=())
            thread.daemon = True
            thread.start()
        except Exception as e:
            raise Exception(e)

    def _newJob(self):
        try:
            for new_message in self._p.listen():
                if(new_message["type"] == "message" or new_message["type"] == "pmessage"):
                    self._newJobThread(
                        type=str(new_message["channel"], 'utf-8'), queue=str(new_message["data"], 'utf-8'))
        except Exception as e:
            self._exit = str(e)
            #raise Exception(e)

    def _newJobThread(self, type, queue):
        try:
            if type == self._subscribeQueue:
                if self._keyExist(self._queuesUnderConsideration, queue):
                    popMessage = self._getMessage(
                        f"{self._queueNamePreString}_{queue}")
                    while popMessage != None:
                        self._runCallback(queue, None, popMessage)
                        popMessage = self._getMessage(
                            f"{self._queueNamePreString}_{queue}")
            if type == self._finishedQueue:
                with self._lock:
                    if self._keyExist(self._finishedQueuesUnderConsideration, queue):
                        popMessage = self._getMessage(
                            f"{self._queueNamePreString}_{queue}",True)
                        
                        self._finishedQueuesUnderConsideration[queue] = popMessage

        except Exception as e:
            raise Exception(e)

    def _keyExist(self, dict, key):
        if key in dict.keys():
            return True
        else:
            return False

    def _getMessage(self, queueName, delete = False):
        try:
            message = self._redisClient.lpop(queueName)
            if message == 0 or message == None:
                return None

            message = json.loads(message)
            if delete == True:
                self._redisClient.delete(queueName)
            return message
        except Exception as e:
            raise Exception(e)

    def _onCreatedJob(self, jobName, callback):
        try:
            #Commenting Out this code to allow Job Creation Twice
            #if (self._keyExist(self._queuesUnderConsideration, jobName)):
            #    raise Exception(
            #        'Cannot Call on Created Twice for same Job name')
            self._queuesUnderConsideration[jobName] = callback
            self._newJobThread(self._subscribeQueue, jobName)
        except Exception as e:
            raise Exception(e)

    def _runCallback(self, jobName, err, initialData):
        try:
            def complete(data, error=False):
                newId = self._encryptRandom()
                finalData = {
                    "id": newId,
                    "initial_id": initialData["id"],
                    "initial_data": initialData["message"],
                    "completed_on": datetime.datetime.now().timestamp()*1000,
                    "created_on": initialData["created_on"],
                    "data": data,
                    "error": error
                }
                with self._redisClient.pipeline() as p:
                    p.rpush(
                        f"{self._queueNamePreString}_{initialData['id']}", json.dumps(finalData))
                    p.publish(self._finishedQueue, initialData["id"])
                    p.execute()
                return newId
            self._queuesUnderConsideration[jobName](err, initialData, complete)
        except Exception as e:
            raise Exception(e)

    def _encryptRandom(self):
        return hashlib.md5(f"_${str(random.randint(0, 100000000000))}_{str(random.randint(0, 100000000000))}".encode()).hexdigest()

    def _addToList(self, name, payload):
        try:
            message = json.dumps(payload)
            with self._redisClient.pipeline() as p:
                p.rpush(f"{self._queueNamePreString}_{name}", message)
                p.publish(self._subscribeQueue, name)
                p.execute()
        except Exception as e:
            raise Exception(e)

    def _addToQueue(self, name, payload, timeout=1000*60*10):
        try:
            md5Hash = self._encryptRandom()
            data = {
                "id": md5Hash,
                "created_on": datetime.datetime.now().timestamp()*1000,
                "defer": datetime.datetime.now().timestamp()*1000 + timeout,
                "message": payload
            }
            self._addToList(name, data)
            return md5Hash
        except Exception as e:
            raise Exception(e)

    def _onCompletedJob(self, jobId, timeout):
        try:
            if self._keyExist(self._finishedQueuesUnderConsideration, jobId):
                raise Exception(
                    "onCompleted can only be called once for a Job Id")
            self._finishedQueuesUnderConsideration[jobId] = "Pending"
            counter = 0
            loopVar = True
            while loopVar:
                if counter > timeout:
                    loopVar = False
                    raise Exception(f"Timedout Reached for Job {jobId}")
                with self._lock:
                    if self._finishedQueuesUnderConsideration[jobId] != "Pending":
                        loopVar = False
                        toSend = self._finishedQueuesUnderConsideration[jobId]
                        del self._finishedQueuesUnderConsideration[jobId]
                        return toSend
                sleep(0.01)
                counter += 10
        except Exception as e:
            raise Exception(e)
