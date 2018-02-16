# Lights-control-Occupancy-detection-using-IoT-Raspberry-Pi
A system which collects data from various sensors which help in regulating lighting in the room  
Sep 2016

The project aimed at collecting data from various sensors including PIR sensors, LDR sensors, temperature sensors, along with weather data from a Raspberry Pi setup. The data collected helped in analysing in which situations can the lights in the room be dimmed (and open the window blinds) or brightened to serve the purpose of daylight harvesting.  

The ground truth was collecting using a simple web app where the occupants had to toggle a switch while entering or leaving the room.  

To run the project:
Run the webserver in a terminal and the webapp can be accessed through the browser by providing the IP address of the Raspberry Pi. To start the data collection process, run the script sensordata_collect.py.
