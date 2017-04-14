from flask import Flask,render_template,request
from lib_nrf24 import NRF24
import time
import RPi.GPIO as GPIO
import spidev

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

pipes = [[0xE8 , 0xE8 , 0xF0 , 0xF0 , 0xE1] , [0xF0 ,0xF0, 0xF0, 0xF0, 0xE1]]
radio  = NRF24(GPIO,spidev.SpiDev())
    
pins = {
        1 : {'name' : 'Light' , 'state' : False },
        2 : {'name' : 'Fan'   , 'state' : False }
       }

#for pin in pins :
 #   pins[pin]['state'] = False

@app.route('/')
def index():
   
    radio.begin(0,17)
    radio.setPayloadSize(32)
    radio.setChannel(0x76)
    radio.setDataRate(NRF24.BR_1MBPS)
    radio.setPALevel(NRF24.PA_MIN)
    radio.setAutoAck(True)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()
    radio.openWritingPipe(pipes[0])

    templateData = {
                   'pins' : pins
                  }
   
    return render_template('main.html', **templateData)


@app.route("/<value>/<action>")
def action(value,action):
    
   changePin = int(value)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
       if changePin == 1:
           message = list("1")
           while len(message)<32:
               message.append(0)
           radio.write(message)
           print("Sent message: {}".format(message))
                                 
       if changePin == 2:
           message = list("2")
           while len(message)<32:
               message.append(0)
           radio.write(message)
           print("Sent message: {}".format(message))
           
           

       #message = 'Turned' + deviceName + 'ON'
           
       pins[changePin]['state'] = True
       
      # Save the status message to be passed into the template:
      
   if action == "off":
       if changePin == 1:
           message = list("0")
           while len(message)<32:
               message.append(0)
           radio.write(message)
           print("Sent message: {}".format(message))
           
          
                
       if changePin == 2:
           message = list("3")
           #message = list("GETSTRING1")
           while len(message)<32:
               message.append(0)
           radio.write(message)
           print("Sent message: {}".format(message))
           
               
      # message = 'Turned' + deviceName + 'OFF'
       pins[changePin]['state'] = False
       
       
      
 
      # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
                   'pins' : pins
                  }
     

   return render_template('main.html', **templateData)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
