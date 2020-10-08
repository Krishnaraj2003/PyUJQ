from ujq import ujq
from time import sleep
import sys

UJQ = ujq(host='127.0.0.1', port=6379)


def complete(err, data, complete):
    print(data)
    complete({'bar':'foo'})

def run():
    UJQ.connect()
    print('Reached Here')
    UJQ.onCreated('Test1',complete)
    a = UJQ.runJob('Test1',{'foo':'bar'})
    print('Looking for ',a)

UJQ.onError(lambda x:run())
run()
