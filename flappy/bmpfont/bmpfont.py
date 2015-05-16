
# bmpfont.py
# By Paul Sidorsky - Freeware

"""Provides support for bitmapped fonts using pygame.

Font Index File Descrption

bmpfont lets you define where each character is within the bitmap,
along with some other options.	This lets you use a bitmap of any
dimension with characters of any size.	The file where the position
of each character is defined is called the font index file.  It is
a simple text file that may contain the lines listed below.
Whitespace is ignored, but the keywords are case-sensitive.
NOTE:  Blank lines and comments are not allowed!

bmpfile filename
- filename is the full name (with optional path) of the bitmap file
  to use.  The file can be of any type supported by pygame.image.
  Defaults to font.bmp with no path if omitted.

width x
height y
- Specifies the dimensions of a character, in pixels.  Each
  character must be of the same width and height.  width defaults
  to 8 and height to 16 if omitted.

transrgb r g b
- Specifies the colour being used to indicate transparency.  If you
  don't wish to use transparency, set this to an unused colour.
  Defaults to black (0, 0, 0) if omitted.

alluppercase
- If present, indicates the font only has one case of letters which
  are specified in the index using upper case letters.	Strings
  rendered with BmpFont.blit() will be converted automatically.  If
  omitted, the font is assumed to have both cases of letters.

- All other lines are treated as character index specifiers with
  the following format:

  char x y

  - char is the character whose position is being specified.  It
	can also be "space" (without quotes) to define a position for
	the space character.
  - x is the column number where char is located.  The position
	within the bitmap will be x * width (where width is specified
	above).
  - y is the row number where char is located.	The position will
	be y * height.
"""

import pygame.image
from pygame.locals import *

__all__ = ["BmpFont"]

class BmpFont:
	"""Provides an object for treating a bitmap as a font."""

	# Constructor - creates a BmpFont object.
	# Parameters:  idxfile - Name of the font index file.
	def __init__(self, idxfile = "font.idx"):
		# Setup default values.
		self.alluppercase = 0
		self.chartable = {}
		self.bmpfile = "font.bmp"
		self.width = 8
		self.height = 16
		self.transrgb = (0, 0, 0)

		# Read the font index.	File errors will bubble up to caller.
		f = open(idxfile, "r")

		for x in f.xreadlines():
			# Remove EOL, if any.
			if x[-1] == '\n': x = x[:-1]
			words = x.split()

			# Handle keywords.
			if words[0] == "bmpfile":
				self.bmpfile = x.split(None, 1)[1]
			elif words[0] == "alluppercase":
				self.alluppercase = 1
			elif words[0] == "width":
				self.width = int(words[1])
			elif words[0] == "height":
				self.height = int(words[1])
			elif words[0] == "transrgb":
				self.transrgb = (int(words[1]), int(words[2]),
								 int(words[3]))
			else:  # Default to index entry.
				if words[0] == "space": words[0] = ' '
				if self.alluppercase: words[0] = words[0].upper()
				self.chartable[words[0]] = (int(words[1]) * self.width,
											int(words[2]) * self.height)
		f.close()

		# Setup the actual bitmap that holds the font graphics.
		self.surface = pygame.image.load(self.bmpfile)
		self.surface.set_colorkey(self.transrgb, RLEACCEL)

	# blit() - Copies a string to a surface using the bitmap font.
	# Parameters:  string	 - The message to render.  All characters
	#						   must have font index entries or a
	#						   KeyError will occur.
	#			   surf 	 - The pygame surface to blit string to.
	#			   pos		 - (x, y) location specifying location
	#						   to copy to (within surf).  Meaning
	#						   depends on usetextxy parameter.
	#			   usetextxy - If true, pos refers to a character cell
	#						   location.  For example, the upper-left
	#						   character is (0, 0), the next is (0, 1),
	#						   etc.  This is useful for screens with
	#						   lots of text.  Cell size depends on the
	#						   font width and height.  If false, pos is
	#						   specified in pixels, allowing for precise
	#						   text positioning.
	def blit(self, string, surf, pos = (0, 0), usetextxy = 1):
		"""Draw a string to a surface using the bitmapped font."""
		x, y = pos
		if usetextxy:
			x *= self.width
			y *= self.height
		surfwidth, surfheight = surf.get_size()
		fontsurf = self.surface.convert(surf)

		if self.alluppercase: string = string.upper()

		# Render the font.
		for c in string:
			# Perform automatic wrapping if we run off the edge of the
			# surface.
			if x >= surfwidth:
				x -= surfwidth
				y += self.height
				if y >= surfheight:
					y -= surfheight

			surf.blit(fontsurf, (x, y),
					 (self.chartable[c], (self.width, self.height)))
			x += self.width

# Example code.  Run this file as a script to activate.
if __name__ == "__main__":
	import pygame
	pygame.init()
	screen = pygame.display.set_mode((400, 300), 0, 16)
	# Assumes font.idx and font.bmp are in the current directory.
	bmpfont = BmpFont()
	msg = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"\
		  "0123456789 !@#$%^&*()-=_+\|[]{};:'\",.<>/?`~" * 5
	bmpfont.blit(msg, screen)
	while pygame.event.poll().type != QUIT: pass

# End of file bmpfont.py
