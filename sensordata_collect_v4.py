#september 27 2016
#code to collect data from pir, ldr, temp (two threads)
#frequency of PIR - very frequent
#frequcny of temp, lum - once in 5 minutes
#additionally, weather is also checked every few minutes

import time
import random
import RPi.GPIO as GPIO
import threading
import sys
import spidev
import datetime
import json
import urllib2
from pymongo import MongoClient


GPIO.setmode(GPIO.BOARD)


client = MongoClient('mongodb://username:password@ds141410.mlab.com:41410/meghana_pe')



pir1 = 37
led_for_pir1 = 38

pir2 = 35
led_for_pir2 = 36

ldr1 = 7
ldr2 = 11

dark_medium_thresh = 0.0166
medium_light_thresh = 0.166

# calculates the resistance of the LDR based on time taken
# by capacitor to charge upto 63%
def get_resistance(pin_to_circuit):
        count = 0
        GPIO.setup(pin_to_circuit, GPIO.OUT)
        GPIO.output(pin_to_circuit, GPIO.LOW)
        time.sleep(0.1)

        #Change the pin back to input
        GPIO.setup(pin_to_circuit, GPIO.IN)
    
        #keep track of ticks/seconds
        start = time.time()

        #Count until the pin goes high
        while (GPIO.input(pin_to_circuit) == GPIO.LOW):
                count += 1
    
	#calculate resistance
        end = time.time()
        seconds = end - start
        resistance = seconds*1000000

        return resistance


# calculates luminance from resistance
def get_luminance(res):
        return (500.0/res)


# read SPI data from MCP3208 chip, 8 possible adc's (0 thru 7)
# reads data from temperature sensor using the adc chip
def readadc(adcnum):
        if adcnum > 7 or adcnum < 0:
                return -1
	r = spi.xfer2([((adcnum & 6) >> 1)+12 , (adcnum & 1) << 7, 0])
        adcout = ((r[1] & 15) << 8) + r[2]
        return adcout


#a thread for running the data collection
def temp_ldr():
	try:	
		db = client.meghana_pe
		collection = db.sensors_demo_oct4
		while True:	
			print "temperature while loop"
			res1 = (get_resistance(ldr1))
        		luminance1 = get_luminance(res1) #get luminance value
			res2 = (get_resistance(ldr2))
        		luminance2 = get_luminance(res2) #get luminance value
			print "luminance: ", luminance1, luminance2
			
			op1 = readadc(0) #get temperature value
			mVolt1 = (op1 * 3300)/4096 #it takes 5V, and output has 12 bits, volt in mV
        		temperature1 = (mVolt1) / 10 #500mV offset. one degree celcius for 10mV
			op2 = readadc(1) #get temperature value
			mVolt2 = (op2 * 3300)/4096 #it takes 5V, and output has 12 bits, volt in mV
        		temperature2 = (mVolt2) / 10 #500mV offset. one degree celcius for 10mV
			
			print "temperature: ", temperature1, temperature2

			loc_time = str(datetime.datetime.now())
			collection.insert_one({"timestamp":loc_time, "temperature1":temperature1, "luminance1": luminance1, "temperature2":temperature2, "luminance2": luminance2})
			time.sleep(2) #10 minutes-600
	finally:
		GPIO.cleanup()	
		sys.exit()


def weather_data():
	db = client.meghana_pe
	collection = db.weather_demo_oct4

	while True:
		f = urllib2.urlopen('http://api.wunderground.com/api/476f0829d094e584/geolookup/conditions/q/India/Bangalore.json')

		json_string = f.read()
		parsed_json = json.loads(json_string)
		location = parsed_json['location']['city']
		temp = parsed_json['current_observation']['temp_c']
		weather_string = parsed_json['current_observation']['weather']
		f.close()
		loc_time = str(datetime.datetime.now())
		print "Weather: ",loc_time, weather_string, temp
		collection.insert_one({"timestamp":loc_time, "temperature":temp, "weather_string":weather_string})	
		
		time.sleep(3600) #one hour-3600

if __name__=="__main__":
	GPIO.setup(pir1, GPIO.IN)
	GPIO.setup(pir2, GPIO.IN)
	GPIO.setup(led_for_pir1, GPIO.OUT)
	GPIO.setup(led_for_pir2, GPIO.OUT)

	GPIO.output(led_for_pir1, GPIO.HIGH)
	GPIO.output(led_for_pir2, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(led_for_pir1, GPIO.LOW)
	GPIO.output(led_for_pir2, GPIO.LOW)


	spi = spidev.SpiDev()
	spi.open(0, 0)



	try:	
		templdr_thread = threading.Thread(target = temp_ldr)
		templdr_thread.start()

		weather_thread = threading.Thread(target = weather_data)
		weather_thread.start()

		#main thread for the PIR sensors
		db = client.meghana_pe
		collection = db.pir_demo_oct4
		while True:
			i = GPIO.input(pir1)
			if i==0:
				GPIO.output(led_for_pir1, GPIO.LOW)
			elif i==1:
				GPIO.output(led_for_pir1, GPIO.HIGH)
			j = GPIO.input(pir2)
			if j==0:
				GPIO.output(led_for_pir2, GPIO.LOW)
			elif j==1:
				GPIO.output(led_for_pir2, GPIO.HIGH)
			
			if (i==1 or j==1):
				loc_time = str(datetime.datetime.now())
				collection.insert_one({"timestamp":loc_time, "PIR1":i, "PIR2":j})	
			time.sleep(2)	
	finally:
		GPIO.cleanup()
		sys.exit()
