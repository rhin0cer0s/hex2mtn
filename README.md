TODO :
- ini config file for vendor
    * base path for datafile
    * color square size
- proxy config
- add argument productline
- create a visual test pipeline : random HEX generator and similar proposition
- arguments
	* productLine
	* color-chart creation
	* color-chart path
	* palette name
- colorPalette :
	* prendre en compte plusieurs productline
	* optimisation : `find_similar_colors()` function computes every distances, sort them and keep only the N first.

# Changelog :

- 2022/12/29 :
	- create `ColorChart` class to save output as an image

- 2022/12/25 :
	- add `nb_similar_colors` parameter to several function. The script now outputs `nb_similar_colors` colors suggestion.

- 2022/12/24 :
	- Version 0.1

- 2022/04/24 :
	- create git repository
	- add base files :
		* main.py
		* hex2mtn/Color.py
		* hex2mtn/ColorPalette.py
		* hex2mtn/Vendor.py
		* hex2mtn/MontanaVendor.py
		* hex2mtn/MolotowVendor.py
	- Color.py :
		* real bitwise operator improvement
	- ColorPalette.py :
		* description of attributes architecture
		* add ```add()``` function to add a ```Color``` to the palette
		* edit ```find_similar_colors()``` function to respect the object architecture
		* add ```pretty_print()``` function to nicely print object's attributes
		* all code related to the color chart creation temporarily commented out as long as vendor's properties are not dynamic
