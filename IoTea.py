#!/usr/bin/env python

import gpiozero
import time
from signal import pause
from imapclient import IMAPClient

btn = gpiozero.Button(2)

pump = gpiozero.LED(3, active_high=False)
valve = gpiozero.LED(26)
kettle = gpiozero.LED(5)

HOSTNAME = 'imap.gmail.com'
USERNAME = 'YOUR_GMAIL_USERNAME'
PASSWORD = 'YOUR_GMAIL_PASSWORD'
MAILBOX = 'Inbox'

pumpdelay = 22 #time in secs for the pump to fill a cup of water
kettledelay = 120 #time in secs for kettle to boil + safety margin
valvedelay = 20 #time in secs for the valve to empty water into a cup


def makeACuppa():
    print("Underoing Cuppa Manufacture.")
    
    pump.on()
    time.sleep(pumpdelay)
    pump.off()

    kettle.on()
    time.sleep(kettledelay)
    kettle.off()

    valve.on()
    time.sleep(valvedelay)
    valve.off()

    print("Cuppa manufacture done. thank you")


 
DEBUG = True
 
MAIL_CHECK_FREQ = 60 # check mail every 60 seconds

def setup():
    #runs the following code once to update the minimum unread value
    server = IMAPClient(HOSTNAME, use_uid=True, ssl=True)
    server.login(USERNAME, PASSWORD)

    print('Logging in as ' + USERNAME)
    select_info = server.select_folder(MAILBOX)
    print('%d messages in INBOX' % select_info['EXISTS'])

    folder_status = server.folder_status(MAILBOX, 'UNSEEN')
    newmails = int(folder_status['UNSEEN'])
    prevMails = newmails
    return prevMails

 
def loop(prev):
    server = IMAPClient(HOSTNAME, use_uid=True, ssl=True)
    server.login(USERNAME, PASSWORD)
 
    if DEBUG:
        print('Logging in as ' + USERNAME)
        select_info = server.select_folder(MAILBOX)
        print('%d messages in INBOX' % select_info['EXISTS'])
 
    folder_status = server.folder_status(MAILBOX, 'UNSEEN')
    newmails = int(folder_status['UNSEEN'])
 
    if DEBUG:
        print "You have", newmails, "new emails!"
 
    if newmails > prev:
        makeACuppa()
    time.sleep(MAIL_CHECK_FREQ)
    return newmails

prevMails = setup()
while True:
    prevMails = loop(prevMails)
btn.when_pressed = makeACuppa
pause()


