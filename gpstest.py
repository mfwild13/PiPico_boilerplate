# receive NMEA messages from GPS - test decoding location messages with https://rl.se/gprmc
# GPS RX goes to PICO GP4 and TX to PICO GP5
import uasyncio as asyncio
from machine import UART

gpsdata = UART(1, 9600, bits=8, parity=None, stop=1)

async def receiver():
    sreader = asyncio.StreamReader(gpsdata)
    while True:
        res = await sreader.readline()
        print('RX: ', res)

loop = asyncio.get_event_loop()
loop.create_task(receiver())
loop.run_forever()
