import gpiozero
import time
from signal import pause

btn = gpiozero.Button(2)

pump = gpiozero.LED(3, active_high=False)
valve = gpiozero.LED(26)
kettle = gpiozero.LED(5)

pumpdelay = 2 #time in secs for the pump to fill a cup of water
kettledelay = 60 #time in secs for kettle to boil + safety margin
valvedelay = 5 #time in secs for the valve to empty water into a cup

def makeACuppa():
    pump.on()
    time.sleep(pumpdelay)
    pump.off()

    kettle.on()
    time.sleep(kettledelay)
    kettle.off()

    valve.on()
    time.sleep(valvedelay)
    valve.off()

btn.when_pressed = makeACuppa

pause()
