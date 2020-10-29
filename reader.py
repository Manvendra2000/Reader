# Import libraries 
from PIL import Image 
import pytesseract 
import sys
from sys import stderr
from pdf2image import convert_from_path 
import os
import subprocess
from pathlib import Path

# Locate Tesseract installation, either automatically from PATH or from the TESSERACT_CMD environment variable
which = 'which'
if os.name == 'nt':
	which = 'where.exe'
rc = None
with open(os.devnull) as nul:
	rc = subprocess.call([which, pytesseract.pytesseract.tesseract_cmd], stdout=nul, stderr=nul)
if rc != 0:
	print('Tesseract not found in PATH. Checking TESSERACT_CMD...')
	tess_cmd = os.environ.get('TESSERACT_CMD', '')
	if not Path(tess_cmd).is_file():
			print('Invalid value of TESSERACT_CMD! Set its value to the location of the "tesseract" executable, or add it to PATH.', file=stderr)
			sys.exit(1)
	else:
		print('Using TESSERACT_CMD.')
		pytesseract.pytesseract.tesseract_cmd = tess_cmd
else:
	print('Tesseract found in PATH.')

# Get the file information
PDF_file = input('Enter the name of the file: ')

# Start the application
image_counter = 0
if Path(PDF_file).is_file():
	# Part #1: Converting PDF to images
	
	# Store all the pages of the PDF in a variable 
	pages = convert_from_path(PDF_file, 500)

	# Counter to store images of each page of PDF to image
	image_counter = 1

	# Create output folders if they don't exist
	dirs = [os.path.join(os.getcwd(), 'out', 'imgs'), os.path.join(os.getcwd(), 'out', 'txt')]
	for directory in dirs:
		if not Path(directory).is_dir():
			os.makedirs(directory)

	# Iterate through all the pages stored above
	print('Generating images from pages...')
	for page in pages:
		# Declaring filename for each page of PDF as JPG 
		# For each page, filename will be: 
		# PDF page 1 -> page_1.jpg 
		# PDF page 2 -> page_2.jpg 
		# PDF page 3 -> page_3.jpg 
		# .... 
		# PDF page n -> page_n.jpg 
		filename = f'page_{image_counter}.jpg'

		# Save the image of the page in system
		page.save(os.path.join(dirs[0], filename), 'JPEG')
		print(f'{os.path.join(dirs[0], filename)} created!')

		# Increment the counter to update the filename for the next page
		image_counter += 1
else:
	print('Error: File inaccessible!', file=stderr) # Couldn't read the file
	sys.exit(2)

# Part #2 - Recognizing text from the images using OCR 

# Variable to get count of total number of pages 
filelimit = image_counter - 1

# Creating a text file to write the output 
outfile = os.path.join(dirs[1], "out_text.txt")

# Open the file in append mode so that 
# All contents of all images are added to the same file 
with open(outfile, "a") as f:
	print(f'Writing OCR output to {outfile}...')

	# Iterate from 1 to total number of pages
	for i in range(1, filelimit + 1):
		# Set filename to recognize text from 
		# Again, these files will be: 
		# page_1.jpg 
		# page_2.jpg 
		# .... 
		# page_n.jpg 
		filename = f'page_{i}.jpg'
			
		# Recognize the text as string in image using pytesserct 
		text = str((pytesseract.image_to_string(Image.open(os.path.join(dirs[0], filename)))))

		# The recognized text is stored in variable text 
		# Any string processing may be applied on text 
		# Here, basic formatting has been done: 
		# In many PDFs, at line ending, if a word can't 
		# be written fully, a 'hyphen' is added. 
		# The rest of the word is written in the next line 
		# Eg: This is a sample text this word here GeeksF- 
		# orGeeks is half on first line, remaining on next. 
		# To remove this, we replace every '-\n' to ''. 
		text = text.replace('-\n', '')	 

		# Finally, write the processed text to the file. 
		f.write(text)
		print(f'Identification from {os.path.join(dirs[0], filename)} completed.')
	
	print(f'Output written to {outfile}!')