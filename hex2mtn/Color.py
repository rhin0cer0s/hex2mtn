from __future__ import annotations
import json

class Color() :

	def __init__(self, name : str, red : int = 0, green : int = 0, blue : int = 0) :
		self.name	= name
		self.red	= red
		self.green	= green
		self.blue	= blue

	def __eq__(self, other: Color) -> bool:
		if self.red == other.red and self.green == other.green and self.blue == other.blue :
			return True
		return False

	def __str__(self) -> str :
		output = "{} : {} - {}".format(self.name, self.hex(), self.rgb())
		return output 

	def from_hex(self, hexString : str) -> None :
		# Remove potential web hex identifiers '#'
		if hexString[0] == '#' :
			hexString = hexString[1:]

		colorInt = int(hexString, 16)

		# Check web value boundaries
		if colorInt > 0xFFFFFF or colorInt < 0 :
			raise ValueError('{} is not a right HEX value.'.format(hexString))

		self.red	= (0xFF0000 & colorInt) >> 16
		self.green	= (0x00FF00 & colorInt) >> 8
		self.blue	= (0x0000FF & colorInt)

		pass

	def from_rgb(self, rgbString : str) -> None :
		raise NotImplementedError

	def distance(self, color : Color) -> int :
		red		= (self.red - color.red)**2
		green	= (self.green - color.green)**2
		blue	= (self.blue - color.blue)**2

		return red + green + blue

	def hex(self) -> str :
		hexOutput = "#{:02X}{:02X}{:02X}".format(self.red, self.green, self.blue) 
		return hexOutput
	
	def rgb(self) -> str :
		rgbOutput = "rgb({:03}, {:03}, {:03})".format(self.red, self.green, self.blue)
		return rgbOutput

	def reprJSON(self) -> dict :
		return self.__dict__

class ColorJsonEncoder(json.JSONEncoder) :
	
	def default(self, o: Color) -> dict:
		return o.__dict__