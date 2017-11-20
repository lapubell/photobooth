# photobooth

These two python programs will turn any linux laptop with working webcam and printer into a photobooth

These are python2 programs. check out the imports to know what you need to install. also, you'll want to plug in a high res webcam, and a printer. I'm using an Epson PM240 and it kinda sucks. Set up cups before you try and run these programs.

## How it works

The photobooth.py program is a pygame app that reads from the webcam, draws it on the screen, and after you hit a button it will capture 4 photos and save those to the file system. All along it is creating some HTML that is eventually turned into a PDF, which is dropped into the pdfs/ folder.

The print_looper.py program initializes cups, then sits in a loop forever. If there are any files in the pdfs/ folder (except the .gitkeep file) it will send that file to your printer. after the program gets the success message from cups, it moves the file from pdfs/ to printed_pdfs/ and starts over. don't ever put any files in the pdfs/ folder that isn't a print ready PDF.

There's no error checking.

There's no tests.

## Enjoy!
