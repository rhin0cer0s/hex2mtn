import logging
from turtle import width
from PIL import Image, ImageDraw, ImageFont

from hex2mtn.Color import Color
from hex2mtn.ColorPalette import ColorPalette

class ColorChart():

    def __init__(self, color_palette : ColorPalette, square_size : int = 150) -> None:
        self.palette = color_palette
        self.square_size = square_size
        self.width, self.height = self._compute_image_size()

    def _compute_image_size(self) :
        height = len(self.palette.colors) * self.square_size
        logging.debug("[+] Image Height : {}".format(height))

        width = self.square_size + self.palette.nb_similar_colors * self.square_size
        logging.debug("[+] Image Width : {}".format(width))

        return (width, height)

    def _draw_inputColors_square(self, drawing, inputColor, idx) :

        inputColorP0 = (0, idx * self.square_size)
        inputColorP1 = (self.square_size, (idx+1) * self.square_size) 
        drawing.rectangle(xy=(inputColorP0, inputColorP1), fill=inputColor.hex())

        colorInformationText = "{} - {} ".format(inputColor.hex(), inputColor.rgb())
        font = ImageFont.truetype("Tests/fonts/NotoSans-Regular.ttf", 8)
        drawing.text(xy=inputColorP1, text=colorInformationText, anchor="rd", font=font, fill="black")

    def _draw_similarColors_square(self, drawing, similarColors, row) :

        for column, similarColor in enumerate(similarColors['Montana']['mtn-94']) :
            inputColorP0 = ((column+1) * self.square_size, row * self.square_size)
            inputColorP1 = ((column+2) * self.square_size, (row+1) * self.square_size) 

            drawing.rectangle(xy=(inputColorP0, inputColorP1), fill=similarColor[1].hex())

            colorInformationText = f"{similarColor[0]}\n{similarColor[1].name}\n{similarColor[1].hex()} - {similarColor[1].rgb()}"
            font = ImageFont.truetype("Tests/fonts/NotoSans-Regular.ttf", 8)
            drawing.text(xy=inputColorP1, text=colorInformationText, font=font, fill="black", align="right", anchor="rd")

    def draw(self, outputFilePath : str) :
        logging.debug("[+] Creating color chart ...")

        chartImage = Image.new(mode="RGB", size=(self.width, self.height), color=0x0000FF)
        chartDraw = ImageDraw.Draw(chartImage)

        logging.debug("[!] Drawing colorChart :")
        for row, (colorName, colorInformation) in enumerate(self.palette.colors.items()) :
            logging.debug(f"\t#{row} | {colorName}")

            colorInput = colorInformation['color']
            colorSuggestions = colorInformation['similar']

            # Draw inputColor as the first of the row
            self._draw_inputColors_square(chartDraw, colorInput, row)

            self._draw_similarColors_square(chartDraw, colorSuggestions, row)

        chartImage.save("./test.png")
