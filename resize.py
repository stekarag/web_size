# This Python file uses the following encoding: utf-8
import re
import os
import time
from PIL import Image

# To-do: add prompt for max dimension

virtual = 0
debug = 1

positive = [
			"",
			"Y", "YES", "TRUE", "PROCEED", "POSITIVE", "OF COURSE", "NAI",
			"ΝΑΙ", "ΑΣΦΑΛΩΣ", "ΦΥΣΙΚΑ", "ΤΕΛΕΙΑ", "ΒΕΒΑΙΑ", "ΒΕΒΑΙΩΣ", "1"]

filetype = re.compile('jpg$')
file_format = re.compile('\.[a-z]+$')

def resize(image_f):
	# use RE to isolate filename from suffix
	filename = re.split(r'\.jpg$', image_f)[0]
	if debug: 
		print(f"  Το όνομα του αρχείου είναι {filename}")

	image = Image.open(image_f)
	# compare width to height
	width, height = image.size
	height_f, width_f = 0, 0
	if debug: 
		print(f"  Αρχικές διαστάσεις αρχείου {width}x{height}")
	# scale bigger to 800 and other accordingly
	if (width > height): 
		proportion = (width - 800)/width
		width_f = 800
		height_f = int(height - proportion*height)
	elif (width < height):
		proportion = (height - 800)/height
		height_f = 800
		width_f = int(width - proportion*width)
	elif (width is height):
		height_f = 800
		width_f = 800
	else:
		# error: skip || report
		pass

	if debug: 
		print(f"  Τελικές διαστάσεις αρχείου {width_f}x{height_f}")
	dim = "("+str(width_f)+","+str(height_f)+")"

	if not virtual:
		# save image 
		data = list(image.getdata())
		image_wo = Image.new(image.mode, image.size)
		image_wo.putdata(data)
		image_final = image_wo.resize(dim)
		image_final_name = filename+"_web.png"
		image_final.save(image_final_name)

# Prompt for virtual or actual copy
bool = input("Θέλετε να γίνει πραγματική αντιγραφή των αρχείων;")
boolAns = ""
if bool.upper() in positive:
	virtual = 0
	boolAns = "κανονικά."
else:
	virtual = 1
	boolAns = "εικονικά."
print(f"Το πρόγραμμα θα τρέξει {boolAns}")

sup = input("Θέλετε την αναφορά του προγράμματος στη οθόνη;")
supAns = ""
if sup.upper() in positive:
	debug = 1
else:
	debug = 0
	supAns = "δεν "
print(f"Το πρόγραμμα {supAns}θα επιστρέφει λεπτομέρειες της κατάστασής του.")

if not debug:
	os.system("@echo off") # turn off command output

parentname = os.getcwd()
parentfolder = os.listdir()
for counter, folder in enumerate(parentfolder):
	if debug:
		print(f"Ελέγχεται ο φάκελλος ή αρχείο {folder}")
	
	x = file_format.search(folder)

	if x:  # skip this repetition if not a folder
		continue
		if debug: print(f"Το αρχείο {folder} παραλείπεται.")
	os.chdir(folder)

	if debug:
		print(f"Επεξεργάζεται ο φάκελλος: {folder}")

	dir = os.listdir()

	for archive in dir:
		x = filetype.search(archive)
		if x:
			if debug:
				print(f' Σμίκρυνση του {archive}.')
			resize(archive)
				
	os.chdir(parentname)
	if debug:
		print("Ο φάκελλος ", folder, " είναι έτοιμος!")

	# def for bar also, count files as well
	p = int(round(((counter+1)/len(parentfolder)), 2)*100)
	d = int(p/2)
	rCounter = 50 - d
	stars = ''
	while (d > 0):
		stars = stars + '\u25AE'
		d -= 1
	while (rCounter > 0):
		stars = stars + ' '
		rCounter -= 1
	bar = '[' + stars + ']'
	if not debug:
		print(bar + ' ' + str(p) + '% ολοκληρώθηκε!', end="\r", flush=True)
		time.sleep(0.2)

print("\nΈτοιμα όλα τα αρχεία!")
