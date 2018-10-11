from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

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

print "Connecting ..."
dev = Peripheral(devices[number].addr, 'random')

print "Services ..."
for svc in dev.services:
    print str(svc)

try:
    testService = dev.getServiceByUUID(UUID(0xfff0))
    for ch in testService.getCharacteristic():
        print str(ch)
    ch = dev.getCharacteristic(uuid=UUID(0xfff1))[0]
    if (ch.supportsRead()):
        print ch.read()
finally:
    dev.disconnect()
