# Standard Boilerplate
import picoexplorer as display
import utime, random, math
from machine import Pin

# Setup screen
width = display.get_width()
height = display.get_height()
display_buffer = bytearray(width * height * 2)
display.init(display_buffer)
display.set_backlight(0.3)

up_arrow =[0,4,14,21,4,4,0,0]
down_arrow = [0,4,4,21,14,4,0,0]
bits = [128,64,32,16,8,4,2,1]

def blackscreen():   # clear screen to black
    display.set_pen(0,0,0)
    display.clear()
    display.update()
    
def show_title(msg,r,g,b,s,t):   # Display message on black screen with font size s and clear after t seconds
    blackscreen()
    display.set_pen(r,g,b)
    display.text(msg, 25, 25, 240, s)
    display.update()
    utime.sleep(t)
    blackscreen()

def show_screen(t):   # Update screen and wait for t seconds 
    display.update()
    utime.sleep(t)
                
def mychar(xpos, ypos, pattern):  # Print custom defined character
    for line in range(8):       # 5x8 characters
        for ii in range(5):     # Low value bits only
            i = ii + 3
            dot = pattern[line] & bits[i]  # Extract bit
            if dot:  # Only print WHITE dots
                display.pixel(xpos+i*3, ypos+line*3)
                display.pixel(xpos+i*3, ypos+line*3+1)
                display.pixel(xpos+i*3, ypos+line*3+2)
                display.pixel(xpos+i*3+1, ypos+line*3)
                display.pixel(xpos+i*3+1, ypos+line*3+1)
                display.pixel(xpos+i*3+1, ypos+line*3+2)
                display.pixel(xpos+i*3+2, ypos+line*3)
                display.pixel(xpos+i*3+2, ypos+line*3+1)
                display.pixel(xpos+i*3+2, ypos+line*3+2)

# == Main Programme ==
blackscreen()
show_title("G6DDX",255,50,50,5,2)

display.set_pen(200,200,0)
mychar(120, 130, up_arrow)   # Bigger
mychar(120, 160, down_arrow)  
show_screen(10)


# cleanup
blackscreen()