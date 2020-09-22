from . import redis_lib
from threading import Thread
from time import sleep
import atexit

class ujq (redis_lib.redisLib):
    def __init__(self, host, port):
        super().__init__(host, port)

    def connect(self):
        try:
            result = self._connectRedis()
            def exit_handler():
                while True:
                    sleep(1)
            atexit.register(exit_handler)
            return result
        except Exception as e:
            raise Exception(e)

    def createJob(self, jobName, payload, timeout = 1000 * 60 * 10):
        try:
            id = self._addToQueue(str(jobName), payload, timeout)
            return id
        except Exception as e:
            raise Exception(e)

    def onCreated(self, jobName, callback):
        try:
            if jobName == None or callback == None:
                raise Exception("Job Name and Callback cannot be empty")
            thread = Thread(target=self._onCreatedJob, args=(jobName, callback))
            thread.daemon = True
            thread.start()
        except Exception as e:
            raise Exception(e)
    
    def onCompleted(self, jobId, timeout = 1000 * 60 * 10):
        try:
            result = self._onCompletedJob(jobId, timeout)
            return result
        except Exception as e:
            raise Exception(e)

    def runJob(self, jobName, payload, timeout = 1000 * 60 * 10):
        try:
            id = self.createJob(jobName, payload, timeout)
            result = self.onCompleted(id, timeout)
            if (result["error"]==True):
                raise Exception(str(result["data"]))
            return result["data"]
        except Exception as e:
            raise Exception(e)




    
