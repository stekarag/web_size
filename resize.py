# This Python file uses the following encoding: utf-8
import re
import os
import time
from PIL import Image

# To-do: add prompt for max dimension, rename file that have space to underscore

virtual = 0
debug = 1
MAXSIZE = 800

positive = [
			"",
			"Y", "YES", "TRUE", "PROCEED", "POSITIVE", "OF COURSE", "NAI",
			"ΝΑΙ", "ΑΣΦΑΛΩΣ", "ΦΥΣΙΚΑ", "ΤΕΛΕΙΑ", "ΒΕΒΑΙΑ", "ΒΕΒΑΙΩΣ", "1"]

filetype = re.compile('(\.((pn)|(jpe?))g$)') # need to add support for capital file extensions
file_format = re.compile('\.[A-Za-z]+$')

def resize(image_f):
	# use RE to isolate filename from suffix
	filename = re.split(filetype, image_f)[0] # or png or jpeg, r'\.jpg$'
	suffix = re.split(filetype, image_f)[1]
	if debug: 
		print(f"  Το όνομα του αρχείου είναι {filename}")
		print(f"  Η κατάληξη του αρχείου είναι {suffix}")

	image = Image.open(image_f)
	# compare width to height
	width, height = image.size
	height_f, width_f = 0, 0
	if debug: 
		print(f"  Αρχικές διαστάσεις αρχείου {width}x{height}")
	# scale bigger to MAXSIZE and other accordingly
	if (width > height): 
		proportion = (width - MAXSIZE)/width
		width_f = MAXSIZE
		height_f = int(height - proportion*height)
	elif (width < height):
		proportion = (height - MAXSIZE)/height
		height_f = MAXSIZE
		width_f = int(width - proportion*width)
	else:
		height_f = MAXSIZE
		width_f = MAXSIZE

	if debug: 
		print(f"  Τελικές διαστάσεις αρχείου {width_f}x{height_f}")
	dim = tuple([width_f,height_f])

	if not virtual:
		# save image 
		if 'n' in suffix:
			image = image.convert('RGB')
		data = list(image.getdata())
		image_wo = Image.new(image.mode, image.size)
		image_wo.putdata(data)
		image_final = image_wo.resize(dim)
		suffix = '.jpg'
		image_final_name = filename+"_web"+suffix
		image_final.save(image_final_name)
		print(f"  Σβήνεται το αρχείο {image_f}") # weird malfunction with capital filenames
		os.remove(image_f)

# Prompt for virtual or actual copy
print("Το πρόγραμμα ελέγχει τους υποφακέλλους για αρχεία εικόνας και τα προσαρμόζει σε διαστάσεις για το διαδύκτιο. Όλες οι εικόνες πρέπει να περιέχονται σε υποφακέλλους αλλιώς θα αγνοηθούν.")
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
				print(f' Σμίκρυνση του {archive}')
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
