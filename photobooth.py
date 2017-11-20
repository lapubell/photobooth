#! /usr/bin/python

import sys
import os
import pygame
import pygame.camera
import time
import cups
from xhtml2pdf import pisa

html_start = """
<html>

<style>
@page {
  size: a6;
  margin: 0.38cm;
}

img {
	width: 160px;
	padding-right: 20px;
}

#image_container {
	width: 410px;
}
</style>

<body>
<div id='image_container'>
"""
html = html_start

pygame.init()
pygame.camera.init()

clock = pygame.time.Clock()

# cam = pygame.camera.Camera("/dev/video0", (640,480))
pic_size = (1280,720)
forscreen = (810, 500)
thumbnail = (128,72)
cam = pygame.camera.Camera("/dev/video1", pic_size)
cam.start()

size = width, height = 900, 650
screen = pygame.display.set_mode(size)

screen.fill( (255, 255, 255) )

# hide the mouse
pygame.mouse.set_visible(False);

photo_num = 999							#too high to trigger
holder = 999							#too high to trigger
app_status = "active"					#use this as a toggle active vs. printing
timestamp = str(time.time())

# printer stuff
# conn = cups.Connection()
# ps = conn.getPrinters()
# printer = ps.keys()[0]					# get whatever printer you need to get. this machine only has one.
# basedir = "/home/lapubell/Downloads/photobooth/"
basedir = "/home/lapubell/programming/python/photobooth/"


# countdown images
number_3 = pygame.image.load(basedir + "assets/Countdown_3.png").convert()
number_2 = pygame.image.load(basedir + "assets/Countdown_2.png").convert()
number_1 = pygame.image.load(basedir + "assets/Countdown_1.png").convert()
number_0 = pygame.image.load(basedir + "assets/Countdown_Flash.png").convert()


# printing image
printing_graphic = pygame.image.load(basedir + "assets/PrintingScreen.jpg").convert()

# pdf stuff
filename = basedir + "print.pdf"

def save_and_show(number):
	global html
	photo = cam.get_image()
	# photo = pygame.transform.rotate(photo, 180)

	pygame.image.save(photo, basedir + "saved_images/" + timestamp + "_" + str(number) +".jpg")
	html += "<img src='" + basedir + "saved_images/" + timestamp + "_" + str(number) +".jpg' style='float: left;' />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n"
	html += "<img src='" + basedir + "saved_images/" + timestamp + "_" + str(number) +".jpg' style='float: right;' />\n<br><br>\n\n"

	return photo

while 1:
	clock.tick(60) # set FPS

	# get keyboard input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			cam.stop()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			print event.key
			
			if event.key == 27:
				cam.stop()
				sys.exit()

			if event.key == 264 or event.key == 32:

				# check application state
				if app_status == "active":

					# start capture
					app_status = "printing"
					
					if photo_num > 4:
						holder = 0
						photo_num = 1
						timestamp = str(time.time())

	# get image from camera
	image = cam.get_image()
	imageFlip = pygame.transform.flip(image, True, False)
	imageFlip = pygame.transform.scale(imageFlip, forscreen)

	rect = image.get_rect()
	rect = rect.move([10,10])

	screen.blit(imageFlip, rect)

	if holder < 40 and photo_num < 5:
		if holder > 25:
			screen.blit(number_1, rect)

		if holder <  25:
			if holder > 12:
				screen.blit(number_2, rect)

			if holder < 12:
				screen.blit(number_3, rect)
		holder += 1
	elif holder < 41:
		screen.blit(number_0, rect)
		holder += 1
	else:
		if photo_num < 5:
			if photo_num == 1:
				html = html_start
				
			saved_photo = save_and_show(photo_num)
			saved_photo = pygame.transform.scale( saved_photo, thumbnail )
			saved_photo = pygame.transform.flip( saved_photo, True, False )
			thumb_rect = saved_photo.get_rect()

			if photo_num == 1:
				thumb_rect = thumb_rect.move( [10,520] )

			if photo_num == 2:
				thumb_rect = thumb_rect.move( [212,520] )

			if photo_num == 3:
				thumb_rect = thumb_rect.move( [415,520] )

			if photo_num == 4:
				thumb_rect = thumb_rect.move( [618,520] )

			screen.blit( saved_photo, thumb_rect )

			holder = 0
			photo_num += 1

			if photo_num == 5:
				# add generic photo at the bottom
				html += "<img src='" + basedir + "assets/PhotoStrip_Graphic.jpg' style='float: left;' />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n"
				html += "<img src='" + basedir + "assets/PhotoStrip_Graphic.jpg' style='float: right;' />\n<br><br>\n\n"

				html += "</div></body></html>" #finish off the html
				# print html
				pdf = pisa.CreatePDF(html, file(filename, "w"))
				pdf.dest.close()

				# conn.printFile(printer, filename, "Printing Message", {})
				app_status = "active"
				print "finished running the batch at " + str(timestamp)

				os.system("cp " + basedir + "print.pdf " + basedir + "pdfs/" + timestamp + ".pdf")

				screen.blit(printing_graphic, rect)
				pygame.display.flip()

				pygame.time.wait(145*100)

				screen.fill( [255,255,255] )
		else:
			photo_num = 999
			holder = 999

	pygame.display.flip()
