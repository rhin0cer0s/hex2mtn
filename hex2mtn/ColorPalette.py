import logging
from turtle import width

from PIL import Image, ImageDraw, ImageFont
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
    def __init__(self, name : str = "unamedColorPalette") :
        self.name = name
        self.colors = {}
        self.vendors = []
        self.square_size = 150

    def add(self, color) :
        if color.name in self.colors.keys() :
            logging.warning(f"[!] {color.name} already set in this colorPalette. Ignoring ... ")
            return
        self.colors[color.name] = {
            "color" : color,
            "similar" : {}
        }

    def loadColors(self, colors) :
        for color in colors :
            self.add(color)

    def find_similar_colors (self):
        for colorName in self.colors.keys() :
            for vendor in self.vendors :
                color = self.colors[colorName]['color']
                self.colors[colorName]["similar"][vendor.name] = vendor.similar_colors(color)

    def pretty_print(self) :
        print(f"# {self.name}")
        print(self.colors)
        for colorName in self.colors.keys() :
            print(f"## {self.colors[colorName]['color']}")
            for vendor,similarColors in self.colors[colorName]['similar'].items() :
                print(f"### {vendor}")
                for productLine, similarColors in similarColors.items() :
                    print(f"\t{productLine} : ", end='')
                    for productName in similarColors :
                        print(f"{productName}", end='')
                    print()

    # def compute_image_size(self, similarColors) :
    #     logging.debug("[*] Function : compute_image_size...")
    #     print(similarColors)
    #     nbMaxSimilarColors = 0
    #     for similarColor in similarColors :
    #         if len(similarColor['tout-support-belton-molotow-premium-400ml']) > nbMaxSimilarColors :
    #             nbMaxSimilarColors = len(similarColor['tout-support-belton-molotow-premium-400ml'])
    #     logging.debug("[+] nbMaxSimilarColors : {}".format(nbMaxSimilarColors))

    #     height = len(similarColors) * self.square_size
    #     logging.debug("[+] Image Height : {}".format(height))

    #     width = self.square_size + nbMaxSimilarColors * self.square_size
    #     logging.debug("[+] Image Width : {}".format(width))

    #     return (width, height)

    # def draw_inputColors_square(self, drawing) :
    #     for idx, inputColor in enumerate(self.inputColors) :

    #         inputColorP0 = (0, idx * self.square_size)
    #         inputColorP1 = (self.square_size, (idx+1) * self.square_size) 
    #         drawing.rectangle(xy=(inputColorP0, inputColorP1), fill=inputColor.hex())

    #         colorInformationText = "{} - {} ".format(inputColor.hex(), inputColor.rgb())
    #         font = ImageFont.truetype("Tests/fonts/NotoSans-Regular.ttf", 8)
    #         drawing.text(xy=inputColorP1, text=colorInformationText, anchor="rd", font=font, fill="black")

    # def draw_similarColors_square(self, drawing, similarColors) :
    #     for idx, similarColor in enumerate(similarColors) :
    #         inputColorP0 = (self.square_size, idx * self.square_size)
    #         inputColorP1 = (self.square_size*2, (idx+1) * self.square_size) 
    #         drawing.rectangle(xy=(inputColorP0, inputColorP1), fill=similarColor['tout-support-belton-molotow-premium-400ml'][0].hex())

    #         colorInformationText = "{} \n{} - {} ".format(similarColor['tout-support-belton-molotow-premium-400ml'][0].name, similarColor['tout-support-belton-molotow-premium-400ml'][0].hex(), similarColor['tout-support-belton-molotow-premium-400ml'][0].rgb())
    #         font = ImageFont.truetype("Tests/fonts/NotoSans-Regular.ttf", 8)
    #         drawing.text(xy=inputColorP1, text=colorInformationText, font=font, fill="black", align="right", anchor="rd")

    # def color_chart(self, outputFilePath : str) :
    #     logging.debug("[+] Creating color chart ...")

    #     similarColors = self.find_similar_colors()
    #     imageSize = self.compute_image_size(similarColors)

    #     chartImage = Image.new(mode="RGB", size=imageSize, color=0x0000FF)
    #     chartDraw = ImageDraw.Draw(chartImage)

    #     self.draw_inputColors_square(chartDraw)
    #     self.draw_similarColors_square(chartDraw, similarColors)

    #     chartImage.save("./test.png")
