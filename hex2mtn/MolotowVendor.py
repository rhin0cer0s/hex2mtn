
import logging
import requests

from bs4 import BeautifulSoup

from hex2mtn.Vendor import Vendor
from hex2mtn.Color import Color

class Molotow(Vendor) :
    
    def __init__(self, workingFolder):
        self.rootProductPage = "https://molotow.fr/bombe-de-peinture-"
        self.productLine = [ 'tout-support-belton-molotow-premium-400ml' ]
        super().__init__(workingFolder=workingFolder, name="Molotow", dataFile="molotow.json")

    def _parse_data(self, html : str) :
        """Parse HTML data from the vendor's website.
        The output is an array of <class Color>.
        """

        soup = BeautifulSoup(html, 'html.parser')
        logging.debug(f"[-] Raw soup : \n{soup.text}")
        items_color = soup.find_all("div", class_="grid__options-item")

        if not items_color :
            raise ValueError("No grid__options-item class found.")

        data = []

        for item in items_color : 
            divs = item.find("div", class_="info")
            colorName = divs.find("h4").string
            colorHEX = divs.find_all("li")[1].string
            logging.debug(f"{colorName} : {colorHEX}")

            newColor = Color(colorName)
            try :
                newColor.from_hex(colorHEX)
            except ValueError :
                logging.debug(f"[!] No HEX code found for {colorName}! Pass.")
                del newColor
                continue
            data.append(newColor)

        if not data :
            raise ValueError("No HEX code found on the product page.")

        return data

    def download_data(self) :
        logging.info(f"[*] Download data from {self.name}'s Website ...")

        for product in self.productLine:
            logging.debug("[-] Product : {}".format(product))
            productUrl = f"{self.rootProductPage}{product}.html"
            logging.debug(f"[-] URL : {productUrl}")
            response = requests.get(productUrl)

            if response.status_code != 200:
                logging.info("[!] Error getting {} informations.".format(product))
                continue

            html = response.text
            colorList = self._parse_data(html)
            self.data.update([(product, colorList)])

        if self.data == {} :
            raise Exception(f"Unable to get any information for {self.name}. Check rootPageProduct and your internet connexion.")
        pass
    