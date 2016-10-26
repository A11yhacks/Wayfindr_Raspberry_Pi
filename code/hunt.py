#a11yhacks treasure hunt activity
#Ben Mustill-Rose 10/09/2016
#Based on jcs 6/8/2014 & see blescan.py for additional credits

#Import all the modules we need
import blescan
import os
import sys
import bluetooth._bluetooth as bluez

#Set all the variables we'll be using
deviceID=0 #The ID of the Bluetooth device we'll be using minus hci. To get this run hciconfig and look for hci0, hci1 etc. Should always be hci0 unless you have more than one device
iBeaconUUID="b9407f30f5f8466eaff925556b57fe6d" #The UUID of your iBeacons not including any dashes that may be present
lastEncounterediBeacon="" #Keep track of the last iBeacon we encounted to prevent a scenario where we play the clue multiple times
iBeaconMajor="1000" #The major ID of your beacons (has to be a string otherwise just convert it later)

#Each beacon broadcasts several pieces of information which we're interested in. This method helps separate them out
#Todo: better exception handling
def parsePacket(packet):
 outputToReturn={} #A dictionary that will (hopefully) contain the output that we want to return
 parsedPacket=packet.split(",") #Create a list that contains the individual parts of the packet using a "," as the delimiter
 try: #Put this bit in an exception in case parsedPacket isn't an iBeacon (the below is very iBeacon specific code)
  outputToReturn["BDAddr"]=parsedPacket[0] #The Bluetooth address of the iBeacon
  outputToReturn["UUID"]=parsedPacket[1] #The UUID of the iBeacon
  outputToReturn["major"]=parsedPacket[2] #The major ID of the iBeacon
  outputToReturn["minor"]=parsedPacket[3] #The minor ID of the iBeacon
  #We receive 2 more pieces of data but it is not obvious what they are. Testing suggests that they are not TX / RSSI for example - we'll just ignore them for now
 except:
  raise
 else:
  return outputToReturn

#Play a clue sound
def playClue(id):
 try:
  os.system("aplay preclue.wav > /dev/null 2>&1")
  os.system("aplay "+str(id)+".wav > /dev/null 2>&1")
  os.system("aplay "+str(id)+".wav > /dev/null 2>&1")
 except:
  pass

#Try to create a socket
try:
 sock = bluez.hci_open_dev(deviceID)
 print("Socket created successfully!")
except:
 print("error accessing bluetooth device! Have you set deviceID correctly? Can not continu.")
 sys.exit(1)

#Set everything up in preperation for performing the scan
blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

#Make sure that we're sending audio via the 3.5 jack and that volume is at 100%
os.system("amixer cset numid=3 1 > /dev/null 2>&1")
os.system("amixer set \"PCM\",0 100% > /dev/null 2>&1")

#Play the introduction sound and the first clue
os.system("aplay startup.wav > /dev/null 2>&1")
playClue("intro")

while True:
 results=blescan.parse_events(sock, 10) #socket, maxNumberOfResults (default is 100)
 for packet in results:
  parsed=parsePacket(packet)
  try:
   if parsed["UUID"] == iBeaconUUID and parsed["major"] == iBeaconMajor and parsed["minor"] != lastEncounterediBeacon: #If we've encountered an Estimote iBeacon that has our major Id but is not the last one we delt with
    print(parsed["minor"])
    playClue(parsed["minor"])
    lastEncounterediBeacon=parsed["minor"]
    if parsed["minor"] == "12": os.system("sudo shutdown now")
  except:
   pass
