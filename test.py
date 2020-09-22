from ujq import ujq
UJQ = ujq(host='127.0.0.1', port=6379)
UJQ.connect()

def complete(err, data, complete):
    print(data)
    complete({'bar':'foo'})
UJQ.onCreated('Test1',complete)
a = UJQ.runJob('Test1',{'foo':'bar'})
print('Looking for ',a)