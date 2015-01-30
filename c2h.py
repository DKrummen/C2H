import serial
#import MySQLdb
import urllib2
import re
import time

ip = "192.168.0.22"
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

#The base software that will drive the Close to Home Hub.  This will
#direct all of the modules to be changed should the need arise, and
#will update/download the status of the online database as needed.

#Serial Write Command List Reference:
#a = Lock Unlocked
#b = Lock Locked
#c = Inwall Off
#d = Inwall On
#e = 120v Off
#f = 120v On
#g = Computer Off
#h = Computer On
#i = Occupancy Off
#j = Occupancy On

lockoff = 'a'
lockon = 'b'
inwalloff = 'c'
inwallon = 'd'
voltoff = 'e'
volton = 'f'
compoff = 'g'
compon = 'h'
occoff = 'i'
occon = 'j'

lockstatus = 0
ser.write(lockoff)
urllib2.urlopen("http://"+ip+"/C2H/LockUpdate.php?part_status=0")

inwallstatus = 0
ser.write(inwalloff)
urllib2.urlopen("http://"+ip+"/C2H/InWallUpdate.php?part_status=0")

voltstatus = 0
ser.write(voltoff)
urllib2.urlopen("http://"+ip+"/C2H/120vUpdate.php?part_status=0")

compstatus = 0
ser.write(compoff)
urllib2.urlopen("http://"+ip+"/C2H/ComputerUpdate.php?part_status=0")

occstatus = 0
ser.write(occoff)
urllib2.urlopen("http://"+ip+"/C2H/OccupancyUpdate.php?part_status=0")

lockwork=0
inwallwork=0
voltwork=0
compwork=0
occwork=0

print "Just finished setting everything to 0!"

while 1:  #Mainloop

	#Checks to see if the Android App wants to change anything
	#It will return in the form of 10 20 30 40 50 if no changes needed.
	#Each 0 will become a 1 for the change that needs to be done.
	#1 = Lock
	#2 = InWall
	#3 = 120v
	#4 = Computer
	#5 = Occupancy

	f = urllib2.urlopen("http://"+ip+"/C2H/UpdatesQueryAll.php")
	z = f.read()
	o = ''.join([x for x in z if x.isdigit()])
	print o
	#o = '11213141511'
	o = o[:-1]
	print o

	clist = []

	clist.append(int(o[0]+o[1]))
	clist.append(int(o[2]+o[3]))
	clist.append(int(o[4]+o[5]))
	clist.append(int(o[6]+o[7]))
	clist.append(int(o[8]+o[9]))

	print clist[0]
	print clist[4]
	print clist[0:4]
	
	#The above list contains something like 10, 20, 31, 40, 51
	#Index values are 0=Lock, 1=InWall, 2=120v, 3=Computer, 4=Occupancy

	#Now we go through the Updates List and note any requests
	#We save the requests in temp variables such as lockwork
	#If lockwork is 1, then the user wants a lock changed

	if clist[0] == 11:
		lockwork = 1  #sets the flag to change the lock
		urllib2.urlopen("http://"+ip+"/C2H/LockPiUpdate.php")
		print "We've set the flag for the lock!"
		#The above line sets the value in the Updates table back to 0
	elif clist[0] == 10:
		lockwork = 0


	if clist[1] == 21:
		print "made it into the if!"
		inwallwork = 1 #sets the flag to change the inwall
		urllib2.urlopen("http://"+ip+"/C2H/InWallPiUpdate.php")
	elif clist[1] == 20:
		inwallwork = 0

	if clist[2] == 31:
		voltwork = 1
		urllib2.urlopen("http://"+ip+"/C2H/120vPiUpdate.php")	
	elif clist[2] == 30:
		voltwork = 0
	
	if clist[3] == 41:
		compwork = 1
		urllib2.urlopen("http://"+ip+"/C2H/ComputerPiUpdate.php")
	elif clist[3] == 40:
		compwork = 0
	
	if clist[4] == 51:
		occwork = 1
		urllib2.urlopen("http://"+ip+"/C2H/OccupancyPiUpdate.php")
	elif clist [4] == 50:
		occwork = 0
		
	#Now to apply the changes requested by the Android.

	if lockwork == 1:
		if lockstatus == 0:
			lockstatus = 1
			urllib2.urlopen("http://"+ip+"/C2H/LockUpdate.php?part_status=1")
			ser.write(lockon)
			lockwork = 0
			print "The lock was locked."
		elif lockstatus == 1:
			lockstatus = 0
			urllib2.urlopen("http://"+ip+"/C2H/LockUpdate.php?part_status=0")
			ser.write(lockoff)
			print "The lock was unlocked."
			lockwork = 0

	if inwallwork == 1:
		if inwallstatus == 0:
			inwallstatus = 1
			urllib2.urlopen("http://"+ip+"/C2H/InWallUpdate.php?part_status=1")
			ser.write(inwallon)
			inwallwork = 0
		elif inwallstatus == 1:
			inwallstatus = 0
			urllib2.urlopen("http://"+ip+"/C2H/InWallUpdate.php?part_status=0")
			ser.write(inwalloff)
			inwallwork = 0
	
	if voltwork == 1:
		if voltstatus == 0:
			voltstatus = 1
			urllib2.urlopen("http://"+ip+"/C2H/120vUpdate.php?part_status=1")
			ser.write(volton)
			voltwork = 0
		elif voltstatus == 1:
			voltstatus = 0
			urllib2.urlopen("http://"+ip+"/C2H/120vUpdate.php?part_status=0")
			ser.write(voltoff)
			voltwork = 0

	if compwork == 1:
		if compstatus == 0:
			compstatus = 1
			urllib2.urlopen("http://"+ip+"/C2H/ComputerUpdate.php?part_status=1")
			ser.write(compon)
			compwork = 0
		elif compstatus == 1:
			compstatus = 0
			urllib2.urlopen("http://"+ip+"/C2H/ComputerUpdate.php?part_status=0")
			ser.write(compoff)
			compwork = 0

	if occwork == 1:
		if occstatus == 0:
			occstatus = 1
			urllib2.urlopen("http://"+ip+"/C2H/OccupancyUpdate.php?part_status=1")
			ser.write(occon)
			occwork = 0
		elif occstatus == 1:
			occstatus = 0
			urllib2.urlopen("http://"+ip+"/C2H/OccupancyUpdate.php?part_status=0")
			ser.write(occoff)
			occwork = 0

	#Next, let's try to listen to the XBee modules in the house
	#so that we can determine their physical state

	#time.sleep(1)

	ser.flushInput()
	time.sleep(0.2)
	#buff = ser.read(20)
	buff = ""
	
	
	i = 0
	while i < len(buff):
		if buff[i] == "a":
			print "Got an A"
			lockstatus = 0
		elif buff[i] == "b":
			print "Got a B!"
			lockstatus = 1
		elif buff[i] == "c":
			print "Got a C!"
			inwallstatus = 0
		elif buff[i] == "d":
			inwallstatus = 1
		elif buff[i] == "e":
			voltstatus = 0
		elif buff[i] == "f":
			voltstatus = 1
		elif buff[i] == "g":
			compstatus = 0
		elif buff[i] == "h":
			compstatus = 1
		elif buff[i] == "i":
			occstatus = 0
		elif buff[i] == "j":
			occstatus = 1
		i = i + 1


	if lockstatus == 0:
		urllib2.urlopen("http://"+ip+"/c2h/LockUpdate.php?part_status=0")
	elif lockstatus == 1:
		urllib2.urlopen("http://"+ip+"/c2h/LockUpdate.php?part_status=1")		
	if inwallstatus == 0:
		urllib2.urlopen("http://"+ip+"/c2h/InWallUpdate.php?part_status=0")
	elif inwallstatus == 1:
		urllib2.urlopen("http://"+ip+"/c2h/InWallUpdate.php?part_status=1")
	if voltstatus == 0:
		urllib2.urlopen("http://"+ip+"/c2h/120vUpdate.php?part_status=0")
	elif voltstatus == 1:
		urllib2.urlopen("http://"+ip+"/c2h/120vUpdate.php?part_status=1")
	if compstatus == 0:
		urllib2.urlopen("http://"+ip+"/c2h/ComputerUpdate.php?part_status=0")
	elif compstatus == 1:
		urllib2.urlopen("http://"+ip+"/c2h/ComputerUpdate.php?part_status=1")
	if occstatus == 0:
		urllib2.urlopen("http://"+ip+"/c2h/OccupancyUpdate.php?part_status=0")
	elif occstatus == 1:
		urllib2.urlopen("http://"+ip+"/c2h/OccupancyUpdate.php?part_status=1")

	print "Loop!"
	#time.sleep(2)
