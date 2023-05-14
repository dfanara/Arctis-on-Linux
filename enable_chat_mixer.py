# Rough example used to send a chat mix enable packet.

import usb.core
import usb.util
import usb.backend.libusb1

VENDOR_ID=0x1038
PRODUCT_ID=0x12E0

# print(list(usb.core.find(find_all=True)))

device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if device is None:
    raise ValueError('Device not found')
    sys.exit(1)

print(device)
# print("----------------------------------------------")

configuration = device.get_active_configuration()
device.set_configuration()
# print(configuration)

interface = configuration[(4, 0)]
# device.detach_kernel_driver(interface)

# HID interface OUT (0x04, 0x4)
endpoint = interface[1]

## ENABLE CHATMIX 0x06 0x49 0x01
## DISABLE CHATMIX 0x06 0x49 0x00

print("writing")
print(endpoint.write('\x06\x49\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))
print("done")