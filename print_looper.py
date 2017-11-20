#! /usr/bin/python

import cups
import sys
import os
import time

# printer stuff
conn = cups.Connection()
ps = conn.getPrinters()
printer = ps.keys()[0]					# get whatever printer you need to get. this machine only has one.
# basedir = "/home/lapubell/Downloads/photobooth/"
basedir = "/home/lapubell/programming/python/photobooth/"

while 1:
	pdffiles = os.listdir(basedir + "pdfs")

	if (len(pdffiles) > 1):
		pdffiles.sort()

		for file in pdffiles:
			if file == ".gitkeep":
				print "skipping .gitkeep"
				continue
				
			printJob = conn.printFile(printer, basedir + "pdfs/" + file, "Printing Message", {})
			while conn.getJobAttributes(printJob)["job-state"] < 9:
				print "still printing " + file
				time.sleep(10)

			os.system("mv " + basedir + "pdfs/" + file + " " + basedir + "printed_pdfs/" + file)
			print "finished!"

	else:
		print "nothing to print"

	time.sleep(5)

