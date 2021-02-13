# see https://github.com/peterhinch/micropython-async/tree/master/v2/gps
import uasyncio as asyncio
import as_GPS    #GPS NMEA to lat/log
from machine import UART
from math import floor    #for qth locator conversion

uart =  UART(1, 9600, bits=8, parity=None, stop=1)
sreader = asyncio.StreamReader(uart)  # Create a StreamReader
gps = as_GPS.AS_GPS(sreader)  # Instantiate GPS

def location_to_square(lat, lon):
    #Converts latitude and longitude in decimal format to QTH locator. Gets latitude and longitude as floats.Returns QTH locator as string.
    # Local Constants
    ASCII_0 = 48
    ASCII_A = 65
    ASCII_a = 97
    # Validate input
    assert isinstance(lat, (int, float))
    assert isinstance(lon, (int, float))
    assert -90.0 <= lat <= 90.0
    assert -180.0 <= lon <= 180.0
    
    # Separate fields, squares and subsquares
    lon += 180
    lat += 90
    
    # Fields
    lon_field = int(floor(lon / 20))
    lat_field = int(floor(lat / 10))
    
    lon -= lon_field * 20
    lat -= lat_field * 10
    
    # Squares
    lon_sq = int(floor(lon / 2))
    lat_sq = int(floor(lat / 1))
    
    lon -= lon_sq * 2
    lat -= lat_sq * 1

    # Subsquares
    lon_sub_sq = int(floor(lon / (5.0 / 60)))
    lat_sub_sq = int(floor(lat / (2.5 / 60)))
    
    lon -= lon_sub_sq * (5.0 / 60)
    lat -= lat_sub_sq * (2.5 / 60)
 
    # Extended squares
    lon_ext_sq = int(round(lon / (0.5 / 60)))
    lat_ext_sq = int(round(lat / (0.25 / 60)))
    
    # Generate QTH locator
    qth_locator = ''
    
    qth_locator += chr(lon_field + ASCII_A)
    qth_locator += chr(lat_field + ASCII_A)
    
    qth_locator += chr(lon_sq + ASCII_0)
    qth_locator += chr(lat_sq + ASCII_0)
    
    if lon_sub_sq > 0 or lat_sub_sq > 0 or lon_ext_sq > 0 or lat_ext_sq > 0:
        qth_locator += chr(lon_sub_sq + ASCII_a)
        qth_locator += chr(lat_sub_sq + ASCII_a)

    return qth_locator

async def test():
    print('waiting for GPS data')
    await gps.data_received(position=True, altitude=True)
    for _ in range(10):
        qth = location_to_square(gps.latitude()[0], gps.longitude()[0])
        print (qth)
        await asyncio.sleep(2)

loop = asyncio.get_event_loop()
loop.run_until_complete(test())