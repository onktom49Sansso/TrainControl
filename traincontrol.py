#!/usr/bin/python
# Importiert libraries
import RPi.GPIO as GPIO
import time
import os
import random 

#GPIO.setmode(GPIO.BCM)									# GPIO ueber GPIO-Nummer adressieren

#GPIO.setup(23, GPIO.OUT)								# definiert Ausgang
#GPIO.output(23, GPIO.High)								# schaltet den GPIO ein
#GPIO.output(23, GPIO.LOW)								# schaltet den GPIO aus

#GPIO.setup(24, GPIO.IN)
#if GPIO.input(24) == 0:								#Schalter ist an
#if GPIO.input(24) == 1:								#Schalter ist aus
         
# ------------------  -------------------  ------------------------  ---------------------  --------------
         
# Main function
def main():

    # Set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    
    print ('Definiere die GPIOs')
    print
    
    GPIO.setup(6, GPIO.IN)							    # Input - 1 hinteres Gleis
    GPIO.setup(13, GPIO.IN)							    # Input - 2 Mitte Vordergrund
    GPIO.setup(19, GPIO.IN)							    # Input - 3 rechts vorderes Gleis
    GPIO.setup(26, GPIO.IN)				    			# Input - Aus-Taster

    GPIO.setup(16, GPIO.OUT)							# Weiche rechts (von hinten)
    GPIO.setup(20, GPIO.OUT)							# Weiche links(von hinten)
    GPIO.setup(12, GPIO.OUT)							# WeichenSchaltStrom

    GPIO.setup(23, GPIO.OUT)							# Stopp-Stelle 1 hinteres Gleis
    GPIO.setup(24, GPIO.OUT)							# Stopp-Stelle 2 Vordergrund
    GPIO.setup(25, GPIO.OUT)							# Stopp-Stelle 3 vorderes Gleis
    GPIO.setup(18, GPIO.OUT)							# Signal
    
    print ('Start des Programms')
    print ('S   Stopp-Stellen werden aktiviert')
    GPIO.output(23, GPIO.LOW)							# Stopp 1 - hinteres Gleis
    GPIO.output(24, GPIO.LOW)							# Stopp 2 - Vordergrund
    GPIO.output(25, GPIO.LOW)							# Stopp 3 - vorderes Gleis
    GPIO.output(18, GPIO.HIGH)							# Signal: Halt

    print ("S   Hauptschalter fuer Weichen aus")         
    GPIO.output(12, GPIO.HIGH)							# Hauptschalter fuer Weichen aus
    
    #EsFaehrt == 0
    
    def Weichen_schalten():
        print
        print ('W   Weichen werden geschaltet')
        print
        GPIO.output(12, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(12, GPIO.HIGH)										# Hauptschalter fuer Weichen aus
        print "Weichen sind geschaltet"
         
    def Zugauswahl(x):
        print
        print ('A   Gleis bestimmen')
        items = ['1', '3']
        Gleis = random.sample(items, 1)
        print "A   Gleis " + Gleis[0]
       
        #random.seed()													# initialize random
        #Wartezeit = random.randint(1, 10)								# get random integer value between 1 and 7
        #if Wartezeit <5:
        #    Wartezeit = 0
        #print ("A   Zug Aufenthalt - Wartezeit "+ str(Wartezeit))
        #time.sleep(Wartezeit)

        if Gleis[0] == "1":
            print ("A   Schaltung Gleis 1")
            GPIO.output(16, GPIO.HIGH)  								# Weiche 1 aussen
            GPIO.output(20, GPIO.HIGH)  								# Weiche 3 aussen
            print ("A   Weichen_schalten")
            Weichen_schalten()
            GPIO.output(23, GPIO.HIGH)  								# Stopp 1 aus, Fahrt
            #time.sleep(15)
            #EsFaehrt == 1

        else:
            print ("A   Schaltung Gleis 3")
            GPIO.output(16, GPIO.LOW)  								# Weiche 1 innen
            GPIO.output(20, GPIO.LOW)  								# Weiche 3 innen
            print ("A   Weichen_schalten")
            Weichen_schalten()
            GPIO.output(25, GPIO.HIGH)  								# Stopp 3 aus, Fahrt
            #EsFaehrt == 3

    print
    print "Zugauswahl zum Programmstart aufrufen"         
    Zugauswahl(1)
    
    print
    print('endlose Abfrage der Sensoren ... ... ... ... ... ... ... ... ... ...')
    print

    # Main loop. Das Programm verweilt nun bis zu seinem Ende in dieser loop.
    while True:

        #print "test Input1"
        if GPIO.input(6) == 0:
          print ('Schalter 1')
          
        #print "test Input2"
        if GPIO.input(13) == 0:
          print ('Schalter 2')
          time.sleep(8)
          GPIO.output (18, GPIO.LOW)									#Signal: Fahrt
          time.sleep(3)
          GPIO.output (24, GPIO.HIGH)									#Stopp2: Fahrt
          time.sleep(8)
          GPIO.output (24, GPIO.LOW)									#Stopp2: Halt
          GPIO.output (18, GPIO.HIGH)									#Signal: Halt
          
        #print "test Input3"
        if GPIO.input(19) == 0:
          print ('Schalter 3')
          
        #print "test Input4"
        #if GPIO.input(26) == 0:
          #print ('Ausschalter')
          #os.system("sudo shutdown -h now -P 0")						# System herunterfahren
          

# If run this script directly from the shell, start it:
if __name__ == '__main__':
    try:
        main()
    # When 'Ctrl+C' is pressed 
    except:
        pass

    # Cleanup
    GPIO.cleanup()
