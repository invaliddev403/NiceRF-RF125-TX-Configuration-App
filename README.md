# NiceRF-RF125-TX-Configuration-App
Python script to interact with the RF125-TX Module from NiceRF

# Module Link
https://www.nicerf.com/item/125khz-transmitter-and-receiver-module-rf125

# Requirements
* pyserial
* python3

# Usage
1. Connect a UART to USB adapter to the RF125-TX module
2. Run the script: python3 nicerf-RF125-TX_main.py

# Module Information
* All commands are required to end with ``` 0x0d 0x0a ```
* Set the payload
1. CMD Byte: 0x57
2. Length (1 Byte): 0x2D (45 bytes) or less
3. Payload (length byte):
4. End Code: ``` 0x0d 0x0a ```
5. Example: ``` 0x57 0x05 0x01 0x02 0x03 0x04 0x05 0x0D 0x0A ```
* Set the Transmitter ID
1. CMD Byte: 0x58
2. ID (7 Bits):
3. End Code: ``` 0x0d 0x0a ```
4. Example: ``` 0x58 0x01 0x0D 0x0A ```
* Read out Transmitter ID
1. Command: ``` 0x52 0x0D 0x0A ```
* Set the time interval (ms) between adjacent transmissions. The time interval should be
250ms – 60000 ms), it will be set as 250ms automatically if it is less than 250ms.
1. CMD Byte: 0x53
2. TIME_H (1 Byte):
3. TIME_L (1 Byte):
4. End Code: ``` 0x0d 0x0a ```
5. Example: ``` 0x53 0x03 0xe8 0x0D 0x0A ```
* Start Transmission
1. Command: ``` 0x73 0x74 0x61 0x72 0x74 0x0D 0x0A ```
* Stop Transmission
1. Command: ``` 0x73 0x74 0x6F 0x70 0x0D 0x0A ```
