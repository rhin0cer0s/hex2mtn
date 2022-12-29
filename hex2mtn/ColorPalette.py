import logging
from hex2mtn.Color import Color

class ColorPalette() :
    """ Attributes' architecture : { 
        'name' : 'colorPalette's name'  
        'colors' : {
            'color_1' : {
                'color' : <hex2mtn.Color.Color>,
                'similar' : {
                    'vendor_1' : {
                        'productLine_1' : [ ... ],
                        'productLine_2' : [ ... ]
                    }
                }
            },
            'color_2' : { ... }
        }    
    }
    """
    def __init__(self, name : str = "unamedColorPalette", nb_similar_colors=1) :
        self.name = name
        self.colors = {}
        self.vendors = []
        self.nb_similar_colors=nb_similar_colors

    def add(self, color) :
        if color.name in self.colors.keys() :
            logging.warning(f"[!] {color.name} already set in this colorPalette. Ignoring ... ")
            return
        self.colors[color.name] = {
            "color" : color,
            "similar" : {}
        }

    """
    This function loop through the `self.colors`atribute and extract `Color` objects used to create the palette.
    :return list of `Color` object:
    """
    def get_input_colors(self) -> list :
        return [entry['color'] for key, entry in self.colors.items()] 

    def loadColors(self, colors) :
        for color in colors :
            self.add(color)

    def find_similar_colors (self):
        for colorName in self.colors.keys() :
            for vendor in self.vendors :
                color = self.colors[colorName]['color']
                self.colors[colorName]["similar"][vendor.name] = vendor.similar_colors(color, self.nb_similar_colors)

    def pretty_print(self) :
        print(f"# {self.name}")
        for colorName in self.colors.keys() :
            print(f"## {self.colors[colorName]['color']}")
            for vendor,similarColors in self.colors[colorName]['similar'].items() :
                print(f"### {vendor}")
                for productLine, similarColors in similarColors.items() :
                    print(f"\t{productLine} : ")
                    for (distance,productName) in similarColors :
                        print(f"\t\t[{distance:06}] {productName}")
                    print()

