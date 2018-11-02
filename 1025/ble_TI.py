from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
from time import sleep

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

class NotifyDelegate(DefaultDelegate):
    def __init__(self, handles):
        DefaultDelegate.__init__(self)
        self.handles = handles
    def handleNotification(self, cHandle, data):
        ret = 1 if data == '\x01' else 0
        if cHandle == self.handles[0]:
            print 'btn1', ret 
        if cHandle == self.handles[1]:
            print 'btn2', ret

'''
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)
n = 0
for dev in devices:
    print "%d: Devices %s (%s), RSSI=%d db" % (n, dev.addr, dev.addrType, dev.rssi)
    n += 1
    for (adtype, desc, value) in dev.getScanData():
        print "%s = %s" % (desc, value)

number = input('Enter your device number: ')
print('Device', number)
print(devices[number].addr)
'''

print "Connecting ..."
# dev = Peripheral(devices[number].addr, 'public')
dev = Peripheral('f0:f8:f2:d2:bd:21', 'public')


'''
print "Services ..."
for svc in dev.services:
    print str(svc)
'''

try:
    # testService = dev.getServiceByUUID('f0001110-0451-4000-b000-000000000000')
    # for ch in testService.getCharacteristics():
    #     print str(ch)
    # ch = dev.getCharacteristics(uuid=UUID(0xfff1))[0]
    led1 = dev.getCharacteristics(uuid = 'f0001111-0451-4000-b000-000000000000')[0]
    led2 = dev.getCharacteristics(uuid = 'f0001112-0451-4000-b000-000000000000')[0]

    btns = dev.getServiceByUUID('f0001120-0451-4000-b000-000000000000')
    btn1 = dev.getCharacteristics(uuid = 'f0001121-0451-4000-b000-000000000000')[0]
    btn2 = dev.getCharacteristics(uuid = 'f0001122-0451-4000-b000-000000000000')[0]
    dev.withDelegate(NotifyDelegate([btn1.getHandle(), btn2.getHandle()]))
    d_btns = btns.getDescriptors()
    for d in d_btns:
        print d
    d_btns[1].write('\x01\x00')
    d_btns[3].write('\x01\x00')

    led1.write('\x00')
    led2.write('\x01')
    while True:
        dev.waitForNotifications(0.5)
        if led1.read() == '\x00':
            led1.write('\x01')
            led2.write('\x00')
        else:
            led1.write('\x00')
            led2.write('\x01')
finally:
    dev.disconnect()
