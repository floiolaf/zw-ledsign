#!/usr/bin/python

import time

from neopixel import *

# LED strip configuration:
LED_COUNT      = 144 * 30      # Number of LED pixels.
#LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN        = 21      #21 // for PCM 5400 LEDs
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
#LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_DMA        = 10      # This channel works better to not put SD card into read-only mode
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

import signal
import sys
def signal_handler(signal, frame):
        print('You pressed Ctrl+C! Setting all LEDs off.')
        wipe(strip, Color(0,0,0)) # sets all led's to black
        strip.show()
        strip.show()
        # time.sleep(100)
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

import argparse

parser = argparse.ArgumentParser(description='Send commands to LED color strip to show colors.')
parser.add_argument('--color', help='which color to show in the form ff00ff for RGB, i.e. ff0000 for all red')
parser.add_argument('--rainbow', action='store_true', help='Draw rainbow that fades across all pixels at once.')
parser.add_argument('--rainbowcycle', action='store_true', help='Draw rainbow that uniformly distributes itself across all pixels.')
parser.add_argument('--rainbowchase', action='store_true', help='Rainbow movie theater light style chaser animation.')
parser.add_argument('--seahawks', action='store_true', help='Show blue/green stripes across all pixels.')
args = parser.parse_args()
print(args)

# parser.print_help()
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')

# args = parser.parse_args()
# print args.accumulate(args.integers)

def wipe(strip, color, wait_ms=50):
	"""Wipe color across display all at once."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
	strip.show()

def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)
		
def rainbow(strip): #, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	wait_ms = 2
	iterations = 55
	# 2,000 iterations over 5ms should give us 10 seconds
	for j in range(0, 5*iterations, 5):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip): #, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	wait_ms = 1
	iterations = 56
	for j in range(0, 5*iterations, 5):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	wait_ms = 2
	iterations = 18
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)
				
def seahawks(strip):
    stripes = 30 * 4
    block = strip.numPixels() / stripes
    print("Stripes:", stripes, "Blocks:", block)
    isGreen = True
    for j in range(stripes):
        for i in range(j * block, (j * block) + block):
            if isGreen:
                # print("Pixel:G", "i:", i)
                strip.setPixelColor(i, Color(0,255,0))
            else:
                # print("Pixel:B", "i:", i)
                strip.setPixelColor(i, Color(0,0,255))
        
        # toggle green to blue        
        if isGreen:
            isGreen = False
        else:
            isGreen = True
            
    strip.show()
    time.sleep(10)
		
# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()

wipe(strip, Color(0,0,0)) # sets all led's to black

# show time so we know how long we displayed for
print(time.strftime("%I:%M:%S %p"))

# Show a color for 10 seconds and exit
if (args.rainbow):
    print("Showing rainbow that fades across all pixels at once.")
    rainbow(strip)
    # rainbowCycle(strip)
    # theaterChaseRainbow(strip)
elif (args.rainbowcycle):
    print("Showing rainbow that uniformly distributes itself across all pixels.")
    rainbowCycle(strip)
elif (args.rainbowchase):
    print("Showing rainbow movie theater light style chaser animation.")
    theaterChaseRainbow(strip)
elif (args.seahawks):
    seahawks(strip)
elif (args.color != None):
    print("Showing solid color")
    print "The Color is:", args.color
    s = args.color
    red = s[0:2]
    green = s[2:4]
    blue = s[4:6]
    print("red:", red, "green:", green, "blue:", blue)
    r = int(red, 16)
    g = int(green, 16)
    b = int(blue, 16)
    print("r:", r, "g:", g, "b:", b)
    wipe(strip, Color(r, g, b))
    time.sleep(10)
else:
    print("Nothing to do")
    
print(time.strftime("%I:%M:%S %p"))
wipe(strip, Color(0,0,0)) # sets all led's to black