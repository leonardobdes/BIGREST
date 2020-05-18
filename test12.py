from bigrest.bigrest import BIGREST
import bigrest.bigrest
from datetime import datetime
from bigrest.utils.utils import rest_format
from bigrest.utils.utils import get_token
from bigrest.utils.utils import get_refresh_token
import time

username = 'bigrest'
password = 'oonfq9hd901'

device = BIGREST(device="192.168.255.1", username="test", password="bigip")
#device.download('cs_backup.ucs', path='./downloads/')
device.upload('/mgmt/cm/autodeploy/software-image-uploads', './downloads/cs_backup.ucs')
#data = {}
#data['command'] = 'save'
#data['name'] = 'testucs2'
#id = device.task_start('/mgmt/tm/task/sys/ucs', data=data)
#print(id)
#while device.task_running('/mgmt/tm/task/sys/ucs', id):
#    print("task running")
 #   time.sleep(5)
#result = device.task_result('/mgmt/tm/task/sys/ucs', id)
#print(result)
#token = get_refresh_token(device="192.168.255.1", username="test", password="bigip")
#print(token)
#wideips = device.load(path=f"/mgmt/cm/dns/current-config/wideip/a/")
#for wideip in wideips:
#    if wideip.name == "www.lab.local":
#        wip = wideip
#        break
#print(wip.selfLink)
#virtuals = device.show(f"/mgmt/tm/ltm/virtual/vs_internet")
#for virtual in virtuals:
    #print(virtual.asdict())
#    print(virtual.properties['tmName']['description'])
#    print(virtual.properties['clientside.maxConns']['value'])
#virtual = device.show(f"/mgmt/tm/ltm/virtual/test9")
#print(virtual[0].tmName['descrition'])
#print(virtual[0].clientside.maxConns['value'])
#tm = device.show(f"/mgmt/tm")
#print(virtual[0].com.f5.rest.common.RestWorker.isFineGrainedCollection['value'])
#print(bigrest.__version__)
#transaction = device.start_transaction()
#print (transaction.transId)
#data={}
#data["name"] = "/Common/test7"
#data["destination"] = "10.0.0.207%0:80"
#obj = device.create(path=f"/mgmt/tm/ltm/virtual", data=data)
#transaction_result = device.finish_transaction()
#print(transaction_result.state)
#with device as test:
#    data={}
#    data["name"] = "/Common/test9"
#    data["destination"] = "10.0.0.209%0:80"
#    device.create(path=f"/mgmt/tm/ltm/virtual", data=data)
#    print(test.transId)
#virtual = device.load(path=f"/mgmt/tm/ltm/virtual/test9")
#print(virtual[0].enabled)
#virtual[0].enabled = False
#print(virtual[0].enabled)
#print(virtual[0].asdict()['disabled'])
#device.save(f"/mgmt/tm/ltm/virtual/test9", virtual[0])
#virtuals = device.load(path=f"/mgmt/tm/ltm/virtual")
#for virtual in virtuals:
#    print(virtual.name)
#time.sleep(1200)
#virtual = device.load(path=f"/mgmt/tm/ltm/virtual/vs_asm")
#virtual[0].destination = "/Common/10.0.0.102:80"
#device.save(path=f"/mgmt/tm/ltm/virtual/vs_asm", obj=virtual[0])
#obj = device.save(path=f"/mgmt/tm/ltm/virtual/vs_asm", obj=virtual[0])
#print(obj.destination)
#device.delete(path=f"/mgmt/tm/ltm/virtual/test2")
#data={}
#data["name"] = "test2"
#data["destination"] = "10.0.0.200:80"
#obj = device.create(path=f"/mgmt/tm/ltm/virtual", data=data)
#print(obj.name)
#data["name"] = "test2"
#data["destination"] = "10.0.0.201:80"
#obj = device.modify(path=f"/mgmt/tm/ltm/virtual/test2", data=data)
#print(obj.destination)
#print(datetime.now().strftime("%M:%S:%f"))
#print(device.exist(path=f'/mgmt/tm/ltm/virtual/test2'))
#print(datetime.now().strftime("%M:%S:%f"))
#print(device.exist(path=f'/mgmt/tm/ltm/virtual/test3'))
#print(datetime.now().strftime("%M:%S:%f"))
#data={}
#data["name"] = "/Common/test4"
#data["destination"] = "10.0.0.203%0:80"
#obj = device.create(path=f"/mgmt/tm/ltm/virtual", data=data)
#print(f'/mgmt/tm/ltm/virtual/{rest_format(text="/Common/test4")}')
#print(device.exist(path=f'/mgmt/tm/ltm/virtual/{rest_format(text="/Common/test4")}'))
#print(device.exist(path=f'/mgmt/tm/ltm/virtual/~Common~test4'))
#dc = device.load(path=f"/mgmt/tm/gtm/datacenter/a b")
#print(dc[0].name)
#print(datetime.now().strftime("%H:%M:%S:%f"))