# Arctis on Linux

This project serves to document my journey and progress in reverse engineering the USB protocol for the SteelSeries Acrtis Nova Pro Wireless gaming headset, with the ultimate goal of supporting this hardware on Linux. 

As a goal for this project, I would like to support:
1. Enable the chat/game fader on the device, because fading between discord and my current game is a necessity for me.
    1. This functionality is not available on the headset by default, and is explicitly enabled when connected to the Sonar feature of the SteelSeries GG client.
1. Read the chat/game fader state from the device
    1. Reading the state of the fader allows us to control a software mixer natively form the headset's interface.
1. Provide two audio outputs to pick from on linux, a `Game` output and a `Chat` output.
    1. The fader state on the headset should control the volume of these audio outputs
    1. The outputs should be mixed together and fead to the headset's primary audio stream

# Device Overview

```
DEVICE ID 1038:12e0 on Bus 000 Address 001 =================
 bLength                :   0x12 (18 bytes)
 bDescriptorType        :    0x1 Device
 bcdUSB                 :  0x200 USB 2.0
 bDeviceClass           :    0x0 Specified at interface
 bDeviceSubClass        :    0x0
 bDeviceProtocol        :    0x0
 bMaxPacketSize0        :   0x40 (64 bytes)
 idVendor               : 0x1038
 idProduct              : 0x12e0
 bcdDevice              :  0x130 Device 1.3
 iManufacturer          :    0x1 SteelSeries
 iProduct               :    0x2 Arctis Nova Pro Wireless
 iSerialNumber          :    0x0
 bNumConfigurations     :    0x1
  CONFIGURATION 1: 500 mA ==================================
   bLength              :    0x9 (9 bytes)
   bDescriptorType      :    0x2 Configuration
   wTotalLength         :  0x12f (303 bytes)
   bNumInterfaces       :    0x5
   bConfigurationValue  :    0x1
   iConfiguration       :    0x0
   bmAttributes         :   0x80 Bus Powered
   bMaxPower            :   0xfa (500 mA)
    INTERFACE 0: Audio =====================================
     bLength            :    0x9 (9 bytes)
     bDescriptorType    :    0x4 Interface
     bInterfaceNumber   :    0x0
     bAlternateSetting  :    0x0
     bNumEndpoints      :    0x1
     bInterfaceClass    :    0x1 Audio
     bInterfaceSubClass :    0x1
     bInterfaceProtocol :    0x0
     iInterface         :    0x0
      ENDPOINT 0x81: Interrupt IN ==========================
       bLength          :    0x9 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x81 IN
       bmAttributes     :    0x3 Interrupt
       wMaxPacketSize   :    0x8 (8 bytes)
       bInterval        :    0x8
    INTERFACE 1: Audio =====================================
     bLength            :    0x9 (9 bytes)
     bDescriptorType    :    0x4 Interface
     bInterfaceNumber   :    0x1
     bAlternateSetting  :    0x0
     bNumEndpoints      :    0x0
     bInterfaceClass    :    0x1 Audio
     bInterfaceSubClass :    0x2
     bInterfaceProtocol :    0x0
     iInterface         :    0x0
    INTERFACE 1, 1: Audio ==================================
     bLength            :    0x9 (9 bytes)
     bDescriptorType    :    0x4 Interface
     bInterfaceNumber   :    0x1
     bAlternateSetting  :    0x1
     bNumEndpoints      :    0x1
     bInterfaceClass    :    0x1 Audio
     bInterfaceSubClass :    0x2
     bInterfaceProtocol :    0x0
     iInterface         :    0x0
      ENDPOINT 0x82: Isochronous IN ========================
       bLength          :    0x9 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x82 IN
       bmAttributes     :    0xd Isochronous
       wMaxPacketSize   :   0x60 (96 bytes)
       bInterval        :    0x1
    INTERFACE 2: Audio =====================================
     bLength            :    0x9 (9 bytes)
     bDescriptorType    :    0x4 Interface
     bInterfaceNumber   :    0x2
     bAlternateSetting  :    0x0
     bNumEndpoints      :    0x0
     bInterfaceClass    :    0x1 Audio
     bInterfaceSubClass :    0x2
     bInterfaceProtocol :    0x0
     iInterface         :    0x0
    INTERFACE 2, 1: Audio ==================================
     bLength            :    0x9 (9 bytes)
     bDescriptorType    :    0x4 Interface
     bInterfaceNumber   :    0x2
     bAlternateSetting  :    0x1
     bNumEndpoints      :    0x1
     bInterfaceClass    :    0x1 Audio
     bInterfaceSubClass :    0x2
     bInterfaceProtocol :    0x0
     iInterface         :    0x0
      ENDPOINT 0x2: Isochronous OUT ========================
       bLength          :    0x9 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x2 OUT
       bmAttributes     :    0xd Isochronous
       wMaxPacketSize   :  0x120 (288 bytes)
       bInterval        :    0x1
    INTERFACE 2, 2: Audio ==================================
     bLength            :    0x9 (9 bytes)
     bDescriptorType    :    0x4 Interface
     bInterfaceNumber   :    0x2
     bAlternateSetting  :    0x2
     bNumEndpoints      :    0x1
     bInterfaceClass    :    0x1 Audio
     bInterfaceSubClass :    0x2
     bInterfaceProtocol :    0x0
     iInterface         :    0x0
      ENDPOINT 0x2: Isochronous OUT ========================
       bLength          :    0x9 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x2 OUT
       bmAttributes     :    0xd Isochronous
       wMaxPacketSize   :   0xc0 (192 bytes)
       bInterval        :    0x1
    INTERFACE 3: Human Interface Device ====================
     bLength            :    0x9 (9 bytes)
     bDescriptorType    :    0x4 Interface
     bInterfaceNumber   :    0x3
     bAlternateSetting  :    0x0
     bNumEndpoints      :    0x1
     bInterfaceClass    :    0x3 Human Interface Device
     bInterfaceSubClass :    0x0
     bInterfaceProtocol :    0x0
     iInterface         :    0x0
      ENDPOINT 0x83: Interrupt IN ==========================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x83 IN
       bmAttributes     :    0x3 Interrupt
       wMaxPacketSize   :    0x2 (2 bytes)
       bInterval        :   0x10
    INTERFACE 4: Human Interface Device ====================
     bLength            :    0x9 (9 bytes)
     bDescriptorType    :    0x4 Interface
     bInterfaceNumber   :    0x4
     bAlternateSetting  :    0x0
     bNumEndpoints      :    0x2
     bInterfaceClass    :    0x3 Human Interface Device
     bInterfaceSubClass :    0x0
     bInterfaceProtocol :    0x0
     iInterface         :    0x0
      ENDPOINT 0x84: Interrupt IN ==========================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x84 IN
       bmAttributes     :    0x3 Interrupt
       wMaxPacketSize   :   0x40 (64 bytes)
       bInterval        :   0x10
      ENDPOINT 0x4: Interrupt OUT ==========================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x4 OUT
       bmAttributes     :    0x3 Interrupt
       wMaxPacketSize   :   0x40 (64 bytes)
       bInterval        :   0x10
```

# Protocol Overview

At first glance, it appears that the SteelSeries GG software primarily communicates with the headset via the HID interface (Interface 4), writing HID packets to the `0x4` endpoint. The packets have a data length of 64 bytes, and are zero filled at the end of the packet.

I will refer to the `Interrupt OUT` (Endpoint 0x4) interface on the device as `HID OUT`.

The `Interrupt IN` (Endpoint 0x84) interface is used by the headset control box to relay state back to the SteelSeries GG client. I will refer to this endpoint as `HID IN`

## Controlling the Chat Mixer

The Chat Mixer can be controlled via the `HID OUT` endpoint by sending the following packet:

1. ENABLE CHAT MIXER: `0x06 0x49 0x01`
1. DISABLE CHAT MIXER `0x06 0x49 0x00`

Don't forget the packets are zero filled at the end to 64 bytes.

By enabling the chat mixer, we allow both the headset and the receiver to switch to the mixer option, and fade between game and chat outputs. This implementation appears to be software only, with all of the fading taking place on the Computer itself via the SteelSeries sonar software.

We can listen for changes to the mixer levels by listening to incoming interrupts on 0x84 (`HID IN`). More data to come on this later, but in short, the mixer status packet is in this format:

1. `0x07 0x45 <GAME VOLUME> <CHAT VOLUME>`
    1. where `<GAME VOLUME>` is between (inclusive) 0x00 and 0x64 (0-100 decimal)
    1. where `<CHAT VOLUME>` is between (inclusive) 0x00 and 0x64 (0-100 decimal)
1. When the mixer is exactly in the center, both GAME and CHAT volume are `0x64` or `100%`.