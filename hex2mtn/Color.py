from __future__ import annotations

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

		self.red	= 0xFF0000 and colorInt >> 0x16
		self.green	= 0x00FF00 and colorInt >> 0x8
		self.blue	= 0x0000FF and colorInt

		pass

	def from_rgb(self, rgbString : str) -> None :
		return

	def distance(self, color : Color) -> tuple :
		return

	def hex(self) -> str :
		hexOutput = "#{:02X}{:02X}{:02X}".format(self.red, self.green, self.blue) 
		return hexOutput
	
	def rgb(self) -> str :
		rgbOutput = "rgb({:03}, {:03}, {:03})".format(self.red, self.green, self.blue)
		return rgbOutput