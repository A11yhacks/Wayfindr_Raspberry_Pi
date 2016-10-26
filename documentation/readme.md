#Treasure hunt documentation for mentors

This activity uses BLE beacons & Raspberry Pis to create a high-tech treasure hunt. The following features have been implemented out of the box:

* The treasure hunt script starts at boot negating the need for familiarity with Raspbian.
* Completely audible to enable headless operation.
* The first clue is sounded automatically. Subsequent clues are triggered when a given beacon is in range.
* Automatic shutdown when a given beacon is encountered to prevent file system corruption.

##Checklist:

* A BLE beacon for each location minus the starting one. Beacons should be compatible with Apple's iBeacon standard. We have had good results using Estimote (http://www.estimote.com) beacons in iBeacon mode.
* Enough Raspberry Pi 3's, speakers & power sources (E.G. power bars) for everyone. You may be able to use other SBC's so long as you are able to use Bluetooth & run Python but some of the code is Raspbian-specific. Older Pis should also work so long as a Bluetooth adaptor is present. NB: we had relatively good success in splitting participants into groups & giving each group a Pi, but if headphones are being used watch out for trailing wires!
* A modified `hunt.py` and `debug.py` (it is very unlikely that the supplied code will work out of the box for you).
* To ensure the smooth running of the activity it would be preferable if you are able to familiarise yourself with the location beforehand (see the planning a root section below).

##Understanding how iBeacons work:

Generically speaking, beacons emit a packet every NMS for clients to consume & act upon. The contents of said packets vary between standards and are largely beyond the scope of this document but it is however important to take a moment to develop a basic understanding of how iBeacon packets are structured in preparation for the activity.

The parts of an iBeacon "advertising packet" that we are concerned about are as follows:

* Universally unique identifier or UUID: 32 hexadecimal digits split into 5 groups.
* Major: an integer between 0 & 65535 inclusive.
* Minor: an integer between 0 & 65535 inclusive.

NB: there are other potentially useful pieces of information in a packet although due to time constraints we have not taken these into account as of yet. We are however always open to pull requests.

###A worked example:

Suppose you are a supermarket chain who wishes to provide an app-based indoor navigation experience for your customers. Your chain owns multiple supermarkets & within each supermarket there are multiple isles of items. In this scenario, the above values would most likely be mapped similarly to the following:

* UUID represents your chain.
* Major represents a given supermarket.
* Minor represents an isle within a supermarket.

Note that in this instance minor values would not have to be exclusive across supermarkets so long as the combination of the UUID, major & minor values are able to uniquely identify a beacon.

As you may have surmised, the iBeacon standard is well-suited to larger role outs and is rather overkill for this activity. For our implementation we chose consistent UUID & major values, but if your location has multiple floors for example, there is no reason why major could not denote a floor & minor a specific location on said floor.

##Beacon setup:

The following steps are based on our experiences with Estimote beacons but the steps should largely be the same regardless of the manufacturer:

1. Change the name of all of your beacons to something sensible. We chose Beacon1, Beacon2, ... Beacon11, Beacon12. Note that these names are only used internally & aren't transmitted in advertising packets. Estimote lets you do this via their app or the cloud control panel.
2. Take each beacon & write its name on it for easy identification later. We found the best way to do this was to move a beacon away from the rest of the beacons then use the Estimote app to show nearby beacons.
3. For each beacon you should additionally:
  1. Decrease its range. Estimote lets you specify the broadcast power as a percentage or in feet - we found that 0 percent (3 feet) was a sensible starting range.
  2. Change the major & minor values as per your requirements.

##Setting up a Pi:

These steps assume that you have a working Raspbian install & you are reasonably familiar with how it operates. Steps 1, 2 and 3 should be completed before you carry out the steps in the "planning a root" section. Steps 5 & 6 should only be performed when you are happy with your root & you have modified hunt.py to work with your setup.

1. Copy the 3 .py files to a sensible location.
2. For debugging during the planning root sections we highly recommend you connect the Pi to a wireless network.
3. Run the following commands to install dependencies:
  1. `sudo apt-get update`
  2. `sudo apt-get install python-bluez`
4. Copy all of the sounds into the directory in step 1.
5. We now need to make hunt.py run when the Pi boots. To do this run `sudo raspi-config` Choosing options 3 then b4.
6. Edit `/home/pi/.config/lxsession/LXDE-pi/autostart` Where pi is the name of your user account. You will need to `sudo` to modify this file. Add `*/usr/bin/sudo python /home/pi/hunt.py`.

##Planning a root:

The effectiveness of wireless transmition varies drastically depending on the devices in use, other nearby devices & your location. It is there for important to resist the urge to assume that once you have everything working in one location it will perform even remotely identically at the location you wish to run the activity in.
We found that a treasure hunt that contained 11 clues took just over 5 hours of setup for 2 people with very few interruptions. Our experiences suggest that more people would not necessarily decrease the setup time but familiarity with the location may do. We recommend that a dry run is carried out the day before the event & that the beacons are left in situ overnight once everything is setup if at all possible.

1. Place the beacons in the desired locations.
2. We now need to make sure that the range of the beacons is appropriate & that none of them overlap; this is probably the longest & most frustrating part of the setup process but stick with it! You will need a way of receiving output from a Pi whilst walking about; we used a laptop connected via SSH via a phone that was broadcasting a wireless network. Once everything's working, run `python debug.py` and consult the output. This script is a minimal version of the treasure hunt which, as the name implies, is designed for debugging your root. When a beacon is in range its major & minor values are printed, although if multiple packets are received in a ro from one beacon only the first is displayed. If you have modified a given beacon and wish to test its range again, you will need to walk to the sight of another beacon then walk back to the original one. The Shutdown functionality has not been implemented in this script.
3. Walk your root taking care to pass the clues in the same order that the participants will do whilst checking that you are happy with the performance of the beacons. Pay particular attention to scenarios where 2 beacons are close to each other, consulting the output from the Pi to make sure that it is not possible for both of them to be detected at the same time. If this does happen, experiment with repositioning one of the beacons slightly - E.G. high up, low down, inside a cupboard, behind a door etc. Please also be mindful of scenarios where participants may pass a clue on root to another one - E.G. try to avoid clue 5 sounding when participants are on their way to clue 2. We found the Estimote companion app useful for modifying the range of individual beacons on the go for scenarios where "3 feet" was actually considerably less due to the environment.
4. Once you're happy with everything you will have most likely walked the root a large number of times and will have started to question why you committed to doing the activity in the first place. Never the less, it is important to carry out one last check by starting at the beginning & walking it through to confirm that no more adjustments need to be made. Keep on doing this until you can walk the root without changing anything.

##Supplied .py files:

3 .py files are supplied with this activity:

* bluescan.py - methods to scan for nearby BLE devices. Participants need not concern themselves with the content of this file.
* debug.py - a minimal implementation of the treasure hunt activity for debugging purposes.
* hunt.py - the main treasure hunt file that participants should modify.

##Understanding hunt.py:

Whilst the code is well commented, a breakdown of the various methods & sections of the file can be found below:

1. We first start by importing the various modules & files that our program needs to function.
2. Next we set some variables we'll be using. You will need to change iBeaconUUID, iBeaconMajor and possibly deviceID if your SBC has more than one Bluetooth adaptor. If not 0 is a sensible default.
3. The packets that beacons broadcast contain many different pieces of information. To make it easier to determine which beacon we have encountered later on in the code, we have created a parsePacket method which returns a dictionary containing the various values.
4. When we encounter one of our beacons we need to play the preclue sound then play the clue twice. We've put this functionality into a playClue method.
5. We next perform a number of setup tasks that are required before we go any further:
  1. Attempt to create a socket (make a connection) to our Bluetooth adaptor
  2. Set some parameters relating to the Bluetooth scanning that we'll be doing
  3. Make sure that the Pi is sending audio through the 3.5 audio jack & set volume to 100%
6. Now that everything's been set up it's time to start playing sounds! We first play the startup sound, then we call playClue to play the introduction sound.
7. We then enter a while loop where a few different things happen:
  1. A scan is performed, the results of which are saved in a list called results.
  2. For each of our results we then:
    1. Parse it so we can easily work out which beacon we've encountered.
    2. Check if the UUID & major values of the packet match those that we set above and that the beacon we've found isn't the same one as the last one we found. If this is the case we do a number of things:
      1. Play a clue using the minor value of the packet to determine which clue we need to play.
      2. Keep track of which beacon we've just encountered.
      3. Shutdown the Pi if the beacon is the last one in the hunt.

##Creating the sounds:

The activity relies on a number of different sounds in order to function:

* x.wav - played when a beacon with a minor value of x is encountered.
* preclue.wav - played before each clue.
* startup.wav - played when all the setup is complete.
* intro.wav - the introduction sound. In our implementation this was a clue.

Use a sound recorder of your choice - E.G. Audacity to record the various sounds taking care to ensure that the names are exactly like the ones above.