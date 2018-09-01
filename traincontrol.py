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
    
    GPIO.setup(24, GPIO.IN)							    # Input - Gleis 1 Ausfahrt
    GPIO.setup(18, GPIO.IN)							    # Input - Gleis 2 Ausfahrt
    GPIO.setup(22, GPIO.IN)							    # Input - Gleis 1 Einfahrt
    GPIO.setup(4, GPIO.IN)				    			# Input - Gleis 2 Einfahrt
    
    # weisse Kabel, links unten
    GPIO.setup(6, GPIO.OUT)							    # Relais 1/8 - Stopp 2
    GPIO.setup(13, GPIO.OUT)							# Relais 2/8 - Stopp 1
    GPIO.setup(19, GPIO.OUT)							# Relais 3/8 - Stopp 3
    GPIO.setup(26, GPIO.OUT)							# Relais 4/8 - Stopp 4
    
    # gelbe Kabel, rechts oben 
    GPIO.setup(27, GPIO.IN)							    # Input Ausschalter
    #GPIO.setup(23, GPIO.IN)							    # Input 1 blau
    #GPIO.setup(24, GPIO.IN)						    	# Input 2 weiss
    GPIO.setup(25, GPIO.OUT)							# Relais 8/8 Hauptschalter fuer 4er-Relais
    
    # hellgelbe Kabel, rechts unten 
    GPIO.setup(12, GPIO.OUT)						    # Relais 1/4 - Weiche 1
    GPIO.setup(16, GPIO.OUT)							# Relais 2/4 - Weiche 2
    GPIO.setup(20, GPIO.OUT)							# Relais 3/4 - Weiche 3
    GPIO.setup(21, GPIO.OUT)							# Relais 4/4 - Weiche 4

    print ('Start des Programms')
    print ('S   Stopp-Stellen werden aktiviert')
    GPIO.output(6, GPIO.LOW)							# Stopp 1
    GPIO.output(13, GPIO.HIGH)							# Stopp 2
    GPIO.output(19, GPIO.LOW)							# Stopp 3
    GPIO.output(26, GPIO.LOW)							# Stopp 4
    
    print ("S   Hauptschalter fuer Weichen aus")         
    GPIO.output(25, GPIO.HIGH)											# Hauptschalter fuer Weichen aus
    
    def Weichen_schalten():
        print
        print ('W   Weichen werden geschaltet')
        print
        GPIO.output(25, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(25, GPIO.HIGH)										# Hauptschalter fuer Weichen aus  
    
    belegt1 = "0"    													# Startkonfiguration Gleis 1
    belegt2 = "1"    													# Startkonfiguration Gleis 1
    belegt3 = "1"    													# Startkonfiguration Gleis 1
    
    def Zugauswahl(x):
        print
        print ('A   Aussfahrt bestimmen')
        
        if belegt1 == 1:
           if belegt2 == 1:
              items = ['1', '2']
           else:
              items = ['1', '3']
        else:
           items = ['2', '3']
           
        Ausfahrt = random.sample(items, 1)
        print "A   Ausfahrt Gleis " + Ausfahrt[0]
       
        #random.seed()													# initialize random
        #Wartezeit = random.randint(1, 10)								# get random integer value between 1 and 7
        #if Wartezeit <5:
        #    Wartezeit = 0
        #print ("A   Zug Aufenthalt - Wartezeit "+ str(Wartezeit))
        #time.sleep(Wartezeit)
    
        if Ausfahrt[0] == "1":
            print ("A   Schaltung Ausfahrt 1")
            GPIO.output(12, GPIO.LOW)									# Weiche 1 gerade
            print ("A   Weichen_schalten")
            Weichen_schalten()
            GPIO.output(13, GPIO.LOW)									# Stopp 1 aus, Signal Fahrt
            time.sleep(15)
            print ("A   Signal 1 auf Halt")
            GPIO.output(13, GPIO.HIGH)									# Stopp 1 an, Signal Halt
            belegt1 == 0
            
        elif Ausfahrt[0] == "2":
            print ("A   Schaltung Ausfahrt 2")
            GPIO.output(16, GPIO.LOW)									# Weiche 2 gerade
            GPIO.output(12, GPIO.HIGH)									# Weiche 1 Bogen
            print ("A   Weichen_schalten")
            Weichen_schalten()
            GPIO.output(13, GPIO.LOW)									# Stopp 2 aus
            belegt2 == 0
            
        elif Ausfahrt[0] == "3":
            print ("A   Schaltung Ausfahrt 3")
            GPIO.output(16, GPIO.HIGH)									# Weiche 2 Bogen
            GPIO.output(12, GPIO.HIGH)									# Weiche 1 Bogen
            print ("A   Weichen_schalten")
            Weichen_schalten()
            GPIO.output(19, GPIO.HIGH)									# Stopp 3 aus
            belegt3 == 0

        #print      
        #print ('E   Einfahrt bestimmen')
        #print ("E   Bitte warten ... ")
        #time.sleep(15)

        if belegt1 == 1:
           items = ['2', '3']
        elif belegt2 == 1:
           items = ['1', '3']
        else:
           items = ['1', '2']
           
        Einfahrt = random.sample(items, 1)  
        print "E   Einfahrt auf Gleis " + Einfahrt[0]
        
        if Einfahrt[0] == "1":
           print ("E   Einfahrt auf Gleis 1")
           GPIO.output(21, GPIO.LOW)									# Weiche 4 gerade   
           GPIO.output(13, GPIO.HIGH)									# Stopp 1 an
           belegt1 == 1

        if Einfahrt[0] == "2":											
           print ("E   Einfahrt auf Gleis 2")
           GPIO.output(21, GPIO.HIGH)									# Weiche 4 Bogen
           GPIO.output(20, GPIO.LOW)						  			# Weiche 3 gerade
           GPIO.output(13, GPIO.LOW)									# Stopp 2 an
           belegt2 == 1
           
        if Einfahrt[0] == "3":
           print ("E   Einfahrt auf Gleis 3")
           GPIO.output(12, GPIO.HIGH)									# Weiche 4 Bogen
           GPIO.output(12, GPIO.HIGH)									# Weiche 3 Bogen
           GPIO.output(26, GPIO.LOW)						   			# Stop 3 an
           belegt3 == 1
           
        print ("E   Weichen_schalten")
        Weichen_schalten()
        
        print
               
    print
    print "Zugauswahl zum Programmstart aufrufen"         
    Zugauswahl(1)
    
    print
    print('endlose Abfrage der Sensoren ... ... ... ... ... ... ... ... ... ...')
    print

    # Main loop. Das Programm verweilt nun bis zu seinem Ende in dieser loop.
    while True:
        print "test1"
                 
        if GPIO.input(24) == 0:
          print ('Schalter 1 neu ... Gleis 1, Ausfahrt')
          
        print "test2"
          
        if GPIO.input(4) == 0:
          print ('Schalter 4 neu ... Gleis 2 Einfahrt')
          
        print "test3"
          
        if GPIO.input(18) == 0:
          print ('Schalter 2 neu ... Gleis 2 Ausfahrt')
          
        print "test4" 
        if GPIO.input(22) == 0:
          print ('Schalter 3 neu ... Gleis 1 Einfahrt')
          

        print "test5"

        if GPIO.input(27) == 0:
          print ('Ausschalter')
          os.system("sudo shutdown -h now -P 0")						# System herunterfahren
          

# If run this script directly from the shell, start it:
if __name__ == '__main__':
    try:
        main()
    # When 'Ctrl+C' is pressed 
    except:
        pass

    # Cleanup
    GPIO.cleanup()
